import os, csv, json 
import pprint as pp 

dir = r"C:\Users\Anna Fetz\Desktop\Data_Science\third_semester\KDI_2021\KDI_project\scraped_websites\ESN"
list_dir = os.listdir(dir)
list_dir_paths = [os.path.join(dir, f) for f in list_dir]



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
                    write_dic_to_json(d, file_name, dir_name)

def write_dic_to_json(dic,title, dir) :
    with open('{}\{}.json'.format(dir,title), 'w', encoding='utf-8') as f:
        json.dump(dic, f, ensure_ascii=False, indent=4, default=str)
             
create_parsed_dictionary_and_write()