import re
from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selsunpool import selenium_job, SeleniumPoolExecutor
from scrapingBetMonitorImport import processMatchup,bookkeep

options = Options()
options.add_argument('--headless=new')
options.add_argument("--headless=new")
driver = webdriver.Chrome(options = options) 
driver.get('https://www.betmonitor.com/odds-comparison') 


leagues = driver.find_elements(By.CLASS_NAME,"dark")
links = [el.get_attribute('href') for el in leagues]
tennisLeagueLinks = [l for l in links if re.match(pattern = 'https://www.betmonitor.com/odds-comparison/tennis/[A-Za-z\-0-9]+/[0-9]{8}',string = l)]

driver.close()


# I want the scraper to be fast, so I'm going to parallelize the collection of matchup links by processing the league links in parallel
# and then going through those collected links in parallel.

@selenium_job(webdriver_param_name='driver')
def getMatchups(url, driver):
    driver.get(url)
    games = driver.find_elements(By.CLASS_NAME, 'dark')
    gameLinks = [el.get_attribute('href') for el in games]
    return [l for l in gameLinks if re.match(pattern = 'https://www.betmonitor.com/odds-comparison/tennis/[A-Za-z\-0-9]+/[A-Za-z0-9/-]+/[0-9]+',string = l)]

tennisMatchupLinks = []
with SeleniumPoolExecutor(num_workers=len(tennisLeagueLinks), close_on_exit=True) as pool:
    pool.map_async(getMatchups, tennisLeagueLinks)
    for r in pool.job_results():
        tennisMatchupLinks.extend(r.result)

toSave = []
with SeleniumPoolExecutor(num_workers = len(tennisMatchupLinks), close_on_exit=True) as pool:
    pool.map_async(processMatchup, tennisMatchupLinks)
    for r in pool.job_results():
        toSave.extend(r.result)

bookkeep("/Users/aaronfoote/COURSES/Arbitrage Project",'tennis',toSave)