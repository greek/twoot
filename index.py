import tweepy
import random
import time
import json
import webbrowser
import string
from utils import decorators

f = open("config.json")
data = json.load(f)

api_key = data["api_key"]
api_secret = data["api_secret"]

auth = tweepy.OAuthHandler(api_key, api_secret)
api = tweepy.API(auth)


def startup():
    print("Welcome to the multi-tweeter bot! What do you want to do?")
    selector = input("select: ")
    if selector == "tweet":
        tweet()
    if selector == "loop":
        tweetLoop()
    if selector == "to":
        tweetTo()
    if selector == "many":
        replyToAsManyAsPossible()
    if selector == "latest":
        replyToLatest()

@decorators.toStartup
def tweet():
    phrase = input("Say... ")
    try:
        api.update_status(phrase)
        print("done. tweeted " + phrase)
    except:
        print("The status is a dupe, try again.")

def tweetLoop():
    phrase = input("Say... ")

    while True:
      api.update_status(random.choice(string.punctuation) + phrase + random.choice(string.punctuation))
      print(f"tweeted {phrase}")
      time.sleep(60) # 1 min timer

@decorators.toStartup
def tweetTo():
    print("whats the handle?")
    handle = input()

    if not handle:
        print("What? Try again...")
        handle = input()

    print(handle.strip('@') + " ...good choice")
    print("what do you wanna say?")
    phrase = input()

    if not phrase:
        print("You didn't say anything. Try again")
        phrase = input()
        return

    api.update_status("@{} ".format(handle) + phrase)
    print("Posted! Check your replies")

@decorators.toStartup
def tweetToLatest():
    print("whats the handle?")
    handle = input()

    if not handle:
        print("What? Try again...")
        handle = input()

    print(handle.strip('@'), "...good choice")
    print("what do you wanna say?")
    phrase = input()

    if not phrase:
        print("You didn't say anything. Try again")
        phrase = input()

    tweets = api.user_timeline(screen_name="{}".format(handle))
    tweet0 = tweets[0]
    api.update_status("@{}".format(handle) + " {}".format(phrase), tweet0.id)

@decorators.toStartup
def replyToLatest():
    handle = input("Listen to... ")
    phrase = input("Say... ")

    tweets = api.user_timeline(screen_name="{}".format(handle))
    tweet0 = tweets[0]
    for tweet0 in tweets:
        api.update_status("@{} ".format(handle) + phrase, tweet0.id)
        print("This will reply \"{}\" every three hours on the most latest tweet.".format(phrase))
        time.sleep(1080020) # Sleep for 3 hours to prevent ratelimiting.

@decorators.toStartup
def replyToAsManyAsPossible():
    handle = input("Listen to... ")
    phrase = input("Say... ")

    tweets = api.user_timeline(screen_name="{}".format(handle))
    tweet0 = tweets
    for tweet0 in tweets:
        api.update_status("@{} ".format(handle) + phrase, tweet0.id)
        print("This will reply \"{}\" every three hours on the most latest tweet.".format(phrase))
        time.sleep(8) # Sleep for 3 hours to prevent ratelimiting.

def main():
    # initalize auth
    webbrowser.open_new_tab(auth.get_authorization_url())
    authtoken = input("what's the magic code? ")
    auth.get_access_token(str(authtoken))

    startup()

if __name__ == "__main__":
    main()
