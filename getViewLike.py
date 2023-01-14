from bs4 import BeautifulSoup
import requests
import re
from math import floor

magnitudeDict={0:'', 1:'K', 2:'M', 3:'B'}
url = 'https://youtu.be/7nT7JGZMbtM'
r = requests.get(url)
s = BeautifulSoup(r.text, "html.parser")

def getView():
    #view
    viewrw = str(s)[str(s).find("viewCount"):str(s).find("viewCount")+40]
    vsplit = re.split('"', viewrw)
    view = vsplit[2]
    return(simplify(int(view)))

def getLike():
    #like
    like_text = '"defaultIcon":{"iconType":"LIKE"},"defaultText":{"accessibility":{"accessibilityData":{"label":'
    likerw = str(s)[str(s).find(like_text):str(s).find(like_text)+len(like_text)+40]
    lsplit = re.split('"', likerw)
    liketxt = lsplit[15]
    like = re.search("[\d,]+",liketxt)
    like = like.group()
    like = re.sub(",","",like)

    return(simplify(int(like)))

def simplify(num):
    num = floor(num)
    magnitude = 0
    while num >= 1000.0:
        magnitude += 1
        num = num/1000.0
    return(f'{floor(num*10.0)/10.0} {magnitudeDict[magnitude]}')