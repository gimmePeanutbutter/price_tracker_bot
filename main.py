from scraper import JIB_Scraper
import time


discord_url = 'https://discord.com/api/webhooks/1466278571520561205/E5qM1HdkE5k2AizBSUDC4Et_gtjtJMKeDJHYgAFTeHkArOKevWtZbpjBz6MVbn1yQ3Ko'

if __name__ == "__main__":
    
    print("\n--- Start hunting ---")
    while True:
        catagory_input = input("Please choose the category:\n1 for Graphics cards\n2 for Apple products\n> ").strip()
        if catagory_input in {"1", "2"}:
            break
        print("Please choose only number that shown")

    keyword_input = input("--Please insert keyword of product ---> : ").strip()

    print(" Bot Manager Started...")
    jib_bot = JIB_Scraper(discord_url, catagory_input)
    
    jib_bot.hunt_cheapest(keyword_input)

    if not jib_bot.jib_product:
        print("No products found Exiting...")
        jib_bot.close()
        exit()

    print(f"Tracking {len(jib_bot.jib_product)} items. Start monitoring...")

    
    try:
        while True:
            print("\n Checking prices cycle...")
            
            for item in jib_bot.jib_product:
                jib_bot.check_product(item["name"], item["URL"], item["target_price"])
                 
            
            print(" Cycle complete. Sleeping for 60 seconds...")
            time.sleep(60) 

    except KeyboardInterrupt:
        print("Bot is closing")
        jib_bot.close()