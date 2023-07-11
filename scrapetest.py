
from urllib.request import urlopen
from bs4 import BeautifulSoup

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


"""


WRITE LOTS OF FUNCTIONS TO ROBUSTLY HANDLE EXCEPTIONS PLUS MAKE CODE MORE READABLE



"""
html = urlopen('http://www.pythonscraping.com/pages/warandpeace.html')
bs = BeautifulSoup(html.read(),'html.parser')
nameList = bs.findAll('span',{'class' : 'green'})
for name in nameList:
    # get_text() should be the last thing you do (before printing/storing). Preserve the tag structure as long as possible
    print(name.get_text())

html = urlopen("http://www.pythonscraping.com/pages/page3.html")
bs = BeautifulSoup(html,"html.parser")

#for child in bs.find('table',{'id' : 'giftList'}).children:
#    print(child)

for sibling in bs.find('table',{'id' : 'giftList'}).tr.next_siblings:
    print(sibling)