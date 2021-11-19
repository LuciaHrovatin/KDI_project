import os 
import json 
import pprint as pp 
dir = os.listdir(r'C:\Users\Anna Fetz\Desktop\Data_Science\third_semester\KDI_2021\EVENTS')

d = {os.path.join(r'C:\Users\Anna Fetz\Desktop\Data_Science\third_semester\KDI_2021\EVENTS',v): [] for v in dir}


def return_list_of_files(dir,d) : 
    """Returns all files in all EVENT subfolders"""
  
    for current in d :
        l = os.listdir(current)
        for element in l :
            if (element.endswith('.json')) :
                d[current].append(os.path.join(current, element))
            else :
                l2 = os.listdir(os.path.join(current, element))
                for other in l2 :
                    d[current].append(os.path.join(os.path.join(current, element), other))

    return d 

def create_keys(dic) : 

    """Adds new keys : ticket, is_online, is_offline, is_blended and event category"""

    key_words = {'b': set(['biglietto', 'prezzo','ticket', 'prenotazione','gratuito','ingresso libero','partecipazione','gratis','libero','ingresso', 'entrata']), 
    'l':set(['webinar', 'online', 'zoom', 'teams'])}
    refused = []
    for key,val in dic.items() : 
        for file in val :
            if (file.endswith('.json')) :
                try: 
                    with open(file, encoding='utf-8') as f : 
                        load  = json.load(f)
                      
                    load['is_online'] = False
                    load['is_offline'] = False
                    load['is_blended'] = False
                    load['ticket'] = []
                    if ('description' in load) : 
                        load['description'] = load['description'].replace(r'\u0080', 'euro')
                        if (load['name'][0] == '-') : 
                            load['name'] = load['name'][1:]
                        if ('party' in load['name']) :
                            spl = 'party'
                        else : 
                            spl = load['name'].split('-')[0]
                        load['category'] = spl

                        desc = load['description'].split() 
                        for word in desc : 
                            n = word.lower().replace(':','')
                            if (n in key_words['b']) and (load['ticket']== []) :
                                
                                i = desc.index(word)
                                load['ticket'] = desc[i:] 
                            if (n == 'euro') : 
                                i = desc.index(word)
                                load['ticket'].append(desc[i-1])
                                load['ticket'].append(word)
                                load['ticket'].append(desc[i+1]) 
                            
                            if (n in key_words['l']) : 
                                i = desc.index(word)
                                load['is_online'] = True 
                            elif (n not in key_words['l']) : 
                                load['is_offline'] = True 
                    if ('ticket' not in load) :
                        if ('info' in load) :  
                            for word in desc : 
                                n = word.lower()
                                if (n in key_words['b']) :
                                    i = desc.index(word)
                                    load['ticket'] = desc[i:] 
                                if (n in key_words['l']) : 
                                    i = desc.index(word)
                                    load['is_online'] = True 
                                elif (n not in key_words['l']) : 
                                    load['is_offline'] = True 
                      
                    with open(file, 'w', encoding = 'utf-8') as f2 :   
                        json.dump(load, f2)
                except :
                    refused.append(file)
    return refused
        
            
        

                            


#ret = create_keys(return_list_of_files(dir,d))
#print('LASTLY, PRINT RET {}'.format(ret))