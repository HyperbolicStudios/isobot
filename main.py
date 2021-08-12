import discord
import asyncio
import math
from discord.ext import tasks, commands
import datetime
import traceback
from updateData import getToken, getData, updateData, pasteData, listData
#OS/Directory
import os

from keep_alive import keep_alive
from iso import collectISO, wipeISO, updateISO, collectAllISOs

def cleanURL(URL):
    URL = URL[URL.find("hypixel.net"):]
    URL = URL[:URL.find("/page-")]
    URL = "https://" + URL.replace("https://", "") + "/"
    return(URL)

TOKEN = getToken("discord")

LIST_OF_CHANNELS = []

helpPage = """
**Assistance**:\n
**Functionality**\n
This bot does a few things: first, it stores in a database every post in games A, B, and C. Updates to the database are done every three hours, and typically takes under 10 minutes. Second, the bot collects posts and generates ISOs on command. The bot is also capable of generating ISOs for *all* players at once (if a mod wants to post links to every ISO at EoD, for instance) and can also generate ISOs restricted to page ranges. \n
      **Assistance and setup**\n 
      Note that the letter "X" in any command refers to the game you are analyzing - be it A, B, or C. (case-sensitive)\n
        `$iso help` - prints this help message\n
        `$iso info` - prints a summary of information stored in the databases, including URLs and number of posts stored. \n 
        `$isoX url <url>` - sets the URL of game X. \n
        `$isoX wipe` - wipes the stored posts of game X. Useful if there's been a screwup of some kind, such as the bot missing a page.\n 
        **Retrieving ISOs**\n 
        `$isoX <player name>` - generates a single ISO of player <player name> from game X exclusively. \n Link should persistent for one hour. 
        `$isoX <name> range:Y,Z` - generates a single ISO of player <player name> from game X, listing every post from page Y to page Z. Don't forget the comma. \n 
        `$isoX all` - posts links to ISOs of every single player in game X. Link should persist for one day.\n
        **Updating the database**
        By default, the databases are updated every three hours. The bot is unresponsive during updates.\n
        `$isoX updates on` - turns on the automatic updates\n 
        `$isoX updates off` - turns off the automatic updates \n 
        `$isoX update` - manually updates a database. Do *not* overuse this command.\n 
        
        **Channel visibilities**
        `$iso vis on` - gives read/write privileges to every discord user with the default role.\n 
        `$iso vis off` - removes read/write privileges for players that do not have special permissions.\n
        \n\n
        All messages must be entered in the <#{channel_id}> channel.
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

async def embedText(message,text):
  embed = discord.Embed()
  embed.color = 0x7727d9
  embed.description = text
  await message.channel.send(embed=embed)
  return

async def sendHelpMessage(message):
    channel_id = "#iso-bot"
    for channel in message.guild.channels:
      if(channel.name == channel_name):
        channel_id = str(channel.id)
    text = helpPage.format(channel_id = channel_id)
    await message.channel.send("**Votecount Bot " + getToken("name") + " help:**")
    await embedText(message,text)
    return

async def checkForData():
    await client.wait_until_ready()
    while not client.is_closed():
        delta = round((datetime.datetime.now()-datetime.datetime.fromisoformat(getData("last_time"))).total_seconds())
        print(delta)
        if ( delta > 3600*3):
            print("Updating ISO databases.")
            for gameLetter in ["A","B","C"]:
              if getData("updateStatuses")[["A","B","C"].index(gameLetter)] == "on":
                updateISO(gameLetter)
            print("Updated all ISO databases automatically.")
            updateData("last_time",datetime.datetime.now().isoformat())
        await asyncio.sleep(2)

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
  if message.channel.name == channel_name:
    if message.content == "$iso vis on":
      print("Turning vis on")
      guild = message.channel.guild
      for role in guild.roles:
          print(role.name)
          if role.is_default() == True:
              everyone = role
      print(everyone.name)
      try:
          await message.channel.set_permissions(everyone, read_messages=True,send_messages=True)
          await message.channel.send("Visibility on!")
      except:
          await message.channel.send(
              "Error. I might not have the right permissions; double-check the channel permissions.")
    elif message.content == "$iso vis off":
      print("Turning vis off")
      guild = message.channel.guild
      for role in guild.roles:
          print(role.name)
          if role.is_default() == True:
              everyone = role
      print(everyone.name)
      try:
          await message.channel.set_permissions(everyone, read_messages=False,send_messages=False)
          await message.channel.send("Visibility off. Goodbye!")
      except:
          await message.channel.send(
              "Error. I might not have the right permissions; double-check OAuth2.")
    elif message.content == "$iso ping":
      await message.channel.send("I'm still here!")

    if message.content == "$iso help":
      await sendHelpMessage(message)

    elif message.content[:9] in ["$isoA url","$isoB url","$isoC url"]:
      url = message.content[10:]
      updateData("URL"+message.content[4],cleanURL(url))
      await message.channel.send("Updated URL to " + cleanURL(url))

    elif message.content in ["$isoA update","$isoB update","$isoC update"]:
      await message.channel.send("Updating database of stored posts. This will take some time.")
      await message.channel.send(updateISO(message.content[4]))

    elif message.content in ["$isoA wipe","$isoB wipe","$isoC wipe"]:
      wipeISO(message.content[4])
      await update("ISOs for game {} wiped. Will rescrape at update time.".format(message.content[4]))
    
    elif message.content.find("range:") != -1 and message.content[:6] in ["$isoA ","$isoB ","$isoC "]:
      #$iso <player> range:x,y
      text = message.content
      lowerbound = int(text[text.find("range:")+6:text.find(",")])
      upperbound = int(text[text.find(",")+1:])
      playername = text[5:text.find("range:")-1].strip()
      await message.channel.send("Retrieving a ranged ISO.")
      await message.channel.send(collectISO(message.content[4],playername,lowerbound,upperbound))
    
    elif message.content == "$iso terminate 1":
      await message.channel.send("Bye bye!")
      await client.close()
    
    elif message.content == "$iso info":
      await embedText(message,listData())

    elif message.content[:6] in ["$isoA ","$isoB ","$isoC "] and message.content[6:] in ["updates on","updates off"]:
      updateStatuses = getData("updateStatuses")
      updateStatuses[["A","B","C"].index(message.content[4])] = message.content[-3:].strip()
      updateData("updateStatuses",updateStatuses)
      await message.channel.send("Updated auto-update status to {} for game {}.".format(message.content[-3:].strip(),message.content[4]))

    elif message.content in ["$isoA all","$isoB all","$ISOC all"]:
      await message.channel.send("Sorting ISOs for all players in game {}.".format(message.content[4]))
      await embedText(message,collectAllISOs(message.content[4]))
      await message.channel.send("Links expire in one day.")

    elif message.content[:6] in ["$isoA ","$isoB ","$isoC "]:
        await message.channel.send("Retrieving an ISO of " + message.content[6:])
        data = collectISO(message.content[4],message.content[6:])
        if data == "":
          await message.channel.send("Nothing found for '{}' in game {}.".format("message.content[6:]",message.content[4]))
        else:
          await message.channel.send(data)
    

client.loop.create_task(checkForData())
client.run(TOKEN)
