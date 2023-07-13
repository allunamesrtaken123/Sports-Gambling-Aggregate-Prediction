
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import datetime
import random
"""
html = urlopen('http://pythonscraping.com/pages/page1.html')

# First argument is the HTML itself, second is the parser you want BS to use
bs = BeautifulSoup(html.read(),'html.parser')
print(bs.h1)


# HTML can go bad and if you're automating something it's really foolish/poor practice to not catch exceptions

from urllib.error import HTTPError
from urllib.error import URLError

try:
    html = urlopen('https://pythonscrapingthisurldoesnotexist.com')
except HTTPError as e:
    print(e)
except URLError as e:
    print("Server couldn't be found")
else:
    print("It worked!")


# Every time you access a tag in a BeautifulSoup object you should add a check to make sure the tag actually exists
try:
    badContent = bs.nonExistingTag.anotherTag
except AttributeError as e:
    print('Tag not found')
else:
    if badContent == None:
        print("Tag Not Found!")
    else:
        print(badContent)


# Putting it together:
def getTitle(url):
    try:
        html = urlopen(url)
    except HTTPError as e:
        return None
    try:
        bs = BeautifulSoup(html.read(),'html.parser')
        title = bs.body.h1
    except AttributeError as e:
        return None
    return title

title = getTitle('http://www.pythonscraping.com/pages/page1.html')
if title == None:
    print("Title not found")
else:
    print(title)





WRITE LOTS OF FUNCTIONS TO ROBUSTLY HANDLE EXCEPTIONS PLUS MAKE CODE MORE READABLE




html = urlopen('http://www.pythonscraping.com/pages/warandpeace.html')
bs = BeautifulSoup(html.read(),'html.parser')
nameList = bs.findAll('span',{'class' : 'green'})
for name in nameList:
    # get_text() should be the last thing you do (before printing/storing). Preserve the tag structure as long as possible
    #print(name.get_text())
    pass

html = urlopen("http://www.pythonscraping.com/pages/page3.html")
bs = BeautifulSoup(html,"html.parser")

#for child in bs.find('table',{'id' : 'giftList'}).children:
#    print(child)

for sibling in bs.find('table',{'id' : 'giftList'}).tr.next_siblings:
    # This will skip the first tr element, which is useful if you want to scrape a table and the first row of the table
    # is a header/title
    #print(sibling)
    pass

html = urlopen('http://en.wikipedia.org/wiki/Kevin_Bacon')
bs = BeautifulSoup(html, 'html.parser')
for link in bs.find('div', {'id' : 'bodyContent'}).find_all('a',href = re.compile('^(/wiki/)((?!:).)*$')):
    if 'href' in link.attrs:
        print(link.attrs['href'])

random.seed(datetime.datetime.now())
def getLinks(articleUrl):
    html = urlopen(f'http://en.wikipedia.org{articleUrl}')
    bs = BeautifulSoup(html,'html.parser')
    return bs.find('div',{'id':'bodyContent'}).find_all('a',href = re.compile('^(/wiki/)((?!:).)*$'))
links = getLinks('/wiki/Kevin_Bacon')
while len(links) > 0:
    newArticle = links[random.randint(0,len(links) - 1)].attrs['href']
    print(newArticle)
    links = getLinks(newArticle)
"""



from selenium import webdriver 
from selenium.webdriver.common.by import By
import time
driver = webdriver.Chrome() 
driver.get('http://pythonscraping.com/pages/javascript/ajaxDemo.html') 
time.sleep(3)
print(driver.find_element(By.ID,"content").text)
driver.close()