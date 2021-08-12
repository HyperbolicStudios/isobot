import time
import traceback
from pbwrap import Pastebin
import json
from pastemyst import Client, Language, Paste, Pasty, ExpiresIn, EditType
import os
from replit import db
from inspect import getsourcefile
from os.path import abspath

def getToken(tokenName):

        #set active directory to app location
    directory = abspath(getsourcefile(lambda:0))
    #check if system uses forward or backslashes for writing directories
    if(directory.rfind("/") != -1):
        newDirectory = directory[:(directory.rfind("/")+1)]
    else:
        newDirectory = directory[:(directory.rfind("\\")+1)]
    os.chdir(newDirectory)

    f = open("tokens.json")
    data = json.load(f)
    return data[tokenName]

#Pastebin stuff to dump error data
def pasteData(text,persistence = "ONE_HOUR"):
  client = Client(key='')
  if(persistence == "ONE_DAY"):
    res4 = client.create_paste(Paste(pasties=[Pasty('ISO', text)], expires_in=ExpiresIn.ONE_DAY))
  else:
    res4 = client.create_paste(Paste(pasties=[Pasty('ISO', text)], expires_in=ExpiresIn.ONE_HOUR))
  return("https://paste.myst.rs/"+res4.id)
def getData(key):
  i = 0
  while(1):
    i=i+1
    if(2**i>64):
      return "failure"
    try:
      if(key == "delay"):
        return float(db[key])
      else:
        return(db[key])
    except KeyError:
      if key == "list_of_aliases":
        db[key] = {}
        return db[key]
      print("Database error: could not find value of _" + key + "_. Set value to 0.")
      updateData(key,"0")
    except: #Likely a rate-limiting error for repl.it database?
      traceback.print_exc()
      time.sleep(2**i)
      print("Exception caught. Will sleep for " + str(2**i) + " seconds and retry.")

def updateData(key, value):
    if(key=="delay"):
      db[key] = str(value)
    else:
      db[key] = value
    return
def listData():
  format = ("Stored data:\n")

  for key in db.keys():
    if(key.find("listofposts") == -1):
        format = format + key + ": " + str(db[key]) + "\n"
    else:
      format = format + "{}: {} items.\n".format(key,len(db[key]))
  return format
