from updateData import getData, updateData, pasteData
import requests
from bs4 import BeautifulSoup
import cloudscraper
import os
from inspect import getsourcefile
from os.path import abspath
import math
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

random.seed()

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(options=chrome_options)
#URL = "https://hypixel.net/threads/hypixel-mafia-l-died-carpe-jugulum-game-c-day-1.4439668"
    #set active directory to app location
directory = abspath(getsourcefile(lambda:0))
#check if system uses forward or backslashes for writing directories
if(directory.rfind("/") != -1):
    newDirectory = directory[:(directory.rfind("/")+1)]
else:
    newDirectory = directory[:(directory.rfind("\\")+1)]
os.chdir(newDirectory)

def getISO(URL,listofposts):
    firstpost = 1
    if listofposts != []:
        firstpost = listofposts[-1][1]+1 #firstpost that the bot should scrape
    class post: #object to store post data
        def __init__(self,user,number,text,id):
            self.user = user
            self.number = number
            self.text = text
            self.id = id
    scrapedPosts = [] #post objects stored here
    scraper = cloudscraper.create_scraper()

    page = math.ceil(firstpost/20.0)

    print("Starting at page " + str(page) + ". First post: " + str(firstpost))
    oldtag = 0
    while(page <= 1000): #the bot automatically ends at the end of thread; this is a failsafe
        print(page, end="   first post number: ")
        time.sleep(1.5+random.random())
        response = scraper.get(URL+"page-"+str(page)).text
       # driver.get(URL+"/page-"+str(page))
        #response = driver.page_source
        soup = BeautifulSoup(response, 'html.parser')

        firstpostnumber = int(soup.find("article",class_='message').find("ul", {"class": "message-attribution-opposite message-attribution-opposite--list"}).text.replace(",","").replace("\n","").replace("#","")) #first post number of the page
        print(firstpostnumber)
        if firstpostnumber == oldtag:
            print("Detected end of thread.")
            break
        oldtag = firstpostnumber

        for message in soup.find_all("article", class_='message'):
            for quote in (message.find_all("blockquote")):
                quote.clear()

            username = ((message.find(class_='username')).contents)[0].replace("\n","")
            postnumber = int(message.find("ul", {"class": "message-attribution-opposite message-attribution-opposite--list"}).text.replace("\n","").replace(",","").replace("#",""))
            text = (message.find(class_='bbWrapper')).get_text()
            postid = message.find("a",rel='nofollow')["href"]
            postid = int(postid[postid.find("post-")+5:])
          
            if postnumber >= firstpost:
                scrapedPosts.append(post(username,postnumber,text,postid))

        page = page+1

    for post in scrapedPosts: #when all posts are scraped, convert list of objects into list of lists
        listofposts.append([post.user,post.number,post.text,post.id])
    #driver.quit()
    return(listofposts)

def updateISO(gameLetter):
  gameLetter = gameLetter.upper()
  data = getISO(getData("URL"+gameLetter),getData("listofposts"+gameLetter))
  updateData("listofposts"+gameLetter,data)
  print("Game {} update complete. Database contains {} posts.".format(gameLetter,len(getData("listofposts"+gameLetter))))
  return("Update complete. Game {} database contains {} posts.".format(gameLetter,len(getData("listofposts"+gameLetter))))

def wipeISO(gameLetter):
  updateData("listofposts{}".format(gameLetter),[])
  print("Wiped ISO data for game {}.".format(gameLetter))
  return

def collectISO(gameLetter,player,lowerbound = -1,upperbound = 10000000):
  format = ""
  i = 0
  for post in getData("listofposts"+gameLetter):
    pageNumber = math.ceil(int(post[1])/20)
    if(post[0].lower() == player.lower() and pageNumber>=lowerbound and pageNumber <= upperbound):
      i = i+1
      format = format + """[QUOTE="{}, post: {}, member: 1"]{}[/QUOTE]\n""".format(post[0],post[3],post[2])
  
  return("Specified ISO of {} contains {} posts. The following link expires in an hour. Happy scumhunting! {}".format(player,i,pasteData(format)))

def collectAllPosts(gameLetter,lowerbound = -1, upperbound = 10000000):
  format = ""
  i = 0
  for post in getData("listofposts"+gameLetter):
    pageNumber = math.ceil(int(post[1])/20)
    if(pageNumber>=lowerbound and pageNumber <= upperbound):
      i = i+1
      format = format + """[QUOTE="{}, post: {}, member: 1"]{}[/QUOTE]\n""".format(post[0],post[1],post[2])
  return("Specified collection of posts contains {} posts. The following link expires in an hour. Happy scumhunting! {}".format(i,pasteData(format)))

def collectAllISOs(gameLetter,lowerbound = -1, upperbound = 1000000):
  gameLetter = gameLetter.upper()
  sortedISOs = {}
  for post in getData("listofposts"+gameLetter):
      if post[0] not in sortedISOs.keys():
        sortedISOs.update({post[0]:[post]})
      else:
        sortedISOs[post[0]].append(post)
  print("Sorted posts.")
  format = "List of collected ISOs: \n"
  for player in sortedISOs.keys():
      ISO = sortedISOs[player]
      format = format+"{}".format(ISO[0][0]) +": "
      quotes = ""
      for post in ISO:
          quotes = quotes + """[QUOTE="{}, post: {}, member: 1"]{}[/QUOTE]\n""".format(post[0],post[3],post[2])
      format = format + pasteData(quotes,"ONE_DAY") + "\n"
 
  return(format)

def printToFile():
  f = open("data.txt","a")
  for post in getData("listofposts"):
    f.write("{},{},{}".format(post[0],post[1],post[2]))
  f.close()

