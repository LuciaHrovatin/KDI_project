import eventbrite 
from eventbrite import Eventbrite
import os 
import json 
import pandas as pd
import csv 


path = os.getcwd()
key_path = path[:-11]+'eventbrite.txt'

    

class EventSearch():

    def __init__(self, path,dir) : 
        self.key_path = path 
        self.events = {}
        self.dir = dir

    def connection(self) :
        """ Instantiating a connection """
        with open(self.key_path) as f:
            lines = f.readlines()
            token = lines[-1]
            event_connection = Eventbrite(token)

        return event_connection 

    def return_scenarios(self) : 
        """Returns a list of events' categories"""
        conn = self.connection()
        categories = conn.get_categories()

        return categories
    def return_sub_scenarios(self) : 
        """Returns a list of events' subcategories"""
        conn = self.connection()
        subcats = conn.get_subcategories()

        return subcats
    """
    def list_and_save_scenarios(self) : 
        scenarios = self.return_scenarios() 
        

        if ('list_of_categories.csv' not in os.listdir(self.dir)) : 
            df = pd.DataFrame({})
        else : 
            p = os.path.join(self.dir, 'list_of_categories' + "." + 'csv')
            df = pd.read_csv(p)
        
        for d in scenarios['categories'] : 
            df[d['name']] = 0 

        df.to_csv('list_of_categories.csv',index = False)
        return df

    def list_and_save_subscenarios(self) : 
        scenarios = self.return_sub_scenarios() 
        

        if ('list_of_subcategories.csv' not in os.listdir(self.dir)) : 
            df = pd.DataFrame({})
        else : 
            p = os.path.join(self.dir, 'list_of_subcategories.csv' + "." + 'csv')
            df = pd.read_csv(p)
        
        for d in scenarios['subcategories'] : 
            df[d['name']] = 0 

        df.to_csv('list_of_subcategories.csv',index = False)
        return df
    """

    def create_hierarchy(self) :
        """Returns a dictionary of categories and subcategories of events"""
        sub = self.return_sub_scenarios()
        if ('hierarchies.csv' not in os.listdir(self.dir)) : 
            df = pd.DataFrame({})
            df = df.to_dict()

        else : 
            df = {}

        for d in sub['subcategories'] : 
            if (d['parent_category']['name'] not in df) :
                df[d['parent_category']['name']] = [d['name']]
            else : 
                df[d['parent_category']['name']].append(d['name'])

        #df = pd.DataFrame.from_dict(df)
        #df.to_csv('hierarchies.csv', index = False)
        return df #TEMPORARY


    def get_event_details(self, event_ID) : 
        conn = self.connection()
        details = conn.get_event_attendees(event_ID)

        return details 


event = EventSearch(key_path, path)
user = event.get_event_details('187973753557') #NOT AUTHORIZED ACCESS
