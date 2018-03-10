
import os

import nexmo
import config #need your config file 

NEXMO_API_KEY = os.environ["e68cada7"]
NEXMO_API_SECRET = os.environ["AXb198qZSVjABNPp"]

client = nexmo.Client(key=NEXMO_API_KEY, secret=NEXMO_API_SECRET)
TO_NUMBER = "447543610370"


client.send_message({
    'from': 'drug reminder service',
    'to': TO_NUMBER,
    # 'to': "447805946442",
    'text': 'drug reminder!!',
})