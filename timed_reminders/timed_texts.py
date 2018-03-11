
import os
import nexmo
import config #need your config file 

NEXMO_API_KEY = "e68cada7"
NEXMO_API_SECRET = "AXb198qZSVjABNPp"

client = nexmo.Client(key=NEXMO_API_KEY, secret=NEXMO_API_SECRET)
TO_NUMBER = "447543610370"


client.send_message({
	    'from': 'Drug rmndr',
	    'to': TO_NUMBER,
	    # 'to': "447805946442",
	    'text': 'Hi Kat, please make sure you take your scheduled Ibuprofen',
	})