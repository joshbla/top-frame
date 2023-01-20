# Import the necessary libraries
import os
import random
import requests
import urllib.parse
from googleapiclient.discovery import build

# Set the API key for the YouTube Data API
API_KEY = 'YOUR_API_KEY'

# Build the YouTube Data API service
service = build('youtube', 'v3', developerKey=API_KEY)

# Retrieve the 100 most popular videos on YouTube
response = service.videos().list(
    part='id',
    chart='mostPopular',
    maxResults=100,
).execute()

# Create an empty list to store the video URLs
video_urls = []

# Loop through the list of videos
for video in response['items']:
    # Get the video ID
    video_id = video['id']

    # Get the video URL
    video_url = 'https://www.youtube.com/watch?v=' + video_id

    # Add the video URL to the list
    video_urls.append(video_url)

# Randomly choose a video URL from the list
video_url = random.choice(video_urls)

# Get the video duration
response = service.videos().list(
    part='contentDetails',
    id=video_id,
).execute()
video_duration = response['items'][0]['contentDetails']['duration']

# Parse the video duration into seconds
parsed_duration = urllib.parse.parse_duration(video_duration)
video_seconds = parsed_duration.total_seconds()

# Generate a random time in the video
random_time = random.uniform(0, video_seconds)

# Download the video from YouTube
video_filename = video_id + '.mp4'
urllib.request.urlretrieve(video_url, video_filename)

# Extract a frame from the video at the random time
frame_filename = video_id + '.jpg'
os.system('ffmpeg -ss ' + str(random_time) + ' -i ' + video_filename + ' -vframes 1 ' + frame_filename)

# Delete the downloaded video file
os.remove(video_filename)
