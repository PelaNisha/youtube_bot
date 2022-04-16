from urllib import response
from aiohttp import request
from googleapiclient.discovery import build
from dotenv import load_dotenv
import os
import json
import requests
from pprint import pprint


load_dotenv()


youtube = build('youtube','v3', developerKey = os.getenv('api_key'))


def get_playlist():
	final_list = []
	with open('input.txt') as f:
		for line in f:
			for channel_name in line.split():
				initial_request = youtube.channels().list(
				part = 'contentDetails, statistics',
				forUsername = channel_name
				)
				initial_respons= initial_request.execute()
				channel_id = initial_respons['items'][0]['id']				
				
				final_request = youtube.playlists().list(
					part="snippet,contentDetails",
					channelId= channel_id,
					maxResults=5
				)
				final_respons= final_request.execute()
				for item in final_respons['items']:

					playlist_date = item['snippet']['publishedAt']
					published_title = item['snippet']['title']
					description = item['snippet']['description']		# average views in all channels
					playlist_id = item['id']
					playlist_videos = get_videos_of_playlists(playlist_id)
					# info_dict = {'playlist date':playlist_date,'published_title':published_title,'description':description}
					# final_list.append(info_dict)
					print(playlist_videos)
	# sort the final_list according to the subscribers count
	li = sorted(final_list, key=lambda i: i['playlist date'],reverse=True)
	return li


def get_videos_of_playlists(playlist_list):
	initial_request = youtube.playlistItems().list(
					part="contentDetails",
					playlistId= playlist_list,
					maxResults=5
	)
	initial_response = initial_request.execute()
	for item in initial_response['items']:
		print(item['contentDetails']['videoId'])


# saves the final_result to file.json
def save_to_file(final_result):
	with open('file1.json', "w+") as f:
		json.dump(final_result, f, indent = 2)

# x =get_playlist()
# print(x)
get_videos_of_playlists('PLOU2XLYxmsILpEjOkRY0C7Bl6t6cUFFxf')
# pprint(x)