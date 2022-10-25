import time
import requests
import argparse
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

response = requests.get('https://prettygr.im/anyminis/api', timeout=10)
while response != "yes":
    print('In Stock:', response.text)
    time.sleep(5.0)
    response = requests.get('https://prettygr.im/anyminis/api', timeout=10)

title = "Miyoo Mini In Stock!"
url = "https://aliexpress.us/item/3256803425362523.html"
poMessage = "Miyoo Mini In Stock!"
print(poMessage)
sendPushover(apikey, userkey, poMessage, title, url)
