print("Starting bookie server")

import praw
import os
from datetime import datetime
import io
# import boto3
from boto3 import session
from boto3.s3.transfer import S3Transfer
import json
import string
import requests
import re

print("Imports worked")

tickerMatch = re.compile("(?:\s|^)(?:\$([A-Za-z]{1,5})|([A-Z]{2,5}))(?=(?:[\s.,?!]|$))")

tickerData = {}
comments = {}
buckets = [{}]
last_min = datetime.now().strftime("%M")
last_hour = datetime.now().strftime("%H")


# Initiate session
session = session.Session()
client = session.client('s3',
                        region_name='nyc3', #enter your own region_name
                        endpoint_url='https://nyc3.digitaloceanspaces.com', #enter your own endpoint url

                        aws_access_key_id=os.environ["SPACES_ACCESS"],
                        aws_secret_access_key=os.environ["SPACES_SECRET"])

print("Initialized s3 connection")

# Load reddit
reddit = praw.Reddit(
    client_id=os.environ["REDDIT_CLIENT_ID"],
    client_secret=os.environ["REDDIT_SECRET"],
    # password="PASSWORD",
    user_agent=os.environ["REDDIT_USER_AGENT"],
    # username="USERNAME",
)

print("Initialized reddit connection")

# returns a dict of key: ticker symbol value: symbol count, for th comment
def parseComment(comment: str):
    output = {}
    candidates = []
    for match in tickerMatch.finditer(comment):
        groups =  [*match.groups()]
        candidate = groups[0] if groups[0] else groups[1]
        if candidate in tickerData:
            if not candidate in output:
                output[candidate] = 1
            else:
                output[candidate] += 1
    return output

def getTickerData():
    tickerDict = {}
    payload = {'download': 'true'}
    headers = {'Accept': 'application/json', 'Accept-Encoding': 'gzip', 'User-Agent': 'Bookie'}
    r = requests.get('https://api.nasdaq.com/api/screener/stocks', params=payload, headers=headers)
    nasDat = r.json()
    for symbol in nasDat["data"]["rows"]:
        tickerDict[symbol["symbol"]] = symbol
    return tickerDict

tickerData = getTickerData()

print("Loaded NASDAQ data")

def createClientObject():
    today = buckets[0:23]
    aggregate = {}
    for bucket in today:
        for symbol in bucket:
            if not symbol in aggregate:
                aggregate[symbol] = {
                    "daily_mentions": 1,
                    "prev_daily_mentions": 0
                }
            else:
                aggregate[symbol]["daily_mentions"] += 1

    yesterday = buckets[24:47]
    for bucket in yesterday:
        for symbol in bucket:
            if not symbol in aggregate:
                aggregate[symbol] = {
                    "daily_mentions": 0,
                    "prev_daily_mentions": 1
                }
            else:
                aggregate[symbol]["prev_daily_mentions"] += 1

    for symbol in aggregate:
        if symbol in tickerData:
            aggregate[symbol]["last_sale"] = tickerData[symbol]["lastsale"]


    return aggregate

print("Running primary loop")

while(True):
    try:
        for comment in reddit.subreddit("wallstreetbets").stream.comments():
            print(comment)

            # Get the data from reddit
            rawComment = comment.body

            # comment de-dupe on reinitialize after error
            if (comment.id in comments):
                continue
            else:
                comments[comment.id] = True

            
            # process data
            mentioned = parseComment(rawComment)
            for key in mentioned:
                if not key in buckets[0]:
                    buckets[0][key] = 1
                else:
                    buckets[0][key] += 1

            # perform minute updates
            minstr = datetime.now().strftime("%M")
            if (minstr != last_min):
                last_min = minstr

                # pull new data every 5 minutes
                if (int(minstr) % 5 == 0):
                    tickerData = getTickerData()

                data = createClientObject()
                print(data)
                # upload to the space
                datastream = io.BytesIO(bytes(json.dumps(data), "ascii"))
                client.upload_fileobj(datastream, "ledger", "data.json", ExtraArgs={'ACL':'public-read'})


            # perform hour updates
            hourstr = datetime.now().strftime("%H")
            if (hourstr != last_hour): #an hour has passed since the last update
                last_hour = hourstr
                buckets.insert(0, {})
                if len(buckets) > 49:
                    buckets.pop()
    
    except KeyboardInterrupt:
        print("Quitting :)")
        break

    except:
        print("Unexpected error, retrying...")
