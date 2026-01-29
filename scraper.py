from selenium import webdriver
from selenium.webdriver.chrome.service import Service 
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import requests
import heapq
import time

class Scraper:
    def __init__(self, discord_url):
        self.discord_url = discord_url
        self.service = Service(ChromeDriverManager().install())
        self.options = Options()
        self.options.add_argument("--headless") 
        self.options.add_argument("--disable-gpu")
        self.options.add_argument("--log-level=3")
        self.options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        
        self.driver = webdriver.Chrome(service=self.service, options=self.options)
        self.wait = WebDriverWait(self.driver, 20)
        
    def send_alert(self, message):
        if not self.discord_url:
            return
            
        data = {"content": message}
        try:
            response = requests.post(self.discord_url, json=data)
        except Exception as e:
            print(f"Connection Error: {e}")

    def close(self):
        self.driver.quit()

    def check_product(self, url):
        raise NotImplementedError("Subclasses must implement this method")


class JIB_Scraper(Scraper):
    def __init__(self, discord_url, category_choice):
        super().__init__(discord_url)
        
        if category_choice == '1':
            self.category_url = 'https://www.jib.co.th/web/product/product_list/2/51'
        elif category_choice == '2':
            self.category_url = 'https://www.jib.co.th/web/product/product_list/1/1418'
        self.jib_product = []

    def hunt_cheapest(self, keyword):
        print(f"Searching for '{keyword}'...")
        self.driver.get(self.category_url)
        
        try:
            self.wait.until(ec.visibility_of_element_located((By.XPATH, '//*[@id="body"]/div/div/div/div[2]/div/div/div/div[4]/div/div[1]/div/div[4]/div/a/div/div/div/div/span')))
            cards = self.driver.find_elements(By.XPATH, '//*[@id="body"]/div/div/div/div[2]/div/div/div/div[4]/div/div')
            print(f"Found {len(cards)} items.")
        except Exception as e:
            print(f"Error loading shelf: {e}")
            return

        product_heap = []

        for card in cards:
            try:
                name_element = card.find_element(By.XPATH, './div/div[4]/div/a/div/div/div/div/span')
                name = name_element.text

                if keyword.lower().replace(" ", "") in name.lower().replace(" ", ""):
                    price_element = card.find_element(By.XPATH, './div/div[7]/div/div/div/div/div/div[2]/p')
                    price_text = price_element.text.replace(",", "").replace("-", "").strip().replace(".", "")
                    
                    if not price_text.isdigit(): 
                        continue 
                        
                    price = int(price_text)
                    link = card.find_element(By.XPATH, './div/div[4]/div/a').get_attribute('href')

                    heapq.heappush(product_heap, (price, name, link))
            except Exception:
                continue

        print(f"Processing top deals for '{keyword}'...")
        
        count = 0
        limit = min(3, len(product_heap))
        
        while count < limit:
            best_price, best_name, best_link = heapq.heappop(product_heap)
            
            target_price = int(best_price*0.9) 
            
            temp_dict = {
                "name": best_name,
                "URL": best_link,
                "target_price": target_price
            }
            self.jib_product.append(temp_dict)
            print(f"[{count+1}] {best_price} THB | {best_name}")
            count += 1
            
        if len(self.jib_product) == 0:
            print("No items found.")

    def check_product(self, name, product_url, target_price):
        try:
            self.driver.get(product_url)
            price_element = self.wait.until(ec.visibility_of_element_located((By.XPATH, '//*[@id="price_box"]/div[4]/div/div/div[1]/strong')))
            current_price = int(price_element.text.replace(",", ""))
            
            buy_buttons = self.driver.find_elements(By.XPATH, '//*[@id="price_box"]/div[8]/div/div/div')
            
            print(f"Checking: {name[:30]}... | Price: {current_price}")

            if len(buy_buttons) > 0:
                if current_price <= int(target_price):
                    msg = f"PRICE ALERT\nProduct: {name}\nPrice: {current_price} THB\nLink: {product_url}"   
                    self.send_alert(msg)
            else:
                print("Out of Stock")

        except Exception as e:
            print(f"Error checking product: {e}")