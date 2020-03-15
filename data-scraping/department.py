import requests
from bs4 import BeautifulSoup
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import datetime
import time
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS, cross_origin
import json

class Department:
    def __init__(self, query):
        self.query = query
        self.places = []
    
    def google_soup(self):
        # url = 'https://www.google.co.il/maps/search/{}'.format('+'.join([self.type, 'ב'+self.city]).replace(' ','+'))
        url = 'https://www.google.co.il/maps/search/{}'.format(query).replace(' ','+')
        print(url)
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36'}
        response = requests.get(url, headers=headers)
        content = response.content
        self.content = content
        soup = BeautifulSoup((content).decode('UTF-8'))
        
        return soup
    
    def google_api_list(self, api_key = 'AIzaSyDkG702RFFEEm08CP87sLK_amm-ru_eUVs'):
#         api_key = 'AIzaSyDkG702RFFEEm08CP87sLK_amm-ru_eUVs'
        url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"
        
        # typi = self.type
        # city = self.city

        # query = ' '.join([typi, city])

        query = self.query

        r = requests.get(url + 'query=' + query + '&key=' + api_key + '&language=he') 

        resultjson = r.json() 

        results = resultjson['results'] 
        
        return json.dumps([place['name'] for place in results], ensure_ascii=False)