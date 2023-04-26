import os
import openai 
import tweepy 
from datetime import datetime  # for getting the current date and time
from apscheduler.schedulers.blocking import BlockingScheduler  # for adding delays
from src.prompts import get_random_prompt 
import requests
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.environ.get("OPENAI_KEY")
api_key = os.environ.get("TWITTER_KEY")
api_secret = os.environ.get("TWITTER_SECRET")
access_token = os.environ.get("TWITTER_ACCESS")
access_token_secret = os.environ.get("TWITTER_ACCESS_SECRET")
bearer_token = os.environ.get("TWITTER_BEARER")

output_file = open('tweets.txt', 'a')
client = tweepy.Client(bearer_token, api_key, api_secret, access_token, access_token_secret)

# Creating API instance. This is so we still have access to Twitter API V1 features
auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
api = tweepy.API(auth)

def generate_tweet(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    return response['choices'][0]['text']

def post_tweet():
    print("Posting tweet...")
    now = datetime.now()
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    prompt = get_random_prompt()
    text = generate_tweet(prompt)
    client.create_tweet(text=text)

    print("Posted tweet at: ", date_time)
    output_file.write('prompt: ' + prompt + ' date_time: ' + date_time)



# sched = BlockingScheduler()
# sched.add_job(post_tweet, 'interval', hours=12, jitter=7200)
# sched.start()
post_tweet()