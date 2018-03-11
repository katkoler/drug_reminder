from chalice import Chalice, Rate, Cron
import nexmo
from dotenv import load_dotenv
import os
# import config #need your config file 

load_dotenv()

app = Chalice(app_name='timed_reminders')


NEXMO_API_KEY = os.getenv("NEXMO_API_KEY")
NEXMO_API_SECRET = os.getenv("NEXMO_API_SECRET")


TO_NUMBER = "447543610370"
reminder = {"Drug_name": "aspirin", "Interval": 1, "Unit":"hours", "Amount":20, "Start date":"2018/03/10"}


client = nexmo.Client(key=NEXMO_API_KEY, secret=NEXMO_API_SECRET)


@app.route('/')
def index():
    return {'hello': 'world'}


# @app.schedule(Rate(1, unit=Rate.MINUTES))
@app.route('/send')
def handler(foo):
	resp = client.send_message({
	    'from': 'reminder',
	    'to': TO_NUMBER,
	    # 'to': "447805946442",
	    'text': 'drug reminder!!',
	})
	print(resp)
	return 'ok'

# @app.schedule(Rate(1, unit=Rate.MINUTES))
# @app.route('/send')
# def handler(foo):
# 	#look through the file, line by line - extract the fields  and prep them for the message
# 	if datetime.datetime.now() > scheduled_time:
# 		resp = client.send_message({
# 		    'from': 'Drug remndr',
# 		    'to': TO_NUMBER,
# 		    # 'to': "447805946442",
# 		    'text': text_content,
# 		})
# 		print(resp)
# 	return 'ok'



# Cron(minutes, hours, day_of_month, month, day_of_week, year)
# Run every 5 minutes Monday through Friday between
# 08:00am and 5:55pm (UTC).
# Cron('0/5', '8-17', '?', '*', 'MON-FRI', '*')
# Run every 15 minutes.
# Cron('0/15', '*', '*', '*', '?', '*')
# Run every 10 minutes Monday through Friday.
# Cron('0/10', '*', '?', '*', 'MON-FRI', '*')

# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.current_request.json_body
#     # We'll echo the json body back to the user in a 'user' key.
#     return {'user': user_as_json}
#
# See the README documentation for more examples.
#
