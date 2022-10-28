# import the things you need to run the script
import time
import sys
import datetime
import apprise
import asyncio
import nest_asyncio
from prettytable import PrettyTable
from prettytable import SINGLE_BORDER
from apprise import NotifyFormat
from playwright.sync_api import sync_playwright

# setup nesting of asyncio
nest_asyncio.apply()

# Production Miyoo Mini Stuff
item_URL = "https://www.aliexpress.us/item/3256803425362523.html" # miyoo mini link
sleep_time_normal = 120
sleep_time_fast = 30
item_colors = ['RetroGrey', 'Transparent Black', 'Transparent Blue', 'White'] # colors
title = "Miyoo Mini In Stock!"
start_hour = 8 # set the start time for the fast refresh time check later
end_hour = 10 # set the end time for the fast refresh time check later
start = datetime.time(start_hour, 0, 0)
end = datetime.time(end_hour, 0, 0)

# setup apprise
async def sendNotification(title, body, url):   
    pusher = apprise.Apprise()
    config = apprise.AppriseConfig()
    config.add('./config.yml')
    pusher.add(config) 
    
    notify = await pusher.async_notify(
        body=body,
        title=title,
        body_format=NotifyFormat.TEXT,
    )
    return notify

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
        Table.set_style(SINGLE_BORDER)
        return Table 

######################
### RUN THE SCRIPT ###
######################

print("")
print("Starting the script!")
print("")

aliItem = AliItem()

while True:
    if aliItem.check_available():
        # check for stock counts
        StockListMessage = aliItem.check_stock_custom()
        print(StockListMessage, file=sys.stderr)

        # send apprise
        table_txt = StockListMessage.get_string()
        body = f"```{table_txt}```"
        url = item_URL
        push = asyncio.run(sendNotification(title, body, url))

    else:
        print("Not In Stock:",datetime.datetime.utcnow().replace(microsecond = 0), file=sys.stderr)

    current = datetime.datetime.utcnow().time()

    if aliItem.time_in_range(start, end, current):
        time.sleep(sleep_time_fast)
        aliItem.reload()
    else:
        time.sleep(sleep_time_normal)
        aliItem.reload()
    