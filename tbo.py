from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from time import sleep
from bs4 import BeautifulSoup
from threading import Thread
from datetime import datetime

class SearchTBO():
    def __init__(self,from_,to,date,type_="Economy"):
        self.usrname = "{Username}"
        self.passwd = "{Password}"
        self.airline = []
        self.flight_num = []
        self.time = []
        self.duration = []
        self.flight_type = []
        self.price = []
        self.from_ = from_
        self.to = to
        self.date = date
        self.type = type_

    def search(self):
        usr_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36"

        opts = Options()
        opts.add_argument("--headless")
        opts.add_argument("user-agent=%s"%usr_agent)
        opts.add_argument("--debug=False")

        driver = webdriver.Firefox(options=opts)
        driver.get("https://www.travelboutiqueonline.com/")

        username = driver.find_element_by_id("LoginName")
        username.send_keys(self.usrname)

        passwd = driver.find_element_by_id("Password")
        passwd.send_keys(self.passwd)

        login = driver.find_element_by_id("LoginImage")
        login.click()

        driver.find_element_by_id("btnYES").click()

        driver.get("https://m.travelboutiqueonline.com/FlightSearch.aspx")

        origin =  driver.find_element_by_id("origin")
        origin.send_keys(self.from_)

        dest = driver.find_element_by_id("destination")
        dest.send_keys(self.to)

        date = driver.find_element_by_id("departDate")
        date.click()

        date = str(self.date.split('/')[0])

        month = int(self.date.split('/')[1])
        cur_month = datetime.now().month
        dif = month - cur_month
        po = "first"
        
        if dif != 0:
            change = True
        else:
            change = False

        while change == True:
            changer = driver.find_element_by_xpath("//div[@class='ui-datepicker-group ui-datepicker-group-last']//div//a")
            changer.click()
            dif -= 1
            # if dif == 1:
            #     change = False
            #     po = "last"
            #     break
            if dif == 0:
                change = False
                break

        for i in range(1,6):
            for c in range(1,8):
                cal_date = driver.find_element_by_xpath("//div[@class='ui-datepicker-group ui-datepicker-group-%s']//table[@class='ui-datepicker-calendar']//tbody//tr[%s]//td[%s]"%(po,i,c)).text
                if cal_date == date:
                    cal_date = driver.find_element_by_xpath("//div[@class='ui-datepicker-group ui-datepicker-group-first']//table[@class='ui-datepicker-calendar']//tbody//tr[%s]//td[%s]"%(i,c))
                    cal_date.click()

        # for i in range(1,8):
        #     cal_date = driver.find_element_by_xpath("//div[@class='ui-datepicker-group ui-datepicker-group-last']//table[@class='ui-datepicker-calendar']//tbody//tr[1]//td[%s]"%(str(i)))
        #     if cal_date.text == "1":
        #         start = i
        #         break
        
        # #Gets the position of date
        # # DaysLeft = 7 - start
        # date = int(self.date.split('/')[0])
        # date = date + start
        # if date <= 7:
        #     p = 1
        # elif date <= 14:
        #     p = 2
        # elif date <= 21:
        #     p = 3
        # elif date <= 28:
        #     p = 4
        # else:
        #     p = 5
        
        # pos = date%7

        # if pos == 0:
        #     pos = 7

        # cal_date = driver.find_element_by_xpath("//div[@class='ui-datepicker-group ui-datepicker-group-first']//table[@class='ui-datepicker-calendar']//tbody//tr[%s]//td[%s]"%(str(p),str(pos-1)))
        # cal_date.click()

        search = driver.find_element_by_id("btnSearch")
        search.click()
        sleep(10)

        resp = driver.execute_script("return document.documentElement.outerHTML")
        soup = BeautifulSoup(resp,'lxml')
        results = soup.find_all('div',class_="result_p row")

        for result in results:
            tmpNum = result['id'].replace('ResSet_','')
            # print(tmpNum)
            flight_type = result.find('span',id="durationbox_"+tmpNum).a.em.text
            if len(flight_type) < 3:
                flight_type = "Non-Stop"
            self.flight_type.append(flight_type)
            self.airline.append(result.span.code.em.text)
            self.flight_num.append(result.code.find('em',class_="fleft width_100").kbd.text)
            time = result.find('span',class_="duration_flight mt5").text
            time = ''.join(time.split())
            # try:
            #     start_time = result.find('span',class_="duration_flight mt5").kbd.kbd.em.tt.text
            #     end_time = result.find('span',class_="duration_flight mt5").kbd.kbd.find('em',id="arrival_"+tmpNum).tt.text
            # except AttributeError:
            #     times = result.find('span',class_="duration_flight mt5").find('kbd',id="mob_pad_deparr").find_all('kbd',class_="fleft width_100")
            #     for time in times:
            #         start_time1 = time.em.tt.text
            #         end_time1 = 
            self.duration.append(result.find('span',id="durationbox_"+tmpNum).span.text)
            price = str(result.find('span',id="pubPriceSpan_"+tmpNum).find('span',id="PubPrice_"+tmpNum).text).replace('\n','')
            price = price.split()
            self.price.append(''.join(price))
            
            if len(time.split('(')) >= 4:
                a = time.split(')')
                time1 = a[0] + ')' + a[1] + ')'
                time2 =  a[2] + ')' + a[3] + ')'
                time = time1 + '\n' + time2

            self.time.append(time)

    def details(self):
        details = {}
        details['Airline'] = self.airline
        self.num = len(self.airline)
        details['Flight Number'] = self.flight_num
        details['Route/Time'] = self.time 
        details['Duration'] = self.duration
        details['Flight Type'] = self.flight_type
        details['Price'] = self.price
        return details

# a = SearchTBO("Mumbai(BOM), India","Delhi(DEL), India","25/09/2019")
# a.search()
# print(a.details())