from pprint import pprint as pp
import csv, os, json  
from datetime import datetime


dir = r"C:\Users\Anna Fetz\Desktop\Data_Science\third_semester\KDI_2021\KDI_project\scraped_websites\CRUSH"
list_dir = os.listdir(dir)
list_dir_paths = [os.path.join(dir, f) for f in list_dir]
new_dir =  r"C:\Users\Anna Fetz\Desktop\Data_Science\third_semester\KDI_2021\KDI_project\scraped_websites\CRUSH\CSV"
def create_parsed_dictionary_and_write() : 
    """PARSES THE HTML FILE INTO A DICTIONARY"""
    
    for i in range(len(list_dir_paths)) :
        name = list_dir_paths[i].split(r"CRUSH\\")
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
                            '<br/>','<p','<p><span','</a></p>','</a>','</p>'])
                            if (el not in to_remove) :
                                analyse.append(''.join(el.replace('<','').replace('>','').replace('/span','').replace('"','')))
                    
                    if (len(analyse) > 0) :
                        
                   
                        if ('class=testoprincipale' not in analyse) :
                                
                            schema_references = []
                            link_references = []
                            
                            start_name = analyse.index('class=colonnas-1-301ds')
                            
                            
                            if ('itemprop=startDate' in analyse) and ('itemprop=endDate' in analyse) : 
                                startDate = analyse.index('itemprop=startDate')
                                endDate = analyse.index('itemprop=endDate')
                                d['duration_days'] = ' '.join(analyse[startDate-1:endDate]).replace('content=','').replace('itemprop=startDate','')
                            if ('itemprop=startDate' in analyse) and not ('itemprop=endDate' in analyse) : 
                                startDate = analyse.index('itemprop=startDate')
                                d['duration_days'] = ' '.join(analyse[startDate-1:startDate+2]).replace('content=','').replace('itemprop=startDate','')
                            else :
                                d['duration_days'] = 'Not specified'
                            if ('name' in analyse) :
                                end_name = analyse.index('itemprop=name')
                                if ('itemprop=organizer' in analyse) :
                                    organizer = analyse.index('itemprop=organizer')
                                    d['organizer'] = ' '.join(analyse[end_name+1:organizer]).replace('content=','')
                                    d['name'] = ' '.join(analyse[end_name+1:organizer]).replace('content=','')
                                else :
                                    d['name'] = ' '.join(analyse[end_name+1:-1]).replace('content=','')
                            else :
                                name = 'Not speficied'
                                d['name'] = name
                            
                            if ('itemtype=http://schema.org/PostalAddress' in analyse) :
                                location = analyse.index('itemtype=http://schema.org/PostalAddress')
                                d['location'] = ' '.join(analyse[location:]).replace('class=testo-boxgrigio-grassetto','').replace('class=testo-boxgrigio','')
                            elif ('class=testo-boxgrigio-grassettoDove:' in analyse) :
                                
                                location = analyse.index('class=testo-boxgrigio-grassettoDove:')
                                d['location'] = ' '.join(analyse[location:]).replace('class=testo-boxgrigio-grassetto','').replace('class=testo-boxgrigio','')
                            else :
                                location = 'Not specified'
                                d['location'] = location

                            if ('class=testo-boxgrigio-grassettoOrario:' in analyse) :
                                duration = analyse.index('class=testo-boxgrigio-grassettoOrario:')
                                d['duration_hours'] = ' '.join(analyse[duration+1:-1]).replace('class=testo-boxgrigio','')
                            else :
                                duration = 'Not specified'
                                d['duration_hours'] = duration
                            
                            
                            if ('class=testo-boxgrigio-grassettoNote:' in analyse) :     
                                description = analyse.index('class=testo-boxgrigio-grassettoNote:')
                            else :
                                description = analyse.index('class=testo-boxgrigio-grassetto')
                            
                            
                         
                            
                            
                            
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
                        
                        
                ret = parse_dict(d)
                write_dic_to_json(d, new_dir)
                               
        
                    
        

    

def parse_dict(dic) : 
    """CLEANS THE KEYS TO BE READABLE """
    for key in dic :
        if (dic[key] != 'Not specified') : 
            if (type(dic[key]) == str) : 
                dic[key] = dic[key].replace('-grassettoNote', '').replace('-grassetto', '').replace('class=testo-boxgrigio','').replace("'",'')
                dic[key] = dic[key].replace('strong','').replace('strongbr','').strip('/br').strip('abr').replace('...','.').replace('/br/',' ').replace('.br/',' ')
            if (key == 'duration_days') : 
                
                if not isinstance(dic[key][0], datetime.date) :
                    days = dic[key].split()
                    dic[key] = (datetime.strptime(days[0], '%Y-%m-%d').date(), datetime.strptime(days[1], '%Y-%m-%d').date())
                
                
            if (key == 'duration_hours') :
              
                if ('/' in dic[key]) : 
                
                    l = dic[key].split('/')
        
                    dic[key] = l[0]
                    l2 = l[0].split()
                    time = []
                    for i in range(len(l2)) :
                        if ('ore' in l2[i]) :
                            time.append(l2[i+1])
                    dic[key] = time

            if (key == 'location') :
                end = -1
                loc = dic[key].split()
                
                for i in range(len(loc)) :

                    if (loc[i].startswith('itemprop=streetAddress')) :
                        j = i 
                        
                    if ('(bz)' in loc[i].lower()) or ('(tn)' in loc[i].lower()) or ('trento' in loc[i].lower()) or ('bolzano' in loc[i].lower()) :
                        end = i+1 
                        dic[key]= loc[: end]       
        
            if (key == 'description') or (key == 'info'): 
                new = []
                l = dic[key].split()
                for el in l :
                    if ('href' not in el) and ('target=' not in el) and ('class=' not in el):
                        new.append(el)
                new = ' '.join(new)
                dic[key] = new
  

def write_dic_to_json(dic,title) :
    with open('{}.json'.format(title), 'w', encoding='utf-8') as f:
        json.dump(dic, f, ensure_ascii=False, indent=4, default=str)
    return(dic)

create_parsed_dictionary_and_write()





                            


  
