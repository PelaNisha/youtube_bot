# program that scrapes a youtube channel and saves its playlists in a file


# modules used
from urllib import response
from aiohttp import request
from googleapiclient.discovery import build
from dotenv import load_dotenv
import os
import json
import re

load_dotenv()


youtube = build('youtube','v3', developerKey = os.getenv('api_key'))


# function that scrape the all data of playlist and saves them in a list of dicts
def get_playlist():
	final_list = []

	# opens input.txt and reads all the  channel names 
	with open('input.txt') as f:
		for line in f:
			for channel_name in line.split():

				# to return the channel_id of the channels
				initial_request = youtube.channels().list(
				part = 'contentDetails, statistics',
				forUsername = channel_name
				)
				initial_respons= initial_request.execute()
				channel_id = initial_respons['items'][0]['id']				
				
				# to return the plalists of a channel using the channel id
				final_request = youtube.playlists().list(
					part="snippet,contentDetails",
					channelId= channel_id,
					maxResults=5
				)
				final_respons= final_request.execute()
				for item in final_respons['items']:
					published_title = item['snippet']['title']
					playlist_date = item['snippet']['publishedAt']
					description = item['snippet']['description']		
					playlist_id = item['id'] # playlist id to get all the videos in a playlist
					playlist_videos = get_video_titles_and_duration(get_videos_of_playlists(playlist_id)) # get the videos using the get_video_titles_and_duration funtion
					info_dict = {'published_title':published_title,'playlist date':playlist_date,'description':description, 'playlist_videos':playlist_videos}
					final_list.append(info_dict)
					
	# sort the final_list according to the playlist_date
	li = sorted(final_list, key=lambda i: i['playlist date'],reverse=True)
	return li


# to get all the videos in a playlist using the playlist id
def get_videos_of_playlists(playlist_id):
	video_id_list = []
	initial_request = youtube.playlistItems().list(
					part="contentDetails",
					playlistId=playlist_id,
					maxResults=5
	)
	initial_response = initial_request.execute()
	for item in initial_response['items']:
		video_id_list.append(item['contentDetails']['videoId'])
	return video_id_list  


# to get the video titles and duration
def get_video_titles_and_duration(video_ids):
	final_list = []

	# make the request for videos
	initial_request = youtube.videos().list(
					part="contentDetails,snippet",
					id = ','.join(video_ids)
	)
	initial_response = initial_request.execute()

	# get the content video title and duration
	for item in initial_response['items']:
		time_duration = item['contentDetails']['duration']

		# changing the format for time 
		mins_pattern = re.compile(r'(\d+)M')
		sec_pattern = re.compile(r'(\d+)S')
		minutes = mins_pattern.search(time_duration)
		seconds = sec_pattern.search(time_duration)
		final_min = minutes.group(1) if minutes else 0
		final_sec = seconds.group(1)  if seconds else 0
		final_time = str(final_min)+"mins "+str(final_sec)+"secs"

		title_duration_dict = {'title':item['snippet']['title'],'duration':final_time}
		final_list.append(title_duration_dict)
	return final_list


# saves the final_result to file.json
def save_to_file(final_result):
	with open('file1.json', "w+") as f:
		json.dump(final_result, f, indent = 2)

x =get_playlist()
save_to_file(x)