import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

opts = Options()
opts.add_argument("--headless")
usr_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36"
opts.add_argument("user-agent=%s"%usr_agent)

url = "https://flight.yatra.com/air-search-ui/dom2/trigger?type=O&viewName=normal&flexi=0&noOfSegments=1&origin=BOM&originCountry=IN&destination=DEL&destinationCountry=IN&flight_depart_date=22/06/2019&ADT=1&CHD=0&INF=0&class=Economy&source=fresco-home&version=1.88"

driver = webdriver.Chrome(options=opts)
driver.get(url)
print("[*]Connected")
resp = driver.execute_script("return document.documentElement.outerHTML")

soupss = BeautifulSoup(str(resp),'lxml')
soups = soupss.find_all('div',class_="js-flightRow js-flightItem")

for soup in soups:
    airline = soup.article.div.ul.li.div.small.text
    flight_num = soup.article.div.ul.li.div.find('small',class_="fs-10 ltr-gray fl ml5 nowrap").text
    start_time = soup.article.div.ul.find("li",class_="timing").div.span.text
    end_time = soup.article.div.ul.find("li",class_="timing").find('div',class_="end").span.text
    duration = soup.article.div.ul.find("li",class_="timing").find('div',class_="time").span.text
    flight_type = soup.article.div.ul.find("li",class_="timing").find('div',class_="time").small.text
    price = soup.article.div.ul.find("li",class_="price").find('div',class_="full").find('div',class_="btn-free-ui").find('p',class_="tfare fr").label.find('span',class_="bold").text

    main = ""
    main += 'Airline : %s\n'%airline
    main += 'Flight Number : %s\n'%flight_num

    print(main)

    
 #   print(str(soup.article.div.ul.find("li",class_="price").find('div',class_="full").find('div',class_="btn-free-ui").find('p',class_="tfare fr").label.find('span',class_="bold").text))

driver.quit()
