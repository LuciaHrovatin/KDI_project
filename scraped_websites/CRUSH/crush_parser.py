
import csv, os 
from datetime import datetime

dir = r"C:\Users\Anna Fetz\Desktop\Data_Science\third_semester\KDI_2021\KDI_project\scraped_websites\CRUSH"
list_dir = os.listdir(dir)
list_dir_paths = [os.path.join(dir, f) for f in list_dir]

def create_parsed_dictionary() : 
    """PARSES THE HTML FILE INTO A DICTIONARY"""
    i = 0
    for file in list_dir_paths :
        if (file.endswith('.csv')) : 
            with open(file, encoding = "ISO-8859-1") as f : 
                d = {}
                reader = csv.reader(f,delimiter=',')
                for row in reader:
                    analyse = []
                    if (len(row) > 1) :
                        grezzo = ' '.join(row).replace(r'\n','')
                        grezzo = grezzo.split()
                        for el in grezzo :
                            to_remove = set(['<span','<div','</div>','</span>','<br/></span>','<br/>','<p','<p><span','</a></p>','</a>','</p>'])
                            if (el not in to_remove) :
                                analyse.append(''.join(el.replace('<','').replace('>','').replace('/span','').replace('"','')))
                    
                    if (len(analyse) > 0) :
                        
                        try: 
                            if ('class=testoprincipale' not in analyse) :
                                schema_references = []
                                link_references = []
                            
                                start_name = analyse.index('class=colonnas-1-301ds')
                                end_name = analyse.index('itemprop=name')
                                organizer = analyse.index('itemprop=organizer')
                                startDate = analyse.index('itemprop=startDate')
                                endDate = analyse.index('itemprop=endDate')
                                duration = analyse.index('class=testo-boxgrigio-grassettoOrario:')
                                location = analyse.index('itemtype=http://schema.org/PostalAddress')
                                
                                description = analyse.index('class=testo-boxgrigio-grassettoNote:')
                                d['name'] = ' '.join(analyse[start_name+1:end_name]).replace('content=','')
                                d['organzer'] = ' '.join(analyse[end_name+1:organizer]).replace('content=','')
                                d['duration_days'] = ' '.join(analyse[startDate-1:endDate]).replace('content=','').replace('itemprop=startDate','')
                                d['duration_hours'] = ' '.join(analyse[duration+1:-1]).replace('class=testo-boxgrigio','')
                                d['location'] = ' '.join(analyse[location:]).replace('class=testo-boxgrigio-grassetto','').replace('class=testo-boxgrigio','')
                                d['info'] = ' '.join(analyse[description+1:])
                                for el in analyse :
                                    if ("http://schema.org" in el ) : 
                                        schema_references.append(el)
                                    
                                d['schema'] = schema_references

                            else : 

                                description = analyse.index('class=testoprincipale')
                                d['description'] = ' '.join(analyse[description+1:]).replace('class=testo-boxgrigio-grassetto','')
                            for el in analyse: 
                                if (el.startswith('href')) :
                                    link_references.append(el.replace('href=',''))
                                
                                d['links'] = link_references
                        except: 
                            print('Some research words were wrong for file {}'.format(file))
                    
        if i == 3:
            break
        i +=1

        print(d)
def read_parse_dict(dic) : 

    for key in dic : 
        if (key == 'duration_days') : 
            days = key.split()
            dic[key] = (datetime.strptime(days[0], '%Y-%m-%d').date(), datetime.strptime(days[1], '%Y-%m-%d').date())
        
print(create_parsed_dictionary())

                            


  
