import os, json, bs4  
dir = r'C:\Users\Anna Fetz\Desktop\Data_Science\third_semester\KDI_2021\KDI_PROJECT\EVENTS'
all_categories = os.listdir(dir)

class EventParser() : 
    def __init__(self,directory, list_directory, dictionary_events) :

        """INITIALIZES PARSERS' BASELINE DICTIONARY"""
        self.dir = directory
        self.listdir = list_directory 
        self.dict = dictionary_events 
        self.scarti = []

   
    def fill_events_dict(self) :
        
        for current in self.listdir :
            dir = os.path.join(self.dir, current)
            l = os.listdir(dir) #Opening each event's path
            for element in l :
                if (element.endswith('.json')) :
                    if (current in self.dict) :
                        self.dict[dir].append(os.path.join(dir, element))
                    else :
                        self.dict[dir] = [os.path.join(dir,element)]
                else :
                    l2 = os.listdir(os.path.join(dir, element))
                    for other in l2 :
                        if (dir in self.dict) : 
                            self.dict[dir].append(os.path.join(os.path.join(dir, element), other))
                        else : 
                            self.dict[dir] = [os.path.join(os.path.join(dir, element), other)]

    def parse_for_tickets(self) :
        i = 0 
        keys = list(self.dict.keys())

        while i < len(keys) :
            for item in self.dict[keys[i]] : 
              
                try : 
                    with open(item, encoding='utf-8') as f : 
                        loaded = json.load(f)
                        #if ('info' in loaded) : 

                    
                except : 
                    self.scarti.append(item) 
            if ( i == 15 ) : 
                break
            i += 1



        
event = EventParser(dir, all_categories, {})
event.fill_events_dict()
event.parse_for_tickets()