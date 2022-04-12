from googleapiclient.discovery import build
from dotenv import load_dotenv
import os

load_dotenv()

youtube = build('youtube','v3', developerKey = os.getenv('api_key'))

request = youtube.channels().list(
            part = 'statistics',
            forUsername = 'sentdex'
)

respons= request.execute()

print(respons)