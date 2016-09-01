import re
import sys
import os
import platform
import time
from selenium import webdriver
from collections import OrderedDict
from pytube import YouTube

platformType = platform.system()

print("Please enter a youtube playlist link")
playListLink = input()

isValid = re.findall("www.youtube.com/(playlist)\?", playListLink)

if len(isValid) == 0:
    sys.exit(1)

browser = webdriver.Firefox()

browser.get(playListLink)


endOfPlayList = False

while endOfPlayList == False:
    try:
        browser.find_element_by_xpath('//*[@id="pl-video-list"]/button').click()
        time.sleep(3)

    except:
        endOfPlayList = True

htmlSource = browser.page_source
browser.close()

encoded_str = str.encode(htmlSource)
decoded_str = encoded_str.decode('utf-8')
#decoded_str = encoded_str.decode('utf-8')

getTitle = re.findall('<title>  (.*?)\n', decoded_str, re.DOTALL)

encoded_title = getTitle[0].encode('utf-8')
decoded_title = encoded_title.decode('utf-8')

directorySafeName = decoded_title
directorySafeName = directorySafeName.replace("/", "")
directorySafeName = directorySafeName.replace(":", "")
directorySafeName = directorySafeName.replace("?", "")
directorySafeName = directorySafeName.replace("+", "")
directorySafeName = directorySafeName.replace("\"", "'")
directorySafeName = directorySafeName.replace("\'", "'")
directorySafeName = directorySafeName.replace("\\'", "'")
directorySafeName = directorySafeName.replace("\\", "")
directorySafeName = directorySafeName.replace("%", "")
directorySafeName = directorySafeName.replace("<", "")   
directorySafeName = directorySafeName.replace(">", "")


currentDirectory = os.getcwd()

#directory code
if platformType == 'Windows':
    currentDirectory = currentDirectory + "\\" + directorySafeName + "\\"
        
else:
    currentDirectory = currentDirectory + "/" + directorySafeName + "/"

FolderExists = os.path.isdir(currentDirectory)
    
if FolderExists:
    pass
else:
    os.makedirs(currentDirectory)

os.chdir(currentDirectory)

getYouTubeLinks = re.findall('data-video-id="(.*?)"', decoded_str)
list(OrderedDict.fromkeys(getYouTubeLinks))

newTempList = []
for i in range(len(getYouTubeLinks)):
    if getYouTubeLinks[i] not in newTempList:
        newTempList.append(getYouTubeLinks[i])

getYouTubeLinks = newTempList
#getYouTubeLinks = list(set(getYouTubeLinks))

filesAlreadyDownloaded = os.listdir(currentDirectory)

print("Downloading...")

for i in range(len(getYouTubeLinks)):

    ageRestricted = False

    try:
        yt = YouTube("http://www.youtube.com/watch?v=" + getYouTubeLinks[i])

    except:
        print ("Age Restricted Video, unable to download without signing in")
        ageRestricted = True


    if ageRestricted == False:
        if yt.filename + ".mp4" in filesAlreadyDownloaded:
            print ("Skipping Video - ", end=''),

            try:
                print(yt.filename)

            except:
                print ("")

        else:
            try:
                print(yt.filename)

            except:
                print ("WARNING: Video name not ASCII! Still Downloading.")

            findHighestRes = str(yt.filter('mp4')[-1])
            getResolution = re.findall("\(.mp4\) - (.*?) -" , findHighestRes)

            video = yt.get('mp4', getResolution[0])
            video.download(".")