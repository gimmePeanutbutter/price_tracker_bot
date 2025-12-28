from selenium import webdriver
from selenium.webdriver.chrome.service import Service 
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import requests
import heapq


class Scraper:
    def __init__(self,discord_url):
        print("Initializing JibScraper...")
        self.discord_url = discord_url
        self.service = Service(ChromeDriverManager().install())
        self.options = Options()
        self.options.add_argument("--headless")
        self.options.add_argument("--disable-gpu")
        self.options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        
        self.driver = webdriver.Chrome(service=self.service,options=self.options)
        self.wait = WebDriverWait(self.driver,20)
        
    
    
    def send_alert(self,message):
        text = {"content":message}
        requests.post(self.discord_url,json=text)

    def close(self):
        self.driver.quit()

    def check_product(self,url):
        raise NotImplementedError("Must be implement")
    
   


class JIB_Scraper(Scraper):
    def __init__(self, discord_url,catagory):
        super().__init__(discord_url)
        self.catagory = catagory
        match catagory:
            case '1':
                self.catagory = 'https://www.jib.co.th/web/product/product_list/3/2988/0?price=&brand=&vga_sp_bus_type=&vga_sp_series='
            case '2':
                self.catagory = 'https://www.jib.co.th/web/product/product_list/3/2615'
        self.jib_product = []

    def check_product(self,name,product_url,target_price):
        try:
            print(f"Checking {name} on JIB...")
            self.driver.get(product_url)

            price_element = self.wait.until(ec.visibility_of_element_located((By.XPATH,'//*[@id="price_box"]/div[4]/div/div/div[1]/strong')))
            price = int(price_element.text.replace(",",""))
            buy_button = self.driver.find_elements(By.XPATH,'//*[@id="price_box"]/div[8]/div/div/div')
            

            if len(buy_button) > 0:
                print("Checking for price....")
                if price <= int(target_price):
                    print(f"Price is cheap now-- ({price})")
                    msg = f"🚨 **DEAL FOUND!**\n{name} is now {price} THB!\n{product_url}"   
                    self.send_alert(msg)
                else:
                    print("Price is still higher than target price.")
            else:
                print("OUT OF STOCK...")
        except Exception as e:
            print(f"Eror: {e}")
    

    def hunt_cheapest(self,keyword):
        print(f"🌲 Hunting for '{keyword}'...")
        self.driver.get(self.catagory)
        self.wait.until(ec.visibility_of_element_located((By.XPATH,'//*[@id="body"]/div/div/div/div[2]/div/div/div/div[4]/div/div[1]/div/div[4]/div/a/div/div/div/div/span')))
        cards = self.driver.find_elements(By.XPATH,'//*[@id="body"]/div/div/div/div[2]/div/div/div/div[4]/div/div')
        print(f" -> Found {len(cards)} items on the shelf.")

        product_heap = []

        for card in cards:
            try:
                name_element = card.find_element(By.XPATH,'./div/div[4]/div/a/div/div/div/div/span')
                name = name_element.text

                if keyword.lower() in name.lower().strip():
                    price_element = card.find_element(By.XPATH,'./div/div[4]/div/div[1]/div/div[7]/div/div/div/div/div/div[2]/p')
                    price = int(price_element.text.replace(",",""))
                    link = card.find_element(By.XPATH,'./div/div[4]/div/a').get_attribute('href')

                    heapq.heappush(product_heap,(price,name,link))
            except Exception:
                continue


        print("\n🏆 --- TOP 3 CHEAPEST DEALS ---")
        msg = f"Top 3 product cheapest price for {keyword}"
        self.send_alert(msg)

        count = 0
        limit = min(3,len(product_heap))
        
        while count < limit:
            best_price,best_name,best_link = heapq.heappop(product_heap)
            
            target_price = int(best_price - best_price * 0.15)
            temp_dict = {"name": best_name,
                         "URL": best_link,
                         "target_price": target_price}
            self.jib_product.append(temp_dict)
            msg += f"\n\n{best_name} --\n{best_price} THB --\n{best_link}"
            
            count += 1
        
        if count > 0:
            self.send_alert(msg)
        else:
            print("no item found")

        
