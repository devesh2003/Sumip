from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from time import sleep
import string

class SearchYatra():
    def __init__(self,from_,to_,date,class_="Economy"):
        self.time = []
        self.links = []
        self.airline = []
        self.flight_num = []
        self.start_time = []
        self.end_time = []
        self.duration = []
        self.flight_type = []
        self.price = []
        self.date = date
        self.class_ = class_
        self.from_ = from_
        self.dest = to_

    def get_link(self,num,first):
        if first == True:
            # self.driver.find_element_by_xpath("(//div[@class='fr hidden-md']//p[@autom='booknow'])[%d]"%(num)).click()
            self.driver.find_element_by_xpath("(//div[@class='pr tipsy mb-8 book-button i-b ml-5 v-aligm-m']//button[@autom='booknow'])[%d]"%(num)).click()
            sleep(5)
            return str(self.driver.execute_script("return document.location.href"))
        elif first == False:
            # opts = Options()
            # opts.add_argument("--headless")
            # usr_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36"
            # opts.add_argument("user-agent=%s"%usr_agent)
            # self.driver = webdriver.Chrome(options=opts)
            self.driver.get(self.url)
            print(str(self.driver.execute_script("return document.location.href")))
            self.driver.find_element_by_xpath("(//div[@class='pr tipsy mb-8 book-button i-b ml-5 v-aligm-m']//button[@autom='booknow'])[%d]"%(num)).click()
            sleep(2)
            return str(self.driver.execute_script("return document.location.href"))

        self.driver = self.driverWeb

    def search(self):
        url = "https://flight.yatra.com/air-search-ui/dom2/trigger?type=O&viewName=normal&flexi=0&noOfSegments=1&origin=%s&originCountry=IN&destination=%s&destinationCountry=IN&flight_depart_date=%s&ADT=1&CHD=0&INF=0&class=%s&source=fresco-home&version=1.88"%(self.from_,self.dest,self.date,self.class_)
        #print(url)
        self.url = url
        opts = Options()
        opts.add_argument("--headless")
        usr_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36"
        opts.add_argument("user-agent=%s"%usr_agent)
        opts.add_argument("--debug=False")
        self.driverWeb = webdriver.Firefox(options=opts)
        self.driverWeb.get(url)

        self.driver = self.driverWeb

        #print("[*]Connected")
        resp = self.driverWeb.execute_script("return document.documentElement.outerHTML")

        soupss = BeautifulSoup(str(resp),'lxml')
        # soups = soupss.find_all('div',class_="js-flightRow js-flightItem")
        
        #Find Airlines
        soups = soupss.find_all('span',class_="i-b text ellipsis")
        for s in soups:
            self.airline.append(str(s.text))
        
        #Find flight numbers
        soups = soupss.find_all('p',class_="normal fs-11 font-lightestgrey no-wrap fl-no")
        for s in soups:
            self.flight_num.append(str(s.text))

        #Find route/time
        # start = soupss.find_all('div',class_="i-b pr")
        start = soupss.find_all('div',class_="timing-det bdr-btm v-aligm-t")
        end = soupss.find_all('p',autom="arrivalTimeLabel")
        for c,s in enumerate(start):
            x = str(s.div.div.div)
            a = s.text.split(' ')
            s1 = a[0].strip(string.ascii_lowercase).strip(string.ascii_uppercase)
            self.time.append(x.split('<')[1].split('>')[1] + ' ---> ' + end[c].text)
        
        #Find Duration
        soups = soupss.find_all('div',class_="stop-cont pl-13")
        for s in soups:
            self.duration.append(s.p.text)

        #Find flight type
        soups = soupss.find_all('span',class_="cursor-default")
        for s in soups:
            self.flight_type.append(s.text)
        
        #Find Price
        soups = soupss.find_all('p',class_="i-b tipsy fare-summary-tooltip fs-18")
        for s in soups:
            self.price.append(s.text)

        # for soup in soups:
        #     # print(str(soup.article.div.ul.li.div.small.text))
        #     # self.links.append(self.get_link(counter,driver))
        #     # counter += 1
        #     self.airline.append(str(soup.article.div.ul.li.div.small.text))
        #     self.flight_num.append(soup.article.div.ul.li.div.find('small',class_="fs-10 ltr-gray fl ml5 nowrap").text)
        #     self.start_time = (soup.article.div.ul.find("li",class_="timing").div.span.text)
        #     self.end_time = (soup.article.div.ul.find("li",class_="timing").find('div',class_="end").span.text)
        #     self.time.append(self.start_time + '-->' + self.end_time) 
        #     self.duration.append(soup.article.div.ul.find("li",class_="timing").find('div',class_="time").span.text)
        #     self.flight_type.append(str(soup.article.div.ul.find("li",class_="timing").find('div',class_="time").small.text).replace('\t','').replace('\n',''))
        #     self.price.append(str(soup.article.div.ul.find("li",class_="price").find('div',class_="full").find('div',class_="btn-free-ui").find('p',class_="tfare fr").label.find('span',class_="bold").text).replace('\t','').replace('\n','').replace('Regular','').replace('\xa0',''))
    print("done")

    def details(self):
        details = {}
        details['Airline'] = self.airline
        self.num = len(self.airline)
        details['Flight Number'] = self.flight_num
        # details['Start Time'] = self.start_time
        # details['End Time'] = self.end_time
        details['Route/Time'] = self.time
        details['Duration'] = self.duration
        details['Flight Type'] = self.flight_type
        details['Price'] = self.price
        return details

# a = SearchYatra("BOM","DEL","10/12/2019")
# a.search()
# print(a.details())
# sleep(100)