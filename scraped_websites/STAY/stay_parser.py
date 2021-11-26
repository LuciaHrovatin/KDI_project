from pprint import pprint as pp
import csv, os, json  
from datetime import datetime

dir = r"C:\Users\Anna Fetz\Desktop\Data_Science\third_semester\KDI_2021\KDI_project\scraped_websites\STAY\CSV"
list_dir = os.listdir(dir)
list_dir_paths = [os.path.join(dir, f) for f in list_dir]
new_dir =  r"C:\Users\Anna Fetz\Desktop\Data_Science\third_semester\KDI_2021\KDI_project\scraped_websites\STAY\JSON"
dates = ['th','st','rd']
months = {'january': 1,'february' : 2,
            'march': 3,'april': 4,'may': 5,
            'june': 6, 'july': 7, 'august': 8, 
            'september': 9, 'october': 10, 'november': 11, 'december': 12}
mesi = {'gennaio': 1,'febbraio' : 2,
            'marzo': 3,'aprile': 4,'maggio': 5,
            'giugno': 6, 'luglio': 7, 'agosto': 8, 
            'settembre': 9, 'ottobre': 10, 'novembre': 11, 'dicembre': 12}
giorni = ['lunedì', 'martedì', 'mercoledì', 'giovedì', 'venerdì', 'sabato', 'domenica']
dayss = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']


def create_parsed_dictionary_and_write() :
    sc = {'name': ('mb-4">','</h1>'),
    'duration_hours': ('h6">','</h2>'),'duration_days': ('h6">','</h2>'),
    'location': 'class="h6">', 'info':[] ,'links':[], 'schema': [], 'description': ('<article','<h3')}
    for i in range(len(list_dir_paths)) :
   

        path = os.path.normpath(list_dir_paths[i])
        name = path.split(os.sep)
        file_name = name[-1]
        name = file_name.split('CSV')
        name = name[0]
        k = name.index('-')
        cat = name[:k]
        title = name[k:]
        if (list_dir_paths[i].endswith('.csv')) : 
            with open(list_dir_paths[i], encoding = "ISO-8859-1") as f : 
                d = {}
                d['links'] = []
                d['schema'] = []
                hours = []
                dy = []
                reader = csv.reader(f, delimiter=',')

                for row in reader: 
                    
                    clean = ' '.join(row).strip().split() 
                   
                
                    for word in clean :
                        if (word == sc['name'][0]) :
                            name = []
                            ind = clean.index(word)
                            while (ind < len(clean)-1) and (sc['name'][1] not in clean[ind]) : 
                                name.append(word)
                                ind +=1
                            name.append(clean[ind])
                            name.extend(['-',cat])
                        if ('tags:' in word) :
                            d['tags'] = []
                            i = clean.index(word)
                            while (i < len(clean)-1) and ('</a>' not in clean[i]) : 
                                w = clean[i].replace('<span','').replace( 'class="badge', '').replace('</h3>','').replace('badge-dark','').replace('mr-2','').replace('mb-2','').replace('</span>','').replace('tags:','').replace(' float-left">','')
                                d['tags'].append(w)
                                i += 1

                        if ('duration_hours' not in d) :
                            
                            if (sc['duration_hours'][0] in word) :
                                
                                
                                ind = clean.index(word)
                                 
                                while (ind < len(clean)) and (sc['duration_hours'][1] not in clean[ind]) :
                                   
                                    if (':' in clean[ind]) :
                                        j = clean[ind].index(':') 
                                        if (clean[ind][:j].isnumeric()) :
                                            hours.append(clean[ind])
                                    if ('am' in clean[ind]) or ('pm' in clean[ind]) :
                                        hours.append(clean[ind])
                                    if ('to' == clean[ind]) : 
                                        hours.append(clean[ind])
                                        hours.append(clean[ind+1])

                                    else :
                                        if (clean[ind] != 'at') and (clean[ind] != 'pm') and (clean[ind] != 'am') and (':' not in clean[ind]) :
                                            if ('to' in clean[ind+1]) :
                                                dy.append(clean[ind]+clean[ind+1])
                                            else :
                                                dy.append(clean[ind])

                                    ind += 1
                                hours.append(clean[ind])
                                d['duration_hours'] = hours 
                                d['duration_days'] = dy
                                

                        if ('location' not in d) :
                            if (sc['location'] in word) : 
                                j = clean.index(word)
                                d['location'] = ' '.join(clean[j:]).replace('class="h6">','').replace('</h2>','').replace('|',',')
                        if ('https' in word) and ('schema' not in word) :
                            d['links'].append(word)
                        if ('https' in word) and ('schema' in word) : 
                             d['schema'].append(word)
                        if (sc['description'][0] in word) :
                            ds = []
                            ind = clean.index(word)
                            while (sc['description'][1] not in clean[ind]) :
                             
                                ds.append(clean[ind])
                                ind += 1

                            d['description'] = ' '.join(ds)
                            d['name'] = title
                write_dic_to_json(d,title) 

                        




        
def write_dic_to_json(dic,title) :
    
    with open(os.path.join(new_dir, title)+'.json', 'w', encoding='utf-8') as f:
        json.dump(dic, f, ensure_ascii=False, indent=4, default=str)
        
create_parsed_dictionary_and_write()