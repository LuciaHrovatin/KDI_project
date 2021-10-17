import mysql.connector
import os 

path = os.getcwd()

class SQLWriter() : 
    def __init__(self, path) :
        self.path = path
        self.cursor = None
       
    def credentials(self, doc_name) :
        key_path = self.path[:-11] + doc_name
        with open(key_path) as f:
            line = f.readline()
            psw = line
            return psw


    def access(self, key_path ): 
        connection = mysql.connector.connect(
            host="127.0.0.1",
            port=3306,
            database='kdi_crushsite',
            user='root',
            password=self.credentials(self.path),
        )
        connection.autocommit = True
        self.cursor = connection.cursor()

    def query(self, dic) :
        query = "INSERT into trentino_events (event_id, event_name, event_date_time, event_note, event_location, event_authors,event_description, event_contacts, event_category, event_subcategory)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        for d in dic :
            self.cursor.execute(query,(
                d['event_id'], d['event_name'], 
                d['event_date_time'], d['event_note'], 
                d['event_location'], d['event_authors'],
                d['event_description'], d['event_contacts'], 
                d['event_category'], d['event_subcategory']
            ))
        self.cursor.close()
        self.connection.close()
        




    