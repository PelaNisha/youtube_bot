from urllib import response
from aiohttp import request
from googleapiclient.discovery import build
from dotenv import load_dotenv
import os
import json
import requests

load_dotenv()

youtube = build('youtube','v3', developerKey = os.getenv('api_key'))

initial_request = youtube.channels().list(
            part = 'contentDetails, statistics',
            forUsername = 'sentdex'
)

initial_respons= initial_request.execute()

channel_id = initial_respons['items'][0]['id']
total_videos = initial_respons['items'][0]['statistics']['videoCount']
print(channel_id,total_videos)
## display the most popular videos, titles and view count

video_ids = youtube.activities().list(
            part = 'contentDetails',
           channelId= channel_id
)

video_ids_respons= video_ids.execute()
# print(video_ids_respons)
with open('file.json', "w+") as f:
	json.dump(video_ids_respons, f, indent = 2)

# # print(video_ids)
# video_request = youtube.videos().list(
#         part="snippet,contentDetails,statistics",
#         id="Ks-_Mh1QhMc"
# )
# video_respons= video_request.execute()
# print(video_respons)


# # most popular videos according to a regiom
        
# video_popular_request = youtube.videos().list(
#        part="contentDetails,statistics",
#         chart="mostPopular",
#         regionCode="US"
# )
# video_popular_respons= video_popular_request.execute()


# getting commments
request = youtube.comments().list(
        part="snippet",
        parentId="UgzDE2tasfmrYLyNkGt4AaABAg"
    )
comment_response = request.execute()

print(comment_response)
with open('file.json', "w+") as f:
	json.dump(comment_response, f, indent = 2)
