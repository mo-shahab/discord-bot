import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive
import praw
import joke_api

reddit = praw.Reddit(client_id="lUDAXZkTdOaNnkrscuartA",
                     client_secret="	OVOtecPikwaVyjQpF6Uplw5F-aNioQ",
                     username="Odd_Diamond_6600",
                     password="mohammedshahabuddinsoharwardi",
                     user_agent="pythonpraw")

client = discord.Client()

greetings = [
    "hello", "dont", "wanna do the thing", "yello", "oi", "yo", "yoi", "hai"
]

sad_words = [
    "sad", "depressed", "unhappy", "angry", "miserable", "chill dude dont be",
    "me too :("
]

starter_encouragements = [
    "Cheer up!", "Hang in there.", "You are a great person / bot!",
    "chill dude dont be", "lol but being depressed is bad", "me too :(",
    "take drugs", "ok so its not nice being sad and all",
    "you wanna do the thing",
    "lol dont worry everybody now is depressed, being depressed is normal for your generation ig",
    "trust me i dont know what to do"
]

cuss_words = ["fuck", "bitch"]

reply_to_cussing = [
    "oh listen here you little shit", "no bro not in the mood to fight you",
    "dont cuss or swear or i'll come to your house and strangle your neck with my own bot hands",
    "dont cuss as my master has forbidded me from both listening and saying such demeaning words",
    "fuck you too bitch", "lol says you get a life"
]

if "responding" not in db.keys():
    db["responding"] = True


def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]["q"] + " -" + json_data[0]["a"]
    return (quote)


'''
so i wrote this but i didnt work so i had to look up on the internet for this so yeah

def get_joke():
  f = "https://official-joke-api.appspot.com/random_ten"
  response = requests.get(f)
  joke = json.loads(response.text)
  return(joke)


'''






def update_encouragements(encouraging_message):
    if "encouragements" in db.keys():
        encouragements = db["encouragements"]
        encouragements.append(encouraging_message)
        db["encouragements"] = encouragements
    else:
        db["encouragements"] = [encouraging_message]


def delete_encouragment(index):
    encouragements = db["encouragements"]
    if len(encouragements) > index:
        del encouragements[index]
    db["encouragements"] = encouragements


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


@client.event
async def meme(ctx):
    subreddit = reddit.subreddit("memes")
    all_subs = []
    top = subreddit.top(limit=5)

    for submission in top:
        all_subs.append(submission)

    random_sub = random.choice(all_subs)

    name = random_sub.title
    url = random_sub.url

    em = discord.Embed(title=name)
    em.set_image(url=url)
    await ctx.send(embed=em)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content

    if msg.startswith("$hello"):
        await message.channel.send(random.choice(greetings))

    #here the bot inspires the shit outta you
    if msg.startswith("$inspire"):
        quote = get_quote()
        await message.channel.send(quote)

    #here the bot does the joke thingy
    if msg.startswith('$joke'):
      joke = joke_api.get_joke()

      if joke == False:
        await message.channel.send("Couldn't get joke from API. Try again later.")
      else:
        await message.channel.send(joke['setup'] + '\n' + joke['punchline'])
    
    #here is the meme thing i dont know if it will work
    if msg.startswith('$meme'):
      return meme()

    if db["responding"]:
        options = starter_encouragements
        if "encouragements" in db.keys():
            options = options + list(db["encouragements"])

        #this handles the sadness and all
        if any(word in msg for word in sad_words):
            await message.channel.send(random.choice(options))

        #this does the work for cussing and all
        if any(word in msg for word in cuss_words):
            await message.channel.send(random.choice(reply_to_cussing))

    if msg.startswith("$new"):
        encouraging_message = msg.split("$new ", 1)[1]
        update_encouragements(encouraging_message)
        await message.channel.send("New encouraging message added.")

    if msg.startswith("$del"):
        encouragements = []
        if "encouragements" in db.keys():
            index = int(msg.split("$del", 1)[1])
            delete_encouragment(index)
            encouragements = db["encouragements"]
        await message.channel.send(encouragements)

    if msg.startswith("$list"):
        encouragements = []
        if "encouragements" in db.keys():
            encouragements = db["encouragements"]
        await message.channel.send(encouragements)

    if msg.startswith("$responding"):
        value = msg.split("$responding ", 1)[1]

        if value.lower() == "true":
            db["responding"] = True
            await message.channel.send("Responding is on.")
        else:
            db["responding"] = False
            await message.channel.send("Responding is off.")


keep_alive()

my_secret = os.environ['TOKEN']
client.run(my_secret)
