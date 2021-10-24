from pprint import pprint as pp
import csv, os, json  
from datetime import datetime

dir = r"C:\Users\Anna Fetz\Desktop\Data_Science\third_semester\KDI_2021\KDI_project\scraped_websites\CRUSH\CSV"
list_dir = os.listdir(dir)
list_dir_paths = [os.path.join(dir, f) for f in list_dir]
new_dir =  r"C:\Users\Anna Fetz\Desktop\Data_Science\third_semester\KDI_2021\KDI_project\scraped_websites\CRUSH\JSON"


def create_parsed_dictionary_and_write() : 
    """PARSES THE HTML FILE INTO A DICTIONARY"""
    
    for i in range(len(list_dir_paths)) :
        name = list_dir_paths[i].split(r"CRUSH\\")
        file_name = name[-1]
        new = file_name.split('CSV')
        to_join = new[-1][1:-4]
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
              
                write_dic_to_json(ret, to_join)
                               
        
                    
        

    

def parse_dict(dic):
    """CLEANS THE KEYS TO BE READABLE """
    for key in dic:
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
    return dic
  

def write_dic_to_json(dic,title) :
    with open(os.path.join(new_dir, title)+'.json', 'w', encoding='utf-8') as f:
        json.dump(dic, f, ensure_ascii=False, indent=4, default=str)
    

#create_parsed_dictionary_and_write()


dir = r"C:\Users\Anna Fetz\Desktop\Data_Science\third_semester\KDI_2021\KDI_project\scraped_websites\CRUSH\JSON"
list_dir = os.listdir(dir)
list_dir_paths = [os.path.join(dir, f) for f in list_dir]

new_dir = r"C:\Users\Anna Fetz\Desktop\Data_Science\third_semester\KDI_2021\KDI_project\scraped_websites\CRUSH\JSON\JSON_PARSED"

mesi = {'gennaio': 1,'febbraio' : 2,
            'marzo': 3,'aprile': 4,'maggio': 5,
            'giugno': 6, 'luglio': 7, 'agosto': 8, 
            'settembre': 9, 'ottobre': 10, 'novembre': 11, 'dicembre': 12}
giorni = ['lunedì', 'martedì', 'mercoledì', 'giovedì', 'venerdì', 'sabato', 'domenica']


for file in list_dir_paths : 
 
   
    with open(file, encoding ="utf-8") as f :
        parsed = {}
        dic = json.load(f)
        name = file.split('\\')
        name = name[-1].split('html')
        name = name[0]
        
        if (len(dic) > 0) : 
            parsed['name'] = name
            parsed['links'] = dic['links']
            parsed['location'] = dic['location']
            parsed['duration_hours'] = dic['duration_hours']
            parsed['duration_days'] = dic['duration_days']
            if ('schema' in dic) :
                parsed['schema'] = dic['schema']
            if ('Dove:' in dic['location']):
                dove = dic['location'].index('Dove:')
                parsed['location'] = dic['location'][dove:]
            if ('Orario:' in dic['location']) :
                orario = dic['location'].index('Orario:')
            else : 
                if ('Orario:' in dic['info']) :
                    orario = dic['info'].index('Orario')
                    parsed['duration_hours'] = orario
                else :
                        
                    if (len(dic['duration_hours']) > 0) and (dic['duration_hours'] != 'Not specified') : 
                        if (isinstance(dic['duration_hours'], str)) : 
                            lista = dic['duration_hours'].split()
                            if (':' in lista) : 
                                l1 = lista[:lista.index(':')]
                                l2 = lista[lista.index(':'):]
                                parsed['duration_hours'] = ' '.join(l1).replace('ore','')
                                if (dic['duration_days'] == 'Not specified') : 
                                    giorno = []
                                    for day in l1 :
                                            
                                        if (len(day) <=2 and day.isnumeric()) :
                                            giorno.append(day+'/')
                                            
                                        rep = day.replace(',','')
                                   
                                        if (rep in giorni) : 
                                            giorno.append(day) 
                                        if (rep.lower() in mesi) :
                                                
                                            giorno.append(str(mesi[rep.lower()])+'/202')
                                        if (day == 'ore') :
                                            parsed['duration_hours'] = parsed['duration_hours'].strip()
                                            parsed['duration_hours'] = parsed['duration_hours'].rstrip('.,:;')
                                            if (len(parsed['duration_hours']) > 5 ) :
                                                t = parsed['duration_hours'].split() 
                                                new = []
                                                for val in t : 
                                                    if ('.' in val) : 
                                                       new.append(val) 
                                                parsed['duration_hours'] = new 
                                    parsed['duration_days'] = giorno
                                if ('dalle' in l1) :
                                    dalle = l1.index('dalle')
                                    if ('alle' == l1[dalle+2]) :
                                        alle = l1.index('alle')
                                        if (len(parsed['duration_hours']) > 5 ) :
                                            parsed['duration_hours'] = l1[dalle:alle+2]
                                    else : 
                                        parsed['duration_hours'] = l1[dalle:]
                    if (parsed['duration_hours'] == 'Not specified') or (parsed['duration_days'] == 'Not specified'):
                        info = dic['info'].split()
                        giorno = []
                        for i in range(len(info)) : 
                            if ('itemprop=startDate' in info[i]) :
                                giorno.append(info[i-1])
                            if ('itemprop=endDate' in info[i]) :
                                giorno.append(info[i-1])
                            if ('itemprop=streetAddress' in info[i]) :
                                if (parsed['location'] == 'Not specified') :
                                    parsed['location'] = info[i:]
                            elif (i == len(info)) and (parsed['location'] == 'Not specified') :
                                if ('Dove:' in info) :
                                    dove = info.index('Dove:')
                                    parsed['location'] = info[dove:]

                        parsed['duration_days'] = giorno 
                        giorno2 = []
                        ora = []
                        if ('description' in dic ):
                            desc = dic['description'].split()
                            
                            for i in range(len(desc)) : 
                                if (parsed['duration_days'] == 'Not specified') : 
                                    rep = desc[i].rstrip(',.:;')
                                    if (rep.lower() in mesi) : 
                                        giorno2.append(str(mesi[rep])+"/")
                                    if (rep.lower() in giorni) :
                                        giorno2.append(rep)
                                if (parsed['duration_hours'] == 'Not specified')  : 
                                        
                                    if (desc[i] == 'ore') or (desc[i] == 'dalle') : 
                                        ora.append(desc[i+1])
                        if (len(ora) > 0) :
                            parsed['duration_hours'] = ora
                        if (len(giorno2) > 0):
                            parsed['duration_days'] = giorno2 

             
        #with open(os.path.join(new_dir,name)+'.json', 'w', encoding='utf-8') as f:
        #    json.dump(parsed, f, ensure_ascii=False, indent=4, default=str)
        




                            


  
