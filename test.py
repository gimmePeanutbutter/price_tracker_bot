from scraper import JIB_Scraper

jib_bot = JIB_Scraper('https://discord.com/api/webhooks/1452066365811982522/lg1JnyJpOLaNyqN8-3GrDPPVleQ6RieM46yLeWGPxtkmlAkW96I0pNdeSKsdFQl5rOoU'
,'1')

jib_bot.hunt_cheapest("rtx5070")
for i in jib_bot.jib_product:
    print(i["name"])