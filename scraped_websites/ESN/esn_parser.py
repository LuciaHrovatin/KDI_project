import os, csv, json 
import pprint as pp 

dir = r"C:\Users\Anna Fetz\Desktop\Data_Science\third_semester\KDI_2021\KDI_project\scraped_websites\ESN\CSV"
list_dir = os.listdir(dir)
list_dir_paths = [os.path.join(dir, f) for f in list_dir]

new_dir = r"C:\Users\Anna Fetz\Desktop\Data_Science\third_semester\KDI_2021\KDI_project\scraped_websites\ESN\JSON"
list_dir_new = os.listdir(new_dir)
list_dir_paths_new = [os.path.join(new_dir, f) for f in list_dir_new]






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
    """PARSES THE HTML FILE INTO A DICTIONARY"""
    for i in range(len(list_dir_paths)) :
        path = os.path.normpath(list_dir_paths[i])
        name = path.split(os.sep)
        dir_name = list_dir_paths[i].split(r"CRUSH\\")
        dir_name = name[-1]
        
       
        file_name = name[-1]
        
        if (list_dir_paths[i].endswith('.csv')) : 
            with open(list_dir_paths[i], encoding = "ISO-8859-1") as f : 
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
                                v = ''.join(el.replace('<','').replace('>','').replace('/span','').replace('"','').replace('/div','').replace('div','').replace('data-block=true','').replace('/h1',''))
                                    
                                    
                                analyse.append(v)

                    if (len(analyse) > 0 ): 
                        analyse = ' '.join(analyse).split('=')
                        links = []
                        description = []
                        schema = []
                        location = []
                        startDate = 0 
                        endDate= 0
                        for i in range(len(analyse)) : 
                            if ('page-title' in analyse[i]) or ('title-id' in analyse[i]) :
                                name = analyse[len('page-title'):]
                                d['name'] = name 
                            else :
                                d['name'] = file_name[:-4]

                            if ('class' not in analyse[i]) and ('data-offset-key' not in analyse[i]) \
                                and ('Fill in the form for the pre-registration' not in analyse[i]) and ('https' not in analyse[i]) : 
                                description.append(analyse[i])
                               
                                
                            if ('https:' in analyse[i]) and not ('schema.org' in analyse[i]) :
                                links.append(analyse[i])
                            if ('schema.org' in analyse[i]) :
                                schema.append(analyse[i])
                            if ('date-display-start' in analyse[i]) :
                                startDate = analyse[i]
                            else :
                                startDate = 'Not specified'
                            if ('date-display-end' in analyse[i]) : 
                                endDate = analyse[i]
                        d['organizer'] = 'ESN'
                        d['info'] = []
                        if ('field-labelAddress' in analyse[i]) : 
                            location.append(analyse[i])
                        if ('country' in analyse[i]) :
                            location.append(analyse[i].replace('country', ''))
                        else :
                            location = 'Not specified'
                            
                        d['description'] = ' '.join(description)
                        d['location'] = location
                        d['duration_hours'] = '{} {}'.format(startDate, endDate)
                        d['duration_days'] = ''
                        d['links'] = links
                        d['schema'] = schema
                    write_dic_to_json(d, file_name, new_dir)

def write_dic_to_json(dic,title, dir) :
    with open('{}\{}.json'.format(new_dir,title), 'w', encoding='utf-8') as f:
        json.dump(dic, f, ensure_ascii=False, indent=4, default=str)
             
#create_parsed_dictionary_and_write()

def parse_json() : 
    """PARSES THE HTML FILE INTO A DICTIONARY"""
    for i in range(len(list_dir_paths_new)) :
        path = os.path.normpath(list_dir_paths_new[i])
        name = path.split(os.sep)
        dir_name = list_dir_paths_new[i].split(r"CRUSH\\")
        dir_name = name[-1]
        
       
        file_name = name[-1]
      
        with open(list_dir_paths_new[i], encoding = "utf-8") as f : 
            dic = {}
            reader = json.load(f)
            date = []
            hour = []
            for d in reader:
                dic[d] = reader[d]
                if (d == 'description') : 
                    ls = reader[d].split()
                    
                    for j in range(len(ls)) : 
                        w = ls[j]
                        
                        if (w[-2:] in dates and w[-3].isnumeric()) :
                            date.append(w.replace('th','').replace('rd','').replace('st',''))
                        
                        if (w.isnumeric() and ls[j+1] in months) or (w.isnumeric() and ls[j+1] in mesi) :
                            date.append(w)
                            date.append(ls[j-1])
                            date.append(str(ls[j+1])+'/')
                            
                        if (w.lower() in months) :
                            date.append(str(months[w.lower()])+'/')

                        if (w.lower() in mesi) :
                            date.append(str(mesi[w.lower()])+'/')

                        if (w.lower() in dayss) :
                            date.append(w.lower())

                        if (w.lower() in giorni) :
                            date.append(w.lower())

                        if ('am' in w) or ('pm' in w) :
                            hour.append(ls[j-1])
                            hour.append(w)
            
            
            la = []
            for j in range(len(date)) : 
                el = date[j].strip() 
                
                    
                if (date[j] in months) :
                    m = str(months[date[j]])+'/'
                    if (m not in la) :
                        la.append(m)
                else :
                    
                    if (date[j][0].isdigit()) :
                        if (el not in la) :
                            la.append(el)
            lb = []
            for j in range(len(hour)) :

                if (hour[j][0].isnumeric()) :
                    if (hour[j] not in lb) :
                        lb.append(hour[j])
                
                if (len(hour[j]) <=3) and ('am'in hour[j]) or (len(hour[j]) <=3 and 'pm'in hour[j]) :
                    
                    lb.append(hour[j].strip('.,)('))
            

            
            
                    


            dic['duration_hours'].append(lb)
            dic['duration_days'].append(la)
            pp.pprint(dic)
            
                          

                        


        if i == 18 :
            break

        

print(parse_json())
