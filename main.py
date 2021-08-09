import discord
import asyncio
import math
from discord.ext import tasks, commands
import datetime
import traceback
from updateData import getToken, getData, updateData, pasteData
#OS/Directory
import os

from keep_alive import keep_alive
from iso import collectISO, wipeISO, updateISO

TOKEN = getToken("discord")

LIST_OF_CHANNELS = []

helpPage = """
**Assistance**:\n
        `$iso help' - prints this help message
        \n\n
        All messages must be entered in the {channel_id} channel.
        """
client = discord.Client()
channel_name = "iso-bot"


async def update(text):
    print(LIST_OF_CHANNELS)
    for CHANNEL in LIST_OF_CHANNELS:
        try:
            channel = client.get_channel(int(CHANNEL))
            await channel.send(text)
        except:
            traceback.print_exc()


async def updateStatus(status):
    game = discord.Game(status)
    await client.change_presence(status=discord.Status.online, activity=game)

async def sendHelpMessage(message):
    embed = discord.Embed()
    embed.color = 0x46848c
    channel_id = "#iso-bot"
    for channel in message.guild.channels:
      if(channel.name == channel_name):
        channel_id = str(channel.id)
    embed.description = helpPage.format(channel_id = channel_id)
    await message.channel.send("**Votecount Bot " + getToken("name") + " help:**")
    await message.channel.send(embed=embed)

async def checkForData():
    await client.wait_until_ready()
    while not client.is_closed():
        updateISO()
        print("Updated ISO automatically.")
        await asyncio.sleep(60*30)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    keep_alive()
    # LIST_OF_CHANNELS = []
    guilds = client.guilds
    for guild in guilds:
        for channel in guild.channels:
            if (channel.name.lower() == channel_name
                and (not (channel.id in LIST_OF_CHANNELS))):
                LIST_OF_CHANNELS.append(channel.id)
                print(guild.name + ": " + channel.name + ": " +
                      str(channel.id))

    print(LIST_OF_CHANNELS)
    print('------')

    await updateStatus("$iso help")
    await client.change_presence(status=discord.Status.online)
    #await update("Bot restarted. AutoVC currently set to " + getData("status") + ".")
    #updateData("status","off")


@client.event
async def on_message(message):
  if message.content == "$iso help":
    await sendHelpMessage(message)
  elif message.content.find("$iso url") == 0:
    url = message.content[7:]
    updateData("URL",url)
    await message.channel.send("Updated URL to " + url)
  elif message.content == "$iso update":
    await message.channel.send("Updating database of stored posts. This will take some time.")
    updateISO()
    await message.channel.send("Update complete.")
  elif message.content == "$iso wipe":
    wipeISO()
    await update("ISOs wiped. Will rescrape at update time.")
  elif message.content.find("range:") != -1:
    #$iso <player> range:x,y
    text = message.content
    lowerbound = int(text[text.find("range:")+6:text.find(",")])
    upperbound = int(text[text.find(",")+1:])
    playername = text[5:text.find("range:")-1].strip()
    await message.channel.send("Retrieving an ranged ISO.")
    await message.channel.send(collectISO(playername,lowerbound,upperbound))
  elif message.content.find("$iso ") == 0:
    if (1):
      await message.channel.send("Retrieving an ISO of " + message.content[5:])
      await message.channel.send(collectISO(message.content[5:]))
    else:
      await message.channel.send("Player not found.")
client.loop.create_task(checkForData())
client.run(TOKEN)
