# Rank the channels
from googleapiclient.discovery import build
from dotenv import load_dotenv
import os
from math import log, floor
import json


load_dotenv()


youtube = build('youtube','v3', developerKey = os.getenv('api_key'))


# Function to return the name, average view on videos and 
# Subscriber count according to channel_name as in 'file.txt'
def get_channel_avg_views_and_subs():
	final_list = []
	with open('input.txt') as f:
		for line in f:
			for channel_name in line.split():
				initial_request = youtube.channels().list(
							part = 'contentDetails, statistics',
							forUsername = channel_name
				)
				initial_respons= initial_request.execute()
				total_videos = initial_respons['items'][0]['statistics']['videoCount']
				total_subs = initial_respons['items'][0]['statistics']['subscriberCount']
				total_view_count = initial_respons['items'][0]['statistics']['viewCount']
				avg_views= int(total_view_count)/int(total_videos) 		# average views in all channels
				info_dict = {'name':channel_name,'avg_view':str(num_formatting(avg_views)),'subcribers_count':int(total_subs)}
				final_list.append(info_dict)

	# Sort the final_list according to the subscribers count
	li = sorted(final_list, key=lambda i: i['subcribers_count'],reverse=True)
	return li


# Function to give tags for numbers like thousand, million,etc
def num_formatting(avg_view):
	units = ['', 'K', 'M', 'G', 'T', 'P']
	k = 1000.0
	magnitude = int(floor(log(avg_view, k)))
	return '%.2f%s' % (avg_view / k**magnitude, units[magnitude])
  

# Saves the final_result to file.json
def save_to_file(final_result):
	with open('file.json', "w+") as f:
		json.dump(result, f, indent = 2)


# Opens file.json, reads it and parse according to use
def read_data():
	with open('file.json', "r") as f:
		data = json.load(f)
		for i in range(0, len(data)):
			print(data[i]['name'])

			
result = get_channel_avg_views_and_subs()
save_to_file(result)
