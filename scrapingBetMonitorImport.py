import re
from time import strftime
from tqdm import tqdm
from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import os
from selsunpool import selenium_job, SeleniumPoolExecutor
options = Options()
options.add_argument('--headless=new')
options.add_argument("--headless=new")

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

def processSport(links : list):
    l = []
    for link in links:
        l.extend(processLeague(link))
    return l

def processLeague(leagueLink : str):
    bigList = []
    driver = webdriver.Chrome(options = options)
    driver.get(leagueLink)
    games = driver.find_elements(By.CLASS_NAME,"dark")
    gameLinks = [el.get_attribute('href') for el in games]
    goodGameLinks = [l for l in gameLinks if re.match(pattern = 'https://www.betmonitor.com/odds-comparison/[A-Za-z]+/[A-Za-z\-0-9]+/[A-Za-z0-9/-]+/[0-9]+',string = l)]
    for l in goodGameLinks:
        bigList.extend(processMatchup(l))
    return bigList

@selenium_job(webdriver_param_name = 'driver')
def processMatchup(matchupLink : str, driver):
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

def bookkeep(saveTo,sport,toSave):
    with open(f"{saveTo}/{sport}.csv",'a') as f:
        if os.path.getsize(f"{saveTo}/{sport}.csv") == 0:
            f.write('ScrapeDate,Tournament,Book,HomePlayer,HomeBEP,AwayPlayer,AwayBEP,Hold\n')
        for r in toSave:
            f.write(r)
    f.close()