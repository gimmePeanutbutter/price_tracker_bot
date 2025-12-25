from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import requests
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
# ... (add your other imports here) ...

class JibScraper:
    def __init__(self, discord_url, headless=True):

        print("Initializing JibScraper...")
        self.discord_url = discord_url
        chorme_option = Options()
        chorme_option.add_argument("--headless")
        chorme_option.add_argument("--disable-gpu")
        chorme_option.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

        self.service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=self.service,options=chorme_option)
        self.wait = WebDriverWait(self.driver,10)
       
    def send_alert(self, message):
        text = {"content":message}
        requests.post(self.discord_url,json=text)


    def check_product(self, product_url, target_price,name):
        try:
            print(f"Checking {name}...")
            self.driver.get(product_url)
            self.price_element = self.wait.until(ec.visibility_of_element_located((By.XPATH,'//*[@id="price_box"]/div[4]/div/div/div[1]/strong')))
            self.price = int(self.price_element.text.replace(",",""))
            
            if self.price <= int(target_price):
                print("Checking for stock....")
                self.buy_button = self.driver.find_elements(By.XPATH,'//*[@id="price_box"]/div[8]/div/div/div')
                if len(self.buy_button) > 0:
                    print("Price is good!!!!!")
                    msg = f"{name} is now {self.price} buy now!"
                    self.send_alert(msg)
                else:
                    print("out of stock")
            else:
                print("Price is still high")
        except Exception as e:
            print(f"Eror: {e}")
        

    def close(self):
        self.driver.quit()
        

