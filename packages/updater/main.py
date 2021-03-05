import time
import praw
import os
import io
# import boto3
from boto3 import session
from boto3.s3.transfer import S3Transfer
import json
import requests

# from botocore.client import Config

example_data = {
  "GME": {
    "prev_daily_mentions": 200,
    "daily_mentions": 300,
    "weekly_mentions": 999,
    "p*rev_weekly_mentions": 1
  },
  "AMZN": {
    "prev_daily_mentions": 0,
    "daily_mentions": 2,
    "weekly_mentions": 69,
    "prev_weekly_mentions": 420
  },
  "TSLA": {
    "prev_daily_mentions": 123,
    "daily_mentions": 420,
    "weekly_mentions": 69420,
    "prev_weekly_mentions": 1
  }
}

# Initiate session
session = session.Session()
client = session.client('s3',
                        region_name='nyc3', #enter your own region_name
                        endpoint_url='https://nyc3.digitaloceanspaces.com', #enter your own endpoint url

                        aws_access_key_id=os.environ["SPACES_ACCESS"],
                        aws_secret_access_key=os.environ["SPACES_SECRET"])


datastream = io.BytesIO(bytes(json.dumps(example_data), "ascii"))

client.upload_fileobj(datastream, "ledger", "data.json")

while True:
    # params = {
    #     "subreddit": "wallstreetbets",
    #     # "after": int(time.time() - 3600)
    # }
    # # params = {}
    # r = requests.get("https://api.pushshift.io/reddit/comment/search", params)
    
    # print("response", r.text)

    time.sleep(60) # Wait an hour

print("script finished")
