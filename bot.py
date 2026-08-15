from datetime import datetime
from time import sleep
import os
from dotenv import load_dotenv, dotenv_values 
import discord
import feedparser

load_dotenv() 

class MyClient(discord.Client): 
    async def on_ready(self): 
        channel = client.get_channel(os.getenv("channel_id"))
        NSFWchannel = client.get_channel(os.getenv("NSFW_channel_id"))
        
        for entry in entries:
            embedVar = discord.Embed(title=entry.title, color=0xFF5700, type='rich', url=entry.link, timestamp = datetime.strptime(entry.published, "%Y-%m-%dT%H:%M:%S+00:00"))
            embedVar.set_author(name=entry.author, url=entry.author_detail.href, icon_url=None)
            if "media_thumbnail" in entry.keys():
                embedVar.set_thumbnail(url=entry.media_thumbnail[0]["url"])
            if "NSFW" not in entry.title:
                await channel.send(embed=embedVar)
            else:
                await NSFWchannel.send(embed=embedVar)
            sleep(3)

d = feedparser.parse(os.getenv("reddit_rss"))

if os.path.exists("timestamp.txt"):
    with open("timestamp.txt") as f:
      dt = datetime.strptime(f.readline(), "%Y-%m-%dT%H:%M:%S+00:00")
else: 
    f = open("timestamp.txt", "x")
    dt = datetime.strptime(d.entries[2].published)

newdt = datetime.strptime(d.entries[0].published, "%Y-%m-%dT%H:%M:%S+00:00")

entries = []

for entry in d.entries:
    if datetime.strptime(entry.published, "%Y-%m-%dT%H:%M:%S+00:00") <= dt:
        break
    entries.insert(0, entry)
        
with open("timestamp.txt", "w") as f:
  f.write(d.entries[0].published)

intents = discord.Intents.default() 

client = MyClient(intents=intents) 

client.run(os.getenv(discord_bot_token))
