import selenium 
import pandas as pd
from selenium import webdriver
import bs4 as bs

import pandas as pd
import sqlite3

import csv 
import os 

path_esn = os.getcwd()+'\scraped_websites\ESN'
path_crush = os.getcwd()+'\scraped_websites\CRUSH'
parser = 'html'
path_stay = os.getcwd()+'\scraped_websites\STAY\CSV'

class Scraping() : 

    def __init__(self, source,link, parser) :
        
        self.soup = bs.BeautifulSoup(source, features = parser)
        self.body = self.soup.body
        self.link = link

    def select_link(self) :
        """ Returns the link """
        s = []
        for url in self.soup.find_all('a'):
            s.append(url.get('href'))
        return s

    def get_body(self, classe) : 
        """Get the Body of the Page"""
        lista = []
        for div in self.soup.find_all('div', class_=classe):
                lista.append(div)
        return lista

    def get_n_body(self, classe, n) :
        lista = []
        i = 0
        for div in self.soup.find_all('div', class_=classe):
                lista.append(div)
                if (i == n) :
                    break
        return lista
        


    def write_to_csv(self, event_name, classe, path):
        """ Write the Body of the Page to csv"""
        
        
        with open("{}/{}.csv".format(path_stay, event_name.replace('/','')), "w", encoding ='utf-8') as f:  
            div = self.soup.find_all('div', class_=classe)
            for d in div:
                csv_writer = csv.writer(f)
                print(d)
                csv_writer.writerow(d)
        f.close()
           
        

