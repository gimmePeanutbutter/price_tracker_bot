from scraper import JIB_Scraper
import time

discord_url = 'https://discord.com/api/webhooks/1452066365811982522/lg1JnyJpOLaNyqN8-3GrDPPVleQ6RieM46yLeWGPxtkmlAkW96I0pNdeSKsdFQl5rOoU'


if __name__ == "__main__":
    
    while True:
        print("\n--- Start hunting ---")
        catagory_input = input("Please choose the catagory:\n1 for RTX 50 series\n2 for RTX 40 series\n> ").strip()
        if catagory_input in {"1", "2"}:
            break
        print("Please choose only number that shown")

    keyword_input = input("--Please insert keyword of product ---> : ").strip()

    print("🤖 Bot Manager Started...")
            jib_bot = JIB_Scraper(discord_url,catagory_input)

   try:
        while True:
            print("\n🔄 Checking prices cycle...")
            
            for item in jib_bot.jib_product:
                jib_bot.check_product(item["name"], item["URL"], item["target_price"])
                time.sleep(2) 
            
            print("💤 Cycle complete. Sleeping for 60 seconds...")
            time.sleep(60) 

    except KeyboardInterrupt:
        print("\n🛑 Stop signal received.")
    finally:
        jib_bot.close()
        print("Bot Closed.")
