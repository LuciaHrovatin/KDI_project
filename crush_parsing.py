import os, csv, json 
import pprint as pp 

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

             
        with open(os.path.join(new_dir,name)+'.json', 'w', encoding='utf-8') as f:
            json.dump(parsed, f, ensure_ascii=False, indent=4, default=str)
        