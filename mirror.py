import time
import threading
import traceback
import locale
import json
from urllib import request
from tkinter import *
from contextlib import contextmanager
import pyowm

ui_locale = '' # e.g. 'fr_FR' fro French, '' as default
time_format = 12 # 12 or 24
date_format = "%b %d, %Y" # check python doc for strftime() for options
news_country_code = 'us'
xlarge_text_size = 94
large_text_size = 48
medium_text_size = 28
small_text_size = 18

LOCALE_LOCK = threading.Lock()

@contextmanager
def setlocale(name): #thread proof function to work with locale
    with LOCALE_LOCK:
        saved = locale.setlocale(locale.LC_ALL)
        try:
            yield locale.setlocale(locale.LC_ALL, name)
        finally:
            locale.setlocale(locale.LC_ALL, saved)

class Clock(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, bg='black')
        # initialize time label
        self.time1 = ''
        self.timeLbl = Label(self, font=('Helvetica', large_text_size), fg="blue", bg="black")
        self.timeLbl.pack(side=TOP, anchor=E)
        # initialize day of week
        self.day_of_week1 = ''
        self.dayOWLbl = Label(self, text=self.day_of_week1, font=('Helvetica', small_text_size), fg="white", bg="black")
        self.dayOWLbl.pack(side=TOP, anchor=E)
        # initialize date label
        self.date1 = ''
        self.dateLbl = Label(self, text=self.date1, font=('Helvetica', small_text_size), fg="white", bg="black")
        self.dateLbl.pack(side=TOP, anchor=E)
        self.tick()

    def tick(self):
        with setlocale(''):
            if time_format == 12:
                time2 = time.strftime('%I:%M %p') #hour in 12h format
            else:
                time2 = time.strftime('%H:%M') #hour in 24h format
                
            day_of_week2 = time.strftime('%A')
            date2 = time.strftime(date_format)
            # if time string has changed, update it
            if time2 != self.time1:
                self.time1 = time2
                self.timeLbl.config(text=time2)
            if day_of_week2 != self.day_of_week1:
                self.day_of_week1 = day_of_week2
                self.dayOWLbl.config(text=day_of_week2)
            if date2 != self.date1:
                self.date1 = date2
                self.dateLbl.config(text=date2)
            # calls itself every 200 milliseconds
            self.timeLbl.after(200, self.tick)

class Weather(Frame):
    def __init__(self,parent,*args, **kwargs):
        Frame.__init__(self, parent, bg='black')
        self.temperature = ''
        self.location = ''
        owm = self.get_weather()
        for keys,values in owm.items():
            print(keys)
            print(values)

    def get_weather(self):

        '''
        API Key: e8f68888e32b9e688db40c7a784aa417
        '''
        
        try:
            weather_api_url = "http://api.openweathermap.org/data/2.5/weather?id=524901&APPID=e8f68888e32b9e688db40c7a784aa417&q=92037,us&units=imperial"
            forecast_api_url = "http://api.openweathermap.org/data/2.5/forecast?id=524901&APPID=e8f68888e32b9e688db40c7a784aa417&q=92037,us&units=imperial"
            req = request.urlopen(forecast_api_url)      # calls for info from Open Weather Map
            omw = req.read().decode('utf-8')            # decodes the bytes into a json format
            data = json.loads(omw)                      # decodes json into dictionary
            #main = data['main']
            #weather = data['weather']
            #city = data['name']
        
            return data

        except Exception as e:
            traceback.print_exc()
            print('Error: ',e)
            print('Cannot get weather')


class FullscreenWindow:

    def __init__(self):
        self.tk = Tk()
        self.tk.configure(background='black')
        self.topFrame = Frame(self.tk, background = 'black')
        self.bottomFrame = Frame(self.tk, background = 'black')
        self.topFrame.pack(side = TOP, fill=BOTH, expand = YES)
        self.bottomFrame.pack(side = BOTTOM, fill=BOTH, expand = YES)
        self.state = False
        self.tk.bind("<Return>", self.toggle_fullscreen)
        self.tk.bind("<Escape>", self.end_fullscreen)
        # clock
        self.clock = Clock(self.topFrame)
        self.clock.pack(side=RIGHT, anchor=N, padx=100, pady=60)
        #weather
        self.weather = Weather(self.topFrame)


    def toggle_fullscreen(self, event=None):
        self.state = not self.state  # Just toggling the boolean
        self.tk.attributes("-fullscreen", self.state)
        return "break"

    def end_fullscreen(self, event=None):
        self.state = False
        self.tk.attributes("-fullscreen", False)
        return "break"

if __name__ == '__main__':
    w = FullscreenWindow()
    w.tk.mainloop()
    

