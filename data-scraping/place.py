import requests
from bs4 import BeautifulSoup
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import datetime
import time
import json

def type_prop(p):
    try:
        place_type = ' | '.join([s.text for s in p.findAll('span', class_='YhemCb')])
    except:
        try:
            place_type = p.find('div', class_='kpS1Ac').text
        except:
            print('ERROR: Couldn\'t find place type.')
            place_type = None 
    return place_type
    
def other_props(p):
    place_address = None
    other_attrib = {}
    
    try:
        for attrib in p.findAll('span', class_='LrzXr'):
            t = attrib.parent.find('span', class_='w8qArf').text.replace(': ','')

            if t == 'כתובת':
                place_address = attrib.text
            else:
                other_attrib[t] = attrib.text
    except:
        None

    return other_attrib, place_address

def events_prop(p):
    close_events = []
    classi = 'AxJnmb'
    sub_classi = 'PZPZlf'

    if p.find('a', class_='P7Vl4c') is not None:
        url = 'https://www.google.com{}'.format(p.find('a', class_='P7Vl4c')['href'])  
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36'}
        response = requests.get(url, headers=headers)
        content = response.content
        soup = BeautifulSoup((content).decode('UTF-8'), features="lxml")
        
        classi = 'EDblX'
        sub_classi = 'h998We'
        p = soup.find('div', class_='appbar')
        
    try:
        for e in p.find('div', class_=classi).findAll('div', class_=sub_classi):
            try:
                day = e.find('div', class_='aXUuyd').text
            except: day = None
            try:
                hour = e.find('div', class_='HoEOQb').text
            except: hour = None
            try:
                title = e.find('div', class_='title').text
            except: title = None
            close_events.append({'Day': day, 'Hour': hour, 'Title': title})
#             print('***', day, hour, title)
    except Exception as e:
        None

    return close_events

def get_code_by_selenium(place, chrome_driver_location):
    chrome_driver_location = chrome_driver_location
    first_url = 'http://www.google.com'
    options = webdriver.ChromeOptions()
    options.add_experimental_option('prefs', {'intl.accept_languages': 'he'})
    driver = webdriver.Chrome(chrome_driver_location, chrome_options=options)
    
    #driver.minimize_window()
    driver.get(first_url)
    driver.find_element_by_name('q').clear()
    search = driver.find_element_by_name('q')
    search.send_keys(place)
    search.send_keys(Keys.RETURN)
    html_code = BeautifulSoup(driver.page_source, 'lxml')
    
    driver.close()
    return html_code
    

class Place:    
    def __init__(self, name):
        self.name = name
        
    def google_soup(self, url=None):
        if url is None:
            url = 'https://www.google.com/search?q={}'.format(self.name.replace(' ','+')) 
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}
        #headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36'}
        response = requests.get(url, headers=headers)
        content = response.content
        self.content = content
        soup = BeautifulSoup((content).decode('UTF-8'), features="lxml")
        self.soup = soup
        return soup
    
    def knowledge_panel(self, current=True):
        if current:
            self.google_soup() 
            # print(self.soup)      
        panel = self.soup.find('div', class_='knowledge-panel')
        
        self.panel = panel
        return panel
    
    def live_pop(self, soup=None, current=True):
        cur_time = datetime.datetime.now().strftime("%D, %H:%M")
            
        if current:
            self.knowledge_panel() 
        
        if soup is not None:
            p = self.soup
        else:
            p = self.panel
        
        try:
            live_report = p.findAll('span', class_='m63ztc')[1].parent.text.replace('שידור חי: ', '')
            live_height = p.find('div', class_='ZQ55mf')['style'].replace('height:', '').replace('px', '')
        except:
            print('Couldn\'t find live property')
            live_report = None
            live_height = None
        try:
            usual_height = p.find('div', class_='ZQ55mf').parent['style'].split(';')[-1].replace('height:', '').replace('px', '')
        except:
            try:
                usual_height = p.find('span', class_='eldaeC0zR5P__bs').text
            except:
                usual_height = None
        


        
        return {'time': cur_time, 'live_report': live_report, 'live_height': live_height, 'usual_height': usual_height}
    
    def set_general_hours(self):
        chrome_driver_location = r'..\chromedriver_win32\chromedriver'
        soup = get_code_by_selenium(self.name, chrome_driver_location)
        
        week_dicti = {}
        for histo in soup.findAll('div', class_='ecodF'):
            day = histo['aria-label'].replace('היסטוגרמה המראה שעות פופולריות בימי ','').replace(':','')
            day_dicti = {}
            for hour_ele in histo.findAll('div', class_='lubh-bar'):
                hour = hour_ele['aria-label'].split()[0]
                day_dicti[hour] = {'general_population': hour_ele['aria-label'], 'height': hour_ele['style']}
            week_dicti[day] = day_dicti

        self.general_population = week_dicti
        return week_dicti
    
    def set_props(self):
        if hasattr(self, 'panel') == False:
            self.knowledge_panel() 
        p = self.panel
        if p is None:
            self.knowledge_panel()
        p = self.panel
        if p is None:
            print('FUCK')
            return {'error': 'couldn\'t set knowledge panel'}


        print('x')
        try:
            place_google_name = p.find('div', class_='kno-ecr-pt').text
        except:
            try:
                place_google_name = p.find('div', class_='SPZz6b').text
            except: 
                print(self.knowledge_panel())
                place_google_name = None
                pass
                # self.knowledge_panel() 
                # return self.set_props()
        
        place_type = type_prop(p)
        
        place_google_images = [img.find('img')['src'] for img in p.findAll('g-img')]
        outside_view_link = []
        for img in p.findAll('g-img'):
            print(img.parent)
            try:
                outside_view_link.append(img.parent.href)
            except: pass 
        outside_view_link = []

        # outside_view_link = [img.find('a')['href'] for img in p.findAll('rhsl5')]

        try:
            place_descrip = p.find('div', class_='hb8SAc').text
        except:
            place_descrip = None
            
        try:
            usual_time_spent = p.find('div', class_='UYKlhc').text
        except:
            usual_time_spent = None
        
        other_attrib, place_address = other_props(p)
        
        close_events = events_prop(p)
        
        live_population = self.live_pop()
        
        self.google_name = place_google_name
        self.type = place_type
        self.description = place_descrip
        
        if place_address is not None:
            self.address = place_address
        self.other = other_attrib
        self.events = close_events
        self.live_population = live_population
        self.usual_time_spent = usual_time_spent

        self.google_images = place_google_images
        self.outside_view_links = outside_view_link
        
        return self.__dict__

    def google_api(self, api_key = 'AIzaSyDkG702RFFEEm08CP87sLK_amm-ru_eUVs'):
        url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"       
        query = self.name

        r = requests.get(url + 'query=' + query + '&key=' + api_key + '&language=he') 

        x = r.json() 
        first_result = x['results'][0]
        
        self.location = first_result['geometry']['location']
        self.address = first_result['formatted_address']

        self.google_api_info = x['results'] 
        
        return x['results']

    def get_props(self):
        dicti = {}
        
        for key in self.__dict__.keys():
            if key not in ['content', 'soup', 'panel']:
                dicti[key] = self.__dict__[key]
        
        return dicti



if __name__ == '__main__':
    print(Place('דיזינגוף סנטר').set_props()['panel']) 
