import time,configparser,os,sys,requests,zipfile
from Static.Static import Static
try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    import pytesseract
    from PIL import Image
except:
    print('Installing Libraries...')
    os.system("pip install -r requirements.txt")
    print('Libraries installed. Restart the program!')
    sys.exit()

def Download(url, extract_to='.'):
    response = requests.get(url)
    zip_path = os.path.join(extract_to, "downloaded_file.zip")
    with open(zip_path, 'wb') as file:
        file.write(response.content)
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    os.remove(zip_path)
    
if not os.path.exists('Tesseract'):
    print('Downloading Tesseract, please wait..')
    url = 'https://drive.usercontent.google.com/download?id=10X_TEAwUic4v3pt7TT4w3QNRcS1DNq87&export=download&authuser=0&confirm=t&uuid=19bcdcbd-e7ce-4617-8f41-caca15b5ab17&at=APZUnTWgmGxytaTOOxw-o87dMp8z%3A1720311459869'  # Substitua pelo URL do seu arquivo .zip
    extract_to = './'
    Download(url, extract_to)

config = configparser.ConfigParser()
config.read('config.cfg')

TYPE = config.get('Settings','TYPE')
VIDEO = config.get('Settings','VIDEO_URL')
AMOUNT = config.getint('Settings','AMOUNT')
class Program():
    def __init__(self):
        self.Options = webdriver.ChromeOptions()
        print('Installing Extensions...')
        self.Options.add_extension('Extensions/ub.crx')
        if config.getboolean('Settings','HEADLESS') : self.Options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=self.Options)
        self.driver.get('https://zefoy.com/')
        pytesseract.pytesseract.tesseract_cmd = r'Tesseract/tesseract.exe'
        self.driver.find_element(By.XPATH,'/html/body/div[8]/div[2]/div[1]/div[3]/div[2]/button[1]').click()
        time.sleep(0.5)
        while not self.PassCaptcha():
            self.driver.refresh()
            time.sleep(1.5)
            continue
        time.sleep(5)
        self.SelectType()

    def PassCaptcha(self):
        with open('Captcha/captcha.png', 'wb') as file:
            file.write(self.driver.find_element(By.XPATH,'/html/body/div[5]/div[2]/form/div/div/img').screenshot_as_png)
        time.sleep(0.1)
        self.driver.find_element(By.XPATH,'/html/body/div[5]/div[2]/form/div/div/div/input').send_keys(pytesseract.image_to_string(Image.open('Captcha/captcha.png')))

        if self.PassedCaptcha():
            return True
        return False
    def PassedCaptcha(self):
        try:
            self.driver.find_element(By.ID,'errorcapthcaclose').click()
            return False
        except:
            return True
        
    def SelectType(self):
        self.driver.find_element(By.XPATH,Static.typeValues[TYPE]).click()
        time.sleep(0.5)
        self.GetViews()

    def GetViews(self):
        time.sleep(1)
        self.driver.find_element(By.XPATH,'/html/body/div[10]/div/form/div/input').send_keys(VIDEO)
        for _ in range(AMOUNT):
            time.sleep(1)
            self.driver.find_element(By.XPATH,'/html/body/div[10]/div/form/div/div/button').click()
            time.sleep(5)
            while True:
                if not self.isReady():
                    time.sleep(5)
                else:
                    break
            time.sleep(1.5)
            self.driver.find_element(By.XPATH,'/html/body/div[10]/div/form/div/div/button').click()
            time.sleep(2)
            self.driver.find_element(By.XPATH,'//*[@id="c2VuZC9mb2xeb3dlcnNfdGlrdG9V"]/div[1]/div/form/button').click()
    def isReady(self):
        return self.driver.find_element(By.XPATH,'//*[@id="c2VuZC9mb2xeb3dlcnNfdGlrdG9V"]/span[1]').text.__contains__('READY') or len(self.driver.find_element(By.XPATH,'//*[@id="c2VuZC9mb2xeb3dlcnNfdGlrdG9V"]/span[1]').text) <= 0

if __name__ == "__main__":                
    Program()