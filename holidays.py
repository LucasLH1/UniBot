#!/usr/bin/env python3

import os 
from slack import WebClient
from slack.errors import SlackApiError
import time
import datetime
from datetime import date
from dateutil.relativedelta import relativedelta, MO
import json
import jsonpickle
from json import JSONEncoder
import re

client = WebClient(token=os.environ['SLACK_KEY'])
channel='A COMPLETER AVEC LID DEFINITIVE DU SALON'

attachments_default = [{
	"blocks": [
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "Hello ! Il est temps de remplir le formulaire d'absences.\n\n*Merci de suivre les instructions ci-dessous.*"
			}
		},
		{
			"type": "divider"
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": ":round_pushpin: *<www.youtube.com|Clique ici pour te rendre sur la fiche d'absences.>* \nSurtout n'oublie pas de réagir avec :heavy_check_mark: afin d'indiquer que c'est bien fait."
			}
		}
	]
}]

attachments_dm = [{
	"blocks": [
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "Hello ! Il est temps de remplir le formulaire d'absences.\n\n*Merci de suivre les instructions ci-dessous.*"
			}
		},
		{
			"type": "divider"
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": ":round_pushpin: *<www.youtube.com|Clique ici pour te rendre sur la fiche d'absences.>* \nSurtout n'oublie pas de réagir avec :heavy_check_mark: sur le message initial du #général afin d'indiquer que c'est bien fait !"
			}
		}
	]
}]



today = date.today()

def last_monday_of_month(any_day):
    next_month = any_day.replace(day=28) + datetime.timedelta(days=4)  # this will never fail
    last_day = next_month - datetime.timedelta(days=next_month.day)
    return last_day + relativedelta(weekday=MO(-2))

last_monday_of_month(date.today())

if today == last_monday_of_month(date.today()):
	response = client.chat_postMessage(channel=channel, text="", attachments=attachments_default)
	timestamp = response['ts']
else:
	print("It's not the good day.")


add_reacts = client.reactions_add(channel=channel,  name="heavy_check_mark", timestamp=timestamp)

today = datetime.datetime.now()

sleep = (datetime.datetime(today.year, today.month, today.day, 23, 59, 59) - today).seconds
print('Waiting for ' + str(datetime.timedelta(seconds=sleep)))
time.sleep(sleep)

def list_users():
	response = client.users_list()
	users = response['members']
	user_ids = list(map(lambda u: u["id"], users))
	return user_ids

def reactions_users():
	reacts = client.reactions_get(channel=channel, timestamp=timestamp)
	reactions_users = reacts["message"]["reactions"][-1]["users"]
	return reactions_users

def send_message(userid):
	dm = client.chat_postMessage(channel=userid, text="", attachments=attachments_dm)


if __name__ == '__main__':
	users = list_users()
	reactions = reactions_users()
	if users != reactions_users:
		rest = set(users) - set(reactions)
		s = list(rest)
		for u in s:
			send_message(u)
		print("Success!")
	else:
		print("Error.")

