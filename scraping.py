import selenium 
import pandas as pd
from selenium import webdriver
import bs4 as bs
import urllib.request
import pandas as pd
import sqlite3
from sql_connection import SQLWriter
import csv 
import os 

path_esn = os.getcwd()+'\scraped_websites\ESN'
path_crush = os.getcwd()+'\scraped_websites\CRUSH'
parser = 'html'


class Scraping() : 

    def __init__(self, link, parser) : 
        self.source = urllib.request.urlopen(link).read()
        self.soup = bs.BeautifulSoup(self.source, features = parser)
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
            

    def write_to_csv(self, event_name, classe, path):
        """ Write the Body of the Page to csv"""
        try:
            with open("{}/{}.csv".format(path, event_name), "a") as f:  # Open the csv file.
                div = self.soup.find_all('div', class_=classe)
                for d in div:
                    
                    csv_writer = csv.writer(f)
                    csv_writer.writerow(d)
        except:
            return False

