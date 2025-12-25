from scraper_class import JibScraper
import time

DISCORD_WEBHOOK = 'https://discord.com/api/webhooks/1452066365811982522/lg1JnyJpOLaNyqN8-3GrDPPVleQ6RieM46yLeWGPxtkmlAkW96I0pNdeSKsdFQl5rOoU'


products=[{
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
}]


if __name__ == "__main__":
   
    bot = JibScraper(DISCORD_WEBHOOK, headless=True)

    try:
        print("🤖 Bot Manager Started...")
        
        while True:
            print("\n--- Starting Scan Cycle ---")
            
            for item in products:
                
                # The Manager tells the Robot: "Go check this specific item"
                bot.check_product(item['URL'], item['target_price'],item["name"])
                
                time.sleep(2) # Rest between pages
            
            print("Cycle complete. Sleeping for 60 seconds...")
            time.sleep(60)

    except KeyboardInterrupt:
        # This runs if you press Ctrl+C
        print("\n🛑 Stopping bot safely...")
        bot.close()
        print("Bot Closed.")