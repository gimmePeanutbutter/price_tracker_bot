from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import requests
from selenium.webdriver.chrome.options import Options
import time


chorme_option = Options()
chorme_option.add_argument("--headless")
chorme_option.add_argument("--disable-gpu")

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
            
            price = driver.find_element(By.XPATH,'//*[@id="price_box"]/div[4]/div/div/div[1]/strong')

            price_string = price.text
            real_price = int(price_string.replace(",",""))
           
            if real_price < int(i["target_price"]):
                print("Cheap now let's buy")
                msg = f"{i['name']} is now {real_price} buy now!"
                discord_alert(msg)
            else:
                print("too expensive")

        except Exception as e:
            print(f"Error {e}")
        
        time.sleep(2)
        print("scan complete waiting")
    time.sleep(15)

