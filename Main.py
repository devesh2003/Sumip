from tkinter.ttk import *
import Yatra
from tkinter import *
from threading import Thread
from selenium import webdriver
import tbo

class HomePage():
    def __init__(self,geometry="1450x500",title="SUMIP"):
        self.first = True
        self.root = Tk()
        self.geometry = geometry
        self.title = title
        self.make_fields()
        self.create_buttons()

    def create_results(self):
        #Creates Frame
        result_frame = Frame(self.root)
        result_frame.place(x=35,y=150)

        tot = len(self.details['Airline'])

        tot_results = Label(self.root,text="Total Result(s) : %d"%(tot))
        tot_results.place(x=40,y=120)

        style = ttk.Style(self.root)
        style.configure('Treeview',rowheight=45)


        self.results = Treeview(result_frame)
        self.results.grid(columnspan=7)

        scroll_bar = ttk.Scrollbar(self.root,orient='vertical',command=self.results.yview)
        scroll_bar.place(x=1220,y=190,height=300)

        self.results.configure(yscrollcommand=scroll_bar.set)

        titles = ["Airline","Flight Number","Route/Time","Duration","Flight Type","Price"]

        self.results["columns"] = titles
        self.results["show"] = "headings"
        for title in titles:
            self.results.heading(title,text=title)

        flight_details = []
        for counter in range(0,self.search.num-1): # Add " + self.tbo.num" for tbo
            for detail in self.details:
                flight_details.append(self.details[detail][counter])
#               print(counter)
#            counter += 1
            flight_details = tuple(flight_details)
            self.results.insert("",0,(counter),values=flight_details)
            self.results.bind("<Double-1>",self.test)
            flight_details = [] 

    def test(self,event):
        item = self.results.selection()[0]
        t = Thread(target=self.booking_page,args=(item))
        t.start()

    def booking_page(self,t,item,**kwargs):
        print(t)
        print("First :",self.first)
        if self.first == True:
            self.first = False
            link = self.search.get_link(int(item)+1,True)
            driver1 = webdriver.Chrome()
            driver1.get(link)
        elif self.first == False:
            link = self.search.get_link(int(item)+1,False)
            driver2 = webdriver.Chrome()
            driver2.get(link)

    def update_details(self,dets):
        titles = ["Airline","Flight Number","Route/Time","Duration","Flight Type","Price"]
        i = 0
        for detail in dets:
            for item in dets[detail]:              
                self.details[titles[i]].append(item)
            i += 1

    def search_flights(self):
        date = self.date.get()
        a = Yatra.SearchYatra(self.from_.get(),self.to_.get(),date)
        search = Thread(target=a.search,name="Yatra Search")
        search.start()

        # TBO search
        # TBO = tbo.SearchTBO("Mumbai(BOM), India","Delhi(DEL), India",date)
        # t = Thread(target=TBO.search,name="TBO Search")
        # t.start()

        search.join()
        # t.join()
        self.details = a.details()
        self.search = a       
        # details_tbo = TBO.details()
        # self.tbo = TBO
        # self.update_details(details_tbo) 
        self.create_results()

    def start_search(self):
        t = Thread(target=self.search_flights)
        t.start()
  
    def create_buttons(self):
        #Creates the search button
        search_frame = Frame(self.root)
        search_frame.place(x=580,y=100)

        search_button = ttk.Button(search_frame,text="Search",command=self.start_search)
        search_button.pack()

    def make_fields(self):
        shift = 10
        #Creates Heading
        h_frame = Frame(self.root)
        h_frame.place(x=580+shift,y=10)

        h_label = Label(h_frame,text="SUMIP",font=("Arial",15))
        h_label.pack()

        #Creates Dropdown box for FROM
        d_frame = Frame(self.root)
        d_frame.place(x=500+shift,y=50)

        from_ = StringVar()
        from_.set('BOM')

        opt = OptionMenu(d_frame,from_,'BOM','DEL')
        opt.pack()

        to_ = StringVar()
        to_.set('DEL')

        #Creates date input
        date_heading = Label(self.root,text="Date",font=("Bold",12))
        date_heading.place(x=785+shift,y=35)

        self.date = StringVar()
        date_input = Entry(self.root,textvariable=self.date,bg="light grey")
        date_input.place(x=750+shift,y=58)
        

        d_frame2 = Frame(self.root)
        d_frame2.place(x=650+shift,y=50)

        opt = OptionMenu(d_frame2,to_,'BOM','DEL')
        opt.pack()

        self.from_ = from_
        self.to_ = to_

    def stop(self):
        self.root.destroy()

    def start(self):
        self.root.geometry(self.geometry)
        self.root.title(self.title)
        # gui_thread = Thread(target=self.root.mainloop)
        # gui_thread.start()
        self.root.mainloop()

a = HomePage()
a.start()