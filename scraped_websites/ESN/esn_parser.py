import os, csv, json 
from pprint import pprint as pp 


class EsnParser() : 
    def __init__(self) : 

        self.dir = r"C:\Users\Anna Fetz\Desktop\Data_Science\third_semester\KDI_2021\KDI_project\scraped_websites\ESN\CSV"
        self.list_dir = os.listdir(self.dir)
        self.list_dir_paths = [os.path.join(self.dir, f) for f in self.list_dir]

        self.new_dir = r"C:\Users\Anna Fetz\Desktop\Data_Science\third_semester\KDI_2021\KDI_project\scraped_websites\ESN\JSON"
        self.list_dir_new = os.listdir(self.new_dir)
        self.list_dir_paths_new = [os.path.join(self.new_dir, f) for f in self.list_dir_new]






        self.dates = ['th','st','rd']
        self.months = {'january': 1,'february' : 2,
                    'march': 3,'april': 4,'may': 5,
                    'june': 6, 'july': 7, 'august': 8, 
                    'september': 9, 'october': 10, 'november': 11, 'december': 12}
        self.mesi = {'gennaio': 1,'febbraio' : 2,
                    'marzo': 3,'aprile': 4,'maggio': 5,
                    'giugno': 6, 'luglio': 7, 'agosto': 8, 
                    'settembre': 9, 'ottobre': 10, 'novembre': 11, 'dicembre': 12}
        self.giorni = ['lunedì', 'martedì', 'mercoledì', 'giovedì', 'venerdì', 'sabato', 'domenica']
        self.dayss = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']


    def create_parsed_dictionary_and_write(self) : 
        """PARSES THE HTML FILE INTO A DICTIONARY"""
        for i in range(len(self.list_dir_paths)) :
            path = os.path.normpath(self.list_dir_paths[i])
            name = path.split(os.sep)
            dir_name = self.list_dir_paths[i].split(r"CRUSH\\")
            dir_name = name[-1]
            
        
            file_name = name[-1]
            
            if (self.list_dir_paths[i].endswith('.csv')) : 
                with open(self.list_dir_paths[i], encoding = "ISO-8859-1") as f : 
                    d = {}
                    reader = csv.reader(f,delimiter=',')
                    for row in reader:
                        analyse = []
                        if (len(row) > 1) :
                            grezzo = ' '.join(row).replace(r'\n','')
                            grezzo = grezzo.split()
                            for el in grezzo :
                                to_remove = set(['<span','<div','</div>','</span>','<br/></span>',
                                    '<br/>','<p','<p><span','</a></p>','</a>','</p>','/div'])
                                if (el not in to_remove) :
                                    v = ''.join(el.replace('<','').replace('>','').replace('/span','').replace('"','').replace('/div','').replace('div','').replace('data-block=true','').replace('/h1','').replace('h1',''))
                                        
                                        
                                    analyse.append(v)
                        
                        
                        if (len(analyse) > 0 ): 
                            
                           
                            analyse = ' '.join(analyse).split('=')
                            links = []
                            description = []
                            schema = []
                            location = []
                            date = []
                            recurrency = []
                            hours = []
                            info = []
                            for i in range(len(analyse)) : 
                                if ('page-title' in analyse[i]) or ('title-id' in analyse[i]) :
                                   
                                    name = ''.join(analyse[len('page-title'):]).replace('class title id page-title','') 
                                    d['name'] = name
                                else :
                                    d['name'] = ''.join(file_name[:-4]).replace('class title id page-title', '')
                                    

                                if ('https:' in analyse[i]) and not ('schema.org' in analyse[i]) :
                                    links.append(analyse[i])
                                if ('schema.org' in analyse[i]) :
                                    schema.append(analyse[i])
                                if ('date-display-start' in analyse[i]) or ('date-display-single' in analyse[i]):
                                    val = analyse[i].replace('date-display-start','').replace('date-display-single','').replace('class','')
                                    t = val.split('-')
                                    if (len(t) > 1) :
                                        hours.append(t[1]) 
                                        date.append(t[0])
                                    else :
                                        date.append(t[0])
                                   
                                if ('date-display-end' in analyse[i]) : 
                                    date.append(analyse[i].replace('date-display-end',''))
                           
                                if ('field-labelAddress' in analyse[i]): 
                                    location.append(analyse[i].replace('field-labelAddress','').replace('class',''))
                                if ('country' in analyse[i]) :
                                    location.append(analyse[i].replace('country', '').replace('class',''))
                                if ('class date-display-start' in analyse[i]) or ('class date-display-end' in analyse[i]) :
                                    hours.append(analyse[i].replace('class date-display-start','').replace('class date-display-end','').replace('class',''))
                                else:
                                    if ('class=' not in analyse[i]) and ('data-offset-key' not in analyse[i]) \
                                     and ('https' not in analyse[i]) and ('field-' not in analyse[i]) : 
                                        description.append(analyse[i])
                               
                                
                            d['description'] = ' '.join(description).replace('class group-secondary class group-details','').replace('field-group- class','').replace('field-label-inline clearfix class field-labelAddress:  class','')
                            d['location'] = location
                            d['duration_hours'] = hours
                            d['duration_days'] = date
                            d['links'] = links
                            d['schema'] = schema
                            d['info'] = info
                            d['recurrency'] = d['duration_days']
                            d['name'] = d['name'].replace('class title id page-title','')
                            
                            time = []
                            keep = []
                            for el in d['duration_days'] :
                                
                                if ('-' in el) :
                                    v = el.split('-')
                                    d['duration_hours'].append(v[-1])
                                    d['duration_days'] = v[0]
                                if (':' in el) :
                                    time.append(el.replace('class',''))
                                else :
                                    keep.append(el)
                            d['duration_hours'].extend(time)
                            d['duration_days'] = keep
                            
                            if ('trip' in d['name']) : 
                                n = d['name'].split('-')
                                d['location'].append(n[1])
                            if ('-val-' in d['name']) :
                                n = d['name'].split('-')
                                d['location'].extend(n[1:])

                            locations = set(['parco', 'piazza','verona','bolzano','trento','rovereto','garda','doss','zoom','virtual'])
                            d['description'] = d['description'].split()
                            for j in range(len(d['description'])) : 
                                w = d['description'][j]
                                
                                w_m1 = d['description'][j-1]
                                if (j+1 < len(d['description'])) :
                                    w_p1 = d['description'][j+1]
                                if (w.lower() in locations) : 
                                    d['location'].append(w)
                                    d['location'].append(w_m1)
                                    if (j+1 < len(d['description'])) :
                                        d['location'].append(w_p1)
                            d['description'] = ' '.join(d['description'])
                            name = d['name']
                           


                    self.write_dic_to_json(d, name, self.new_dir)

    def write_dic_to_json(self,dic,title, dir) :
        with open('{}\{}.json'.format(self.new_dir,title), 'w', encoding='utf-8') as f:
            json.dump(dic, f, ensure_ascii=False, indent=4, default=str)
                
    
    
#ep = EsnParser()            
#ep.create_parsed_dictionary_and_write()

