from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import requests
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

chorme_option = Options()
chorme_option.add_argument("--headless")
chorme_option.add_argument("--disable-gpu")
chorme_option.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service,options=chorme_option)


products={
    "name":" INNO3D GEFORCE RTX 5070 TWIN X2 OC WHITE",
    "URL":"https://www.jib.co.th/web/product/readProduct/75148/2988/VGA--%E0%B8%81%E0%B8%B2%E0%B8%A3%E0%B9%8C%E0%B8%94%E0%B9%81%E0%B8%AA%E0%B8%94%E0%B8%87%E0%B8%9C%E0%B8%A5--INNO3D-GEFORCE-RTX-5070-TWIN-X2-OC-WHITE---12GB-GDDR7--N50702-12D7X-195064W-",
    "target_price":"17500"
},{
    "name":"HONEYWELL WIRELESS SCANNER",
    "URL":"https://www.jib.co.th/web/product/readProduct/70109/2078/HONEYWELL-WIRELESS-SCANNER-%E0%B9%80%E0%B8%84%E0%B8%A3%E0%B8%B7%E0%B9%88%E0%B8%AD%E0%B8%87%E0%B8%AA%E0%B9%81%E0%B8%81%E0%B8%99%E0%B8%9A%E0%B8%B2%E0%B8%A3%E0%B9%8C%E0%B9%82%E0%B8%84%E0%B9%89%E0%B8%94%E0%B9%84%E0%B8%A3%E0%B9%89%E0%B8%AA%E0%B8%B2%E0%B8%A2-%E0%B8%AA%E0%B9%81%E0%B8%81%E0%B8%99%E0%B8%9A%E0%B8%B2%E0%B8%A3%E0%B9%8C%E0%B9%82%E0%B8%84%E0%B9%89%E0%B8%94-1D-%E0%B9%81%E0%B8%A5%E0%B8%B0-2D--HH492-R1-1USB-5-",
    "target_price":"9000"
},{
    "name":"ACER ASPIRE LITE 15 AL15-41P-R47V (SILVER)",
    "URL":"https://www.jib.co.th/web/product/readProduct/74431/32/NOTEBOOK--%E0%B9%82%E0%B8%99%E0%B9%89%E0%B8%95%E0%B8%9A%E0%B8%B8%E0%B9%8A%E0%B8%84--ACER-ASPIRE-LITE-15-AL15-41P-R47V--SILVER-",
    "target_price":"1000000"
}



def discord_alert(message):
    bot_url = 'https://discord.com/api/webhooks/1452066365811982522/lg1JnyJpOLaNyqN8-3GrDPPVleQ6RieM46yLeWGPxtkmlAkW96I0pNdeSKsdFQl5rOoU'
    text = {"content":message}
    requests.post(bot_url,json=text)


while True:
    for i in products:
        print(f"looking for item {i["name"]}...")

        try:
            driver.get(i["URL"])
            
            wait = WebDriverWait(driver,10)
            price = wait.until(ec.visibility_of_element_located((By.XPATH,'//*[@id="price_box"]/div[4]/div/div/div[1]/strong')))
            price_string = price.text
            real_price = int(price_string.replace(",",""))
           
            if real_price < int(i["target_price"]):
                print("Price is good checking status....")
                buy_button = driver.find_elements(By.XPATH,'//*[@id="price_box"]/div[8]/div/div/div')
                if len(buy_button) >0:
                     print('In stock sending alert')
                     msg = f"{i['name']} is now {real_price} buy now!"
                     discord_alert(msg)
                else:
                    print("product currently OUT OF STOCK.")
            else:
                print("too expensive")

        except Exception as e:
            print(f"Error {e}")
        
        time.sleep(2)
    print("scan complete waiting")
    time.sleep(15)

