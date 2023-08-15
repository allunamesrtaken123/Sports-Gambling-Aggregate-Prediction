from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.error import HTTPError
from urllib.error import URLError
import re
from time import strftime
import datetime
from tqdm import tqdm



"""
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
"""


from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
options = Options()
options.add_argument('--headless=new')
options.add_argument("--headless=new")
driver = webdriver.Chrome(options = options) 
driver.get('https://www.betmonitor.com/odds-comparison') 
#time.sleep(3)
leagues = driver.find_elements(By.CLASS_NAME,"dark")
links = [el.get_attribute('href') for el in leagues]

league_links = [l for l in links if re.match(pattern = 'https://www.betmonitor.com/odds-comparison/[A-Za-z]+/[A-Za-z\-0-9]+/[0-9]{8}',string = l)]
tennisLinks = [l for l in links if re.match(pattern = 'https://www.betmonitor.com/odds-comparison/tennis/[A-Za-z\-0-9]+/[0-9]{8}',string = l)]

#for l in league_links:
#    processLeague(l)  <-- This will update a GLOBAL dictionary thing
driver.close()

def toBEP(decimalOdds):
    '''
    converts the decimal odds to breakeven percentages
    '''
    return 1/float(decimalOdds)
def calculateHold(game):
    '''
    calculateHold(game) = the hold that the sportsbook has on game
    '''
    return str(sum([toBEP(odds) for odds in game.values()]) - 1)


def processLeague(leagueLink : str, saveTo : str):
    bigList = []
    driver = webdriver.Chrome(options = options)
    driver.get(leagueLink)
    games = driver.find_elements(By.CLASS_NAME,"dark")
    gameLinks = [el.get_attribute('href') for el in games]
    goodGameLinks = [l for l in gameLinks if re.match(pattern = 'https://www.betmonitor.com/odds-comparison/[A-Za-z]+/[A-Za-z\-0-9]+/[A-Za-z0-9/-]+/[0-9]+',string = l)]
    for l in tqdm(goodGameLinks):
        bigList.extend(processMatchup(l))
    with open(f"{saveTo}/TennisScrapes.csv",'a') as f:
        f.write('ScrapeDate,Tournament,Book,HomePlayer,HomeBEP,AwayPlayer,AwayBEP,Hold\n')
        for r in bigList:
            f.write(r)
    f.close()

def processMatchup(matchupLink : str):
    matchupList = []
    driver = webdriver.Chrome(options = options)
    driver.get(matchupLink)
    #books = driver.find_elements(By.CLASS_NAME,'bookie-cont sortable')
    # This gives me the names of the books in the order they appear
    teams = [e.text for e in driver.find_elements(By.CLASS_NAME,'teams')][0]
    homeTeam = re.search(pattern = '[A-Za-z ]*[A-Za-z]',string= teams).group()
    awayTeam = re.search(pattern = '(?<=— )[A-Za-z ]*[A-Za-z]+', string = teams).group()
    timeOfScrape = strftime("%m/%d/%Y %H:%M")
    league = driver.find_element(By.CLASS_NAME,'bc-league').text
    #dateOfMatch = [e.text for e in driver.find_elements(By.CLASS_NAME,'evtime-switch')]
    #print(f'Date of Match: {datetime.datetime.strptime(dateOfMatch,"").strftime("%m/%d/%Y %H:%M")}')
    bookNames = [e.text for e in driver.find_elements(By.CLASS_NAME,'bookie')]
    # For home odds, I want to get all div elements with class name starting with bettype q1, then take 
    # the span elements of that div element that start with odd-decimal
    homeOddsElements = driver.find_elements(By.XPATH,"//div[contains(@class, 'bettype q1')]/span[contains(@class, 'odd-decimal')]")
    awayOddsElements = driver.find_elements(By.XPATH,"//div[contains(@class, 'bettype q2')]/span[contains(@class, 'odd-decimal')]")
    homeOdds = [e.text for e in homeOddsElements]
    awayOdds = [e.text for e in awayOddsElements]
    for i in range(len(bookNames)):
        matchupList.append(",".join([timeOfScrape,league,bookNames[i],homeTeam,str(toBEP(homeOdds[i])),awayTeam,str(toBEP(awayOdds[i])),calculateHold({'home' : homeOdds[i], 'away' : awayOdds[i]}),'\n']))
    return matchupList


processLeague(tennisLinks[0], "/Users/aaronfoote/COURSES/Arbitrage Project")


"""
Next to do:

For each game, I want to get some summary data like the home team, away team, date/time of the competition, and 
date/time of the scrape. From there I need to format it so that it can go nicely into a pandas dataframe. Maybe I 
write it as a dictionary, append it to a list of dictionaries that I accumulate over the course of one run of the
sciprt, where the list is ultimately converted to a json file that is saved. I think for the NBA passing network 
project I was able to read all json files in a directory and combine them into a meaningful CSV. Those steps feel
like a good path to head down.

Right now I only want to look at games with no draws so I'm going to filter out links that are soccer (football)

With so many sportsbooks, I think arbitrage betting could be a really powerful technique. Especially because I have
such a large attack surface at so many books. It would be interesting to do some analytics on where aribtrage
opportunities present themselves the most, which present the biggest, and how the proximity to gametime affects
the presence of arbitrage opportunities. To do a project on that, I'd need to set up a serious scraping infrastructure.

I think I'd like to start off with tennis since it is played year-round, doesn't get a lot of volume (so maybe I could
do data analysis on real bets to place), and is interesting to me. If I'm scraping, I want to have the two players playing,
the tournament, and the date/time of the match. Making a unique identifier is tough but once I have those columns I can do 
that in R. I think I'll have each sportsbook listing as a row so in each row I'll have the sportsbook, the home
"""