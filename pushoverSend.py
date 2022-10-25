from pushover import Pushover

def sendPushover(apikey,userkey,message,title,url="https://www.google.com/maps"):
    po = Pushover(apikey)
    po.user(userkey)
    msg = po.msg(message)
    msg.set("title", title)
    if url != "https://www.google.com/maps":
        msg.set("url", url)
    po.send(msg)
