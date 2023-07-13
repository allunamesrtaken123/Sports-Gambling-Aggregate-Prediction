from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.error import HTTPError
from urllib.error import URLError
import re
from time import strftime



try:
    html = urlopen('https://www.betmonitor.com/odds-comparison/basketball/usa-wnba/washington-mystics-w-seattle-storm-w/106794772')
except HTTPError as e:
    print(e)
except URLError as e:
    print("Server couldn't be found")
else:
    print("It worked!")

# As a starter, let's get the names of the teams
bs = BeautifulSoup(html.read(),'html.parser')
teams = bs.find_all('div',{'class' : 'teams has-logo'})[0].get_text()
homeTeam = re.search(pattern = '[A-Za-z ]*[A-Za-z]',string= teams).group()
awayTeam = re.search(pattern = '(?<=— )[A-Za-z ]*[A-Za-z]+', string = teams).group()
print(homeTeam)
print(awayTeam)

# Now for the date of the game
date = bs.find_all('span',{'class' : 'evtime-switch','data-type' : 'event-header'})[0].get_text()
gameDate = re.search(pattern = '[A-Za-z0-9]* [A-Za-z]*, [0-9]*',string = date).group()
print(gameDate)

# Now the hard part, scraping the books
oddsDict = {}
odds = bs.find_all('div',{'class' : 'bookie-cont sortable'})
for o in odds:
    print(odds)
    print('*'*20)


from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
options = Options()
options.add_argument('--headless=new')
import time
options.add_argument("--headless=new")
driver = webdriver.Chrome(options = options) 
driver.get('https://www.betmonitor.com/odds-comparison') 
#time.sleep(3)
leagues = driver.find_elements(By.CLASS_NAME,"dark")
links = [el.get_attribute('href') for el in leagues]

league_links = [l for l in links if re.match(pattern = 'https://www.betmonitor.com/odds-comparison/[A-Za-z]+/[A-Za-z\-0-9]+/[0-9]{8}',string = l)]

#for l in league_links:
#    processLeague(l)  <-- This will update a GLOBAL dictionary thing
driver.close()


def processLeague(leagueLink : str):
    driver = webdriver.Chrome(options = options)
    driver.get(leagueLink)
    games = driver.find_elements(By.CLASS_NAME,"dark")
    gameLinks = [el.get_attribute('href') for el in games]
    goodGameLinks = [l for l in gameLinks if re.match(pattern = 'https://www.betmonitor.com/odds-comparison/[A-Za-z]+/[A-Za-z\-0-9]+/[A-Za-z0-9/-]+/[0-9]+',string = l)]
    processMatchup(goodGameLinks[0])
def processMatchup(matchupLink : str):
    print(matchupLink)
    driver = webdriver.Chrome(options = options)
    driver.get(matchupLink)
    #books = driver.find_elements(By.CLASS_NAME,'bookie-cont sortable')
    # This gives me the names of the books in the order they appear
    bookNames = [e.text for e in driver.find_elements(By.CLASS_NAME,'bookie')]
    # For home odds, I want to get all div elements with class name starting with bettype q1, then take 
    # the span elements of that div element that start with odd-decimal
    homeOddsElements = driver.find_elements(By.XPATH,"//div[contains(@class, 'bettype q1')]/span[contains(@class, 'odd-decimal')]")
    awayOddsElements = driver.find_elements(By.XPATH,"//div[contains(@class, 'bettype q2')]/span[contains(@class, 'odd-decimal')]")
    homeOdds = [e.text for e in homeOddsElements]
    awayOdds = [e.text for e in awayOddsElements]
    d = {bookNames[i] : {'home' : homeOdds[i], 'away' : awayOdds[i]} for i in range(len(bookNames))}
    for k in d:
        print(k,d[k])



    #print([e.text for e in bookNames])

processLeague(league_links[0])

"""
Next to do:

For each game, I want to get some summary data like the home team, away team, date/time of the competition, and 
date/time of the scrape. From there I need to format it so that it can go nicely into a pandas dataframe. Maybe I 
write it as a dictionary, append it to a list of dictionaries that I accumulate over the course of one run of the
sciprt, where the list is ultimately converted to a json file that is saved. I think for the NBA passing network 
project I was able to read all json files in a directory and combine them into a meaningful CSV. Those steps feel
like a good path to head down.
"""