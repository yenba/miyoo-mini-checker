# import the things you need to run the script
import time
import sys
import datetime
from playwright.sync_api import Playwright, sync_playwright, expect
import argparse
from prettytable import PrettyTable
from pushoverSend import sendPushover

# setup the argument parser
parser = argparse.ArgumentParser(description="This is how you pass Pushover API keys into the script!",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--apikey", help="Pushover API Key")
parser.add_argument("--userkey", help="Pushover User Key")
args = vars(parser.parse_args())

# Set up parameters
apikey = args["apikey"]
userkey = args["userkey"]

#Production Miyoo Mini Stuff
item_URL = "https://www.aliexpress.us/item/3256803425362523.html" # miyoo mini link
sleep_time_normal = 120
sleep_time_fast = 30
item_colors = ['RetroGrey', 'Transparent Black', 'Transparent Blue', 'White'] # colors
poMessage = ""
title = "Miyoo Mini In Stock!"
start_hour = 8 # set the start time for the fast refresh time check later
end_hour = 10 # set the end time for the fast refresh time check later
start = datetime.time(start_hour, 0, 0)
end = datetime.time(end_hour, 0, 0)

# Dev Test Item Stuff
# item_URL = "https://www.aliexpress.us/item/2255800792609328.html" # grinder link
# sleep_time_normal = 120
# sleep_time_fast = 30
# item_colors = ['BLACK C2 GRINDER', 'RED C2 GRINDER', 'BLUE C2 GRINDER', 'WHITE C2 GRINDER'] # colors
# poMessage = ""
# title = "Grinder In Stock!"
# start_hour = 8 # set the start time for the fast refresh time check later
# end_hour = 10 # set the end time for the fast refresh time check later
# start = datetime.time(start_hour, 0, 0)
# end = datetime.time(end_hour, 0, 0)

# setup the class
class AliItem():
    def __init__(self):
        self.url = item_URL
        self.colors = item_colors
        self.open()
        self.load()

    def open(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.firefox.launch(headless=True)
        self.context = self.browser.new_context()
        self.page = self.context.new_page()

    def close(self):
        self.context.close()
        self.browser.close()
        self.playwright.stop()

    def load(self):
        self.page.set_default_timeout(timeout = 120000)  # in milliseconds
        self.page.goto(self.url)
        self.page.wait_for_load_state('networkidle')

    def reload(self):
        self.page.reload()
        self.page.wait_for_load_state('networkidle')

    def check_available(self):
        return self.page.locator(".customs-message-wrap").count() == 0

    def check_total_stock(self):
        txt = self.page.locator(".product-quantity-tip").inner_text()
        return int(''.join(i for i in txt if i.isdigit()))
    
    def time_in_range(self, start, end, current):
        return start <= current <= end

    def check_stock_custom(self):
        Time = datetime.datetime.utcnow().replace(microsecond = 0) # get the current time
        TimePretty = f"Stock at {Time} UTC" # make it pretty with text
        Table = PrettyTable() # make the table but blank
        Table.field_names = ["Color","Stock"] # add the table headers
        Table.title = TimePretty # set the title of the table to the TimePretty variable
        for color in self.colors: # for every color in the color array above, cycle through and do the stuff inside
            self.page.get_by_role("img", name=color).click() # clicks on the image in AliExpress to cycle through the different colors
            time.sleep(1) # sleep for a sec 
            txt = self.page.locator(".product-quantity-tip").inner_text() # grab the actual text (the stock count)
            stock = int(''.join(i for i in txt if i.isdigit())) # convert it to an int
            Table.add_row([color, stock]) # add as a new row to the table
        Table.align = "l" # left align the table
        return Table 

######################
### RUN THE SCRIPT ###
######################

aliItem = AliItem()

while True:
    print()
    if aliItem.check_available():
        # check for stock counts
        StockListMessage = aliItem.check_stock_custom()
        print(StockListMessage, file=sys.stderr)
        print(StockListMessage)

        # send pushover
        poMessage = StockListMessage
        url = item_URL
        sendPushover(apikey, userkey, poMessage, title, url)
    else:
        print("Not In Stock:",datetime.datetime.utcnow().replace(microsecond = 0), file=sys.stderr)

    current = datetime.datetime.utcnow().time()

    if aliItem.time_in_range(start, end, current):
        time.sleep(sleep_time_fast)
        aliItem.reload()
    else:
        time.sleep(sleep_time_normal)
        aliItem.reload()
    