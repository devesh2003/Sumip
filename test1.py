from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from time import sleep

#url = "https://flight.yatra.com/air-search-ui/dom2/trigger?type=O&viewName=normal&flexi=0&noOfSegments=1&origin=%s&originCountry=IN&destination=%s&destinationCountry=IN&flight_depart_date=%s&ADT=1&CHD=0&INF=0&class=%s&source=fresco-home&version=1.88"%("BOM","DEL","25/06/2019","ECONOMY")
#print(url)
url = "https://flight.yatra.com/air-search-ui/dom2/trigger?ADT=1&CHD=0&INF=0&class=Economy&destination=DEL&destinationCountry=IN&flexi=0&flight_depart_date=23/06/2019&noOfSegments=1&origin=BOM&originCountry=IN&type=O&unique=796710131513&version=1.24&viewName=normal"

opts = Options()
opts.add_argument("--headless")
usr_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36"
opts.add_argument("user-agent=%s"%usr_agent)
driver = webdriver.Chrome(options=opts)
driver.get(url)
#print("[*]Connected")
resp = driver.execute_script("return document.documentElement.outerHTML")
# print(resp)

print(driver.find_element_by_xpath("(//div[@class='fr hidden-md']//p[@autom='booknow'])[2]").is_enabled())

driver.find_element_by_xpath("(//div[@class='fr hidden-md']//p[@autom='booknow'])[2]").click()
sleep(5)
s = driver.execute_script("return window.location.href")
print(s)

# soupss = BeautifulSoup(str(resp),'lxml')
# soups = soupss.find_all('div',class_="js-flightRow js-flightItem")