import RPi.GPIO as GPIO
import time
import sys
import signal
import threading
import urllib2
import urllib
import json
from datetime import datetime
import os
from twilio.rest import TwilioRestClient

from apiclient.discovery import build
from httplib2 import Http
import oauth2client
from oauth2client import client
from oauth2client import tools

account = "AC5bc10b06dfef6a0d19cfef184406cd74" 
token = "c7fb839a2ebd320b392654eaa01cb22a"
client = TwilioRestClient(account, token)

alarmone = 8
alarmtwo = 7
buttonoff = 25
buttonon = 24

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(10, GPIO.OUT)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(9, GPIO.OUT)
GPIO.setup(3, GPIO.OUT)
GPIO.setup(2, GPIO.OUT)
GPIO.setup(4, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(14, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)
GPIO.setup(alarmone, GPIO.OUT)
GPIO.setup(alarmtwo, GPIO.OUT)
GPIO.setup(buttonoff, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(buttonon, GPIO.IN, GPIO.PUD_UP)
arr = [14,15,18,2,3,4,10,9,11]

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Calendar API Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-api-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatability with Python 2.6
            credentials = tools.run(flow, store)
        print 'Storing credentials to ' + credential_path
    return credentials

def cleansig():
	for i in range(len(arr)):
		GPIO.output(arr[i], False)


def signal_handler(signal, frame):
	GPIO.cleanup()
	sys.exit(0)

def templight(temp):
	new = []
	while temp > 0:
		if temp % 2 >0:
			new.append(1)
		else:
			new.append(0)
		temp = temp/2
	for i in range(len(new)):
		if new[i]>0:
			GPIO.output(arr[i], True)
		else:
			GPIO.output(arr[i], False)	
cleansig()
signal.signal(signal.SIGINT, signal_handler)

credentials = get_credentials()
service = build('calendar', 'v3', http=credentials.authorize(Http()))

while True:
	now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
	eventsResult = service.events().list(
	calendarId='primary', timeMin=now, maxResults=1, singleEvents=True,
	orderBy='startTime').execute()
	events = eventsResult.get('items', [])
	breakflag = 0
	if not events:
	    	breakflag = 1
	for event in events:
		if event['summary']=='Sleep':
			breakflag = 0
		else:
			breakflag = 1
	if breakflag == 1:
		break
	time.sleep(60)

flag = 1
message = client.messages.create(to="+16309950526", from_="+13313056100",body= "Rainbow Unicorn Ninja wants you to wake up! https://myspideysenseistingling.files.wordpress.com/2011/09/behold_a_rainbow_unicorn_ninja_by_jess4921.jpg?w=1017&h=624")
while True:

	if flag == 1:
		cleansig()
		GPIO.output(alarmone,True)
		time.sleep(0.001)
		GPIO.output(alarmone,False)
		time.sleep(0.001)	
	if GPIO.input(buttonoff) == False:
		flag = 0
		baseurl = "https://query.yahooapis.com/v1/public/yql?"
		yql_query = "select item.condition from weather.forecast where woeid=2460432"
		yql_url = baseurl + urllib.urlencode({'q':yql_query}) + "&format=json"
		result = urllib2.urlopen(yql_url).read()
		data = json.loads(result)
		print int(data['query']['results']['channel']['item']['condition']['temp'])
		templight(int(data['query']['results']['channel']['item']['condition']['temp']))
	if GPIO.input(buttonon) == False:
		time.sleep(60)
		flag = 1
