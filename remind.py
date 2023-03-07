from datetime import datetime as dt
import time as t
from plyer import notification
import time
from twilio.rest import Client
import json
import os


print("REMINDER APP STARTING")

#get secret auth token things for the messaging
with open(r"stuf\actual projects\testreminder\twiliosecrets.json", 'r') as file:
    twiliosecrets = json.loads(file.read())
account_sid = twiliosecrets["account_sid"]
auth_token = twiliosecrets["auth_token"]
client = Client(account_sid, auth_token)

#get file path
folder = os.path.dirname(os.path.abspath(__file__))
eventFilePath = os.path.join(folder, "events.json")

#function to execute the reminding
def remind(event, mins, days=0,hours=0,seconds=0):
    if seconds==0:
        message = " happening now!"
    elif mins == 0:
        message = f" happening in {days} day(s) and {hours} hour(s)!"
    else:
        message = f" happening in {days} day(s) and {hours+1} hour(s)!"

        

    notification.notify(
        title=event,
        message=f"REMINDER: {event}{message}",
        timeout=10
    )

    message = client.messages .create(
                    body =  f"{event}{message}", #Message you send
                    from_ = "+18556720678",#Provided phone number
                    to =    "+19195949966")#Your phone number
    message.sid

    print(f"reminded for event {event}{message}")

#create a variable. why? no idea
global current

#while loop! so its always running ig
while True:
    
    #get events from the file that has events
    with open(eventFilePath, 'r') as file:
        events_dict = json.loads(file.read())

    #get current time
    now = dt.now()
    
    #for each event in the thing:
    #get time and make it a dt object, check if its within 7 days or 24 hours or if its right now and remind as needed
    for event, time_list in events_dict.items():

        time = dt(time_list[0],time_list[1],time_list[2],time_list[3],time_list[4],time_list[5],time_list[6])
        tdelta = time - now
        days = tdelta.days
        hours = tdelta.seconds//3600
        minutes = (tdelta.seconds//60)%60
        seconds = tdelta.seconds
        tseconds = round(tdelta.total_seconds())
        print(event, tseconds)
        

        # print("tdelta", tdelta)

        if tseconds == 0 or time == now:
            remind(event, minutes)
            print("now")        
            current = event
            break

        if tseconds<=0:
            current = event
            break
            

        elif (days<=7 and days>=0) and ((tseconds/3600)%24==0):
            remind(event,time_list[4], days,0,tseconds)
            print("days")

        elif days<1 and (hours<=24 and hours>=0) and tseconds%3600==0:
            remind(event,time_list[4], 0,hours,tseconds)
            print("hours")
        
        
        
        
    t.sleep(1)
    #if the event happened and the variable was assigned a thing then remove it
    #otherwise chill and continue!
    try:
        del events_dict[current]
        print("deleted ", current)
        events_string = str(events_dict)
        events_string = events_string.replace("\'", "\"")
        with open(eventFilePath, 'w') as file:
            file.write(events_string)
            file.close()
    except KeyError:
        continue
    except NameError:
        continue

    
