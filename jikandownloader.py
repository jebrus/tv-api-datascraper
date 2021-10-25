from jikanpy import Jikan
import sys
import json
import time

stdoutstorer = sys.stdout

#in hindsight this is a terrible way to do this, but i wanted to mess around with reassigning stdout

def printLog(*args, **kwargs): #prints to console
    sys.stdout = stdoutstorer
    print(*args, **kwargs)

def printFile(*args, **kwargs): #prints to file
    sys.stdout = open('birthdaysandratings.txt',
                      'a')  # changes system stdout to be the file birthdaysandratings.txt, w signifies that we'll write to it
    print(*args, **kwargs)

printLog('printLog initialized')

printFile("username, birthday, rating") #adding headers to file
jikan = Jikan()
time_num = 10 #how long we wait between each API call
for page_index in range(87, -1, -1): #loops through each page we can pull w/ the API (capped at 101 pages) and pulls the data
    printLog('Initializing Database #' + str(page_index) + "...")
    with open("USERDUMP_" + str(page_index) + ".json", "w") as write_file: #dumps 75 user ratings into json file
        json.dump(jikan.anime(11757, extension='userupdates', page=page_index), write_file, indent=4)
    printLog('Database #' + str(page_index) + ' initialized')
    printLog('Beginning Database #' + str(page_index) + ' read...')
    with open("USERDUMP_" + str(page_index) + ".json", "r") as read_file: #reads json file
        userdata = json.load(read_file)
    printLog("Now reading from Database #" + str(page_index))
    time.sleep(time_num)
    for users in userdata["users"]: #loops through each review, pulls user rating, username, and birthday, and stores them
        try:
            user_prof = jikan.user(users["username"], request="profile")
            username = str(user_prof["username"])
            birthday = str(user_prof["birthday"])
            score = str(users["score"])
            if (not birthday == "None") and (not birthday == "") and (not score == "") and (not score == "None"):
                printFile(username + "," + birthday + "," + score)
                printLog("Logged user " + username + " with birthday " + birthday + " and score " + score)
            else:
                printLog("User " + username + " not logged, birthday: " + birthday + ", score: " + score)
        except Exception:
            printLog(users["username"] + " not logged, API issue")
        time.sleep(time_num)

printLog("Logging complete!")
