import os, json 
import pprint

dir = r'C:\Users\Anna Fetz\Desktop\Data_Science\third_semester\KDI_2021\PARSING'
all_categories = os.listdir(dir)

class EventParser() : 
    def __init__(self,directory, list_directory, dictionary_events, endingdir) :

        """INITIALIZES PARSERS' BASELINE DICTIONARY"""
        self.dir = directory
        self.listdir = list_directory 
        self.dict = dictionary_events 
        self.scarti = []
        self.writedir = endingdir

   
    def fill_events_dict(self) :
        
        for current in self.listdir :
            if (current.endswith('.json')) :
                if (self.dir) in self.dict :
                    self.dict[self.dir].append(os.path.join(self.dir, current))
                else :
                    self.dict[self.dir] = [os.path.join(self.dir, current)]
            else : 
                dir = os.path.join(self.dir, current)
              
                l = os.listdir(dir) #Opening each event's path
                for element in l :
                    if (not element.endswith('.py')) : 
                        if (element.endswith('.json')) :
                            if (current in self.dict) :
                                self.dict[dir].append(os.path.join(dir, element))
                            else :
                                self.dict[dir] = [os.path.join(dir,element)]
                        else :
                            l2 = os.listdir(os.path.join(dir, element))
                            for other in l2 :
                                if (not other.endswith('.py')) : 
                                    if (dir in self.dict) : 
                                        self.dict[dir].append(os.path.join(os.path.join(dir, element), other))
                                    else : 
                                        self.dict[dir] = [os.path.join(os.path.join(dir, element), other)]

    def parse_for_tickets_CRUSHSITE(self) :
        i = 0
        counter = 0
        classes = ['danza-teatro', 'musica', 'cinema','didattica','incontri','mostre','iniziative-bambini']
        key = 'C:\\Users\\Anna Fetz\\Desktop\\Data_Science\\third_semester\\KDI_2021\\PARSING\\scraped_websites'
        for item in self.dict[key] : 
            print(item)
            if (item.endswith('.json')) : 
                with open(item, encoding='utf-8') as f : 
                        lo = json.load(f)
                       
                        loaded = lo
                        parsed = {}
                        
                        # STARTING WITH LOCATION TIME AND DATE
                        if (len(list(loaded.keys())) > 0) and ('location' in list(loaded.keys()))  : 
                            if (type(loaded['location']) == str) :
                               loaded['location'] = loaded['location'].split()
                           
                            if ('Dove:' in loaded['location']) : 
                                d = loaded['location'].index('Dove:')
                            if  ('Orario:' in loaded['location']) : 
                                o = loaded['location'].index('Orario:')
                            if ('Note:' in loaded['location']) : 
                                n = loaded['location'].index('Note:')
                                
                            if (d and o) : 
                                parsed['location'] = loaded['location'][d+1:o]
                            if (not d and o) : 
                                parsed['location'] = loaded['location'][:o]
                            if (d and not o and n) : 
                                parsed['location'] = loaded['location'][d+1:n]
                            if (o and n) : 
                                parsed['duration'] = loaded['location'][o:n]
                                parsed['info'] = loaded['location'][n:]
                            if (not o and n) :
                                parsed['info'] = loaded['location'][n:]
                            parsed['location'] = ' '.join(parsed['location']).replace('itemtype=http://schema.org/PostalAddress','').replace('itemprop=','').replace('\x96','-').replace('streetAddress','').split()
                            parsed['duration'] = ' '.join(parsed['duration']).replace('\x96','-').replace('Orario:','').split()
                            parsed['info'] = ' '.join(parsed['info']).replace('\x80','€').split()
                            
                            if ('Trento' in parsed['duration']) or ('(Tn)' in parsed['duration']) \
                                or ('Tn' in parsed['duration']) or ('Bolzano' in parsed['duration'] or ('(Bz)' in parsed['duration'])):
                                parsed['location'] += parsed['duration']
                                parsed['duration'] = []
                               
                        # DESCRIPTION AND INFORMATION + SCHEMA AND LINKS

                            if  (parsed['info'] == []) or (parsed['info'][0] == 'Orario:') :
                                if  ('info' in list(loaded.keys())) :
                                    parsed['info'] = loaded['info'].replace('\x80','€').replace('\x92',"'").replace(''.join(parsed['location']),'')
                            if (parsed['duration'] == []) :
                                if ('duration_hours' in list(loaded.keys())) : 
                                    parsed['duration'] = (''.join(loaded['duration_hours']).replace('Not specified','').replace('ore','') + ''.join(loaded['duration_days']).replace('Not specified','').replace('ore','')).replace('\x92',"'").replace('Orario:','').split()
                        if ('description' in loaded) :
                            parsed['description'] = loaded['description']
                            if ('location' in loaded) : 
                                parsed['description'] = parsed['description'].replace(' '.join(loaded['location']),'')
                            parsed['description'] = parsed['description'].replace('\x80', '€')
                        if ('links' in loaded) :
                            parsed['links'] = loaded['links']
                        
                        
                        t = {'is_free': False, 'has_ticket':{
                                'has_onlineBooking': False,
                                'has_extraBenefits' : None, 
                                'has_total' : None,
                                'has_price' : [],
                                'has_currency' : 'EUR',
                                'has_seller': None,
                                'has_purchaser': None
                            }}
                        parsed['specialAnnouncements'] = []
                        parsed['cost'] = t
                        # FIXING SOME SPACES FROM WRONG JOINS 
                        if ('info' in parsed) : 
                            fix = ' '.join(parsed['info']).replace('   ','&').split('&')
                            new_info = []
                            for el in fix :
                                v = el.replace(' ','')
                                new_info.append(v)
                            if (new_info != []) :
                                parsed['info'] = ' '.join(new_info)

                            # TICKET PARSING + COVID REGULATIONS 
                            additional_info = parsed['info'].replace('euro','€').split('/')
                            ticket = []
                            covid = []
                            prenotazione = []
                            sconti = []
                            
                            for el in additional_info :
                                if ('Costo totale del corso:' in el) :
                                    if (el not in ticket) :
                                        ticket.append(el)
                                       
                                if ('Informazioni su prenotazioni' in el) :
                                    if (el not in ticket) :
                                        ticket.append(el)
                                        parsed['info'] = parsed['info'].replace(el,'')
                                if ('mascherine' in el.lower()) or ('mascherina' in el.lower()) or ('prenotazione obbligatoria' in el.lower()) \
                                    or ('posti limitati' in el.lower()) or ('covid' in el.lower()) or ('distanziamento' in el.lower()) \
                                        or ('green pass' in el.lower()) or ('Green' in el.lower()) or ('vaccino' in el.lower()) \
                                            or ('Pass' in el.lower()) or ('Decreto-Legge' in el.lower()) or ('COVID-19' in el) \
                                                or ('assembrament' in el.lower()) or ('potranno subire variazioni' in el.lower()):
                                        covid.append(el)
                                   
                                if ('costo' in el.lower()) or ('€' in el.lower()) :
                                    if (el not in ticket) :
                                        ticket.append(el)
                                      
                                if ('riduzione' in el.lower()) or ('sconto' in el.lower()) or ('gratuito con' in el.lower()):
                                    if (el not in sconti) : 
                                        sconti.append(el)
                                     
                                if ('Ingresso gratuito' in el) or ('Ingresso libero' in el) : 
                                    t['is_free'] = True
                                    parsed['info'] = parsed['info'].replace(el,'')
                                if ('prenotazione online' in el) or ('biglietto online' in el) :
                                    t['has_ticket']['has_onlineBooking'] = True 
                                
                            for el in ticket :
                                if (el != None) :
                                    parsed['info'] = parsed['info'].replace(el,'')
                           
                            for el in sconti :
                                if (el != None) :
                                    parsed['info'] = parsed['info'].replace(el,'')
                            for el in covid :
                                if (el != None) :
                                    parsed['info'] = parsed['info'].replace(el,'')


                                
                                        
                                
                            ticket =' '.join(ticket).replace('Note:Costo:','').split()
                        
                            t['has_ticket']['has_price'] = ' '.join(ticket)
                            t['has_ticket']['has_extraBenefits'] = ' '.join(sconti) 
                            parsed['specialAnnouncements'] = ' '.join(covid) 
                            parsed['cost'] = t

                          
                            
                            ## SISTEMARE DATA TYPES ##
                            parsed['location'] = ' '.join(parsed['location'])
                            parsed['info'] = parsed['info'].replace('/','').replace(parsed['location'],'').replace(parsed['cost']['has_ticket']['has_price'],'').replace(parsed['specialAnnouncements'],'')
                            name = item.split('\\')
                            name = name[-1]
                            
                            
                            for c in classes :
                                if (c in name) :
                                    parsed['category'] = c # TO BE REMOVED
                            
                            if 'category' not in parsed : 
                                parsed['category'] = ''
                            parsed['name'] = name.replace(parsed['category'],'').replace('.html.json','').replace('-',' ')
                            
                        
                            ## FILTERING OUT USELESS DATA ## 
                            
                            if (parsed['info'] != '') and ('bolzano' not in parsed['location'].lower()) and ('bz' not in parsed['location'].lower()) :
                            
                                        
                                ##### SISTEMA PRENOTAZIONE ONLINE #####
                                
                                if ('informazioni e prenotazioni biglietti in a' in parsed['info'].lower()) or \
                                    ('a (prenotazione online)' in parsed['info'].lower())  or ('biglietti, abbonamenti e modalità daccesso su a' in parsed['info'].lower()) \
                                        or ('info, biglietti e modalità di accesso in a' in parsed['info'].lower()) or \
                                            ('a il biglietto online' in parsed['info'].lower()) or ('prenotazione via mail' in parsed['info'].lower()): 
                                            parsed['cost']['has_ticket']['has_onlineBooking'] = True 

                                if ('informazioni su abbonamenti e biglietti'in parsed['info'].lower()) or \
                                     ('info e prenotazioni sul sito' in parsed['info'].lower()) or \
                                         ('modalità di iscrizioni in a' in parsed['info'].lower()) or \
                                             ("all'indirizzo a" in parsed['info'].lower()) or ('info e biglietti in a' in parsed['info'].lower()): 
                                     parsed['cost']['has_ticket']['has_onlineBooking'] = True 
                                if ('acquista a online' in parsed['info'].lower()) or ('informazioni su costi e biglietti a' in parsed['info'].lower()) \
                                    or ('inviare email a' in parsed['info'].lower()) or ('acquistando online' in parsed['info'].lower()) or \
                                        ('biglietteriaonline' in parsed['info'].lower()) or ('biglietteria online' in parsed['info'].lower()):
                                    parsed['cost']['has_ticket']['has_onlineBooking'] = True
                            try: 
                                parsed['description'] += '|' + parsed['info'] 

                                
                                
                            except KeyError:
                                parsed['description'] = parsed['info'] 

                            
                            info = parsed['info'].split()
                            if ('itemprop=startDate' in info) : 
                                data_inizio = info.index('itemprop=startDate')
                                data_fine = info.index('itemprop=endDate')
                                if (data_inizio and data_fine) or (data_inizio and not data_fine) : 
                                    parsed['duration'] = ' '.join(info[data_inizio+1:data_fine+1 or data_inizio+2] + parsed['duration']).replace('content=','').replace('itemprop=endDate','')
                           
                            del parsed['info']
                            
                            ## DESCRIPTION CLEANING ##

                            cleanse = ''
                            desc = parsed['description'].split()

                            for word in desc :
                                if ('=' not in word) and ('img' not in word) :
                                    cleanse += ' ' + word
                           
                            parsed['description'] = cleanse.replace('Dove:','').replace('Orario:','') 
                            
                            if (parsed['cost']['has_ticket']['has_price'] == '') :
                                if ('links' in parsed) :
                                    for l in parsed['links'] : 
                                        if ('booking' in l) or ('biglietti' in l) or ('book' in l) or ('purchase' in l) :
                                            if ('facebook' not in l) :
                                                parsed['cost']['has_ticket']['has_price'] = l 
                                        if ('event' in l) or ('category' in l) or ('spettacoli' in l) or ('calendar' in l) or ('content' in l) or ('facebook' in l):
                                            if ('link' not in parsed) :
                                                parsed['link'] = l
                                        else :
                                            if (len(parsed['links'])> 0) : 
                                                if (parsed['links'][0] == '#') :
                                                    parsed['has_link'] = parsed['links'][1] if ('mailto' not in parsed['links'][1]) else (parsed['links'][-2])
                                                else :
                                                    parsed['has_link'] = parsed['links'][-1]
                            if ('links' in parsed) :       
                                del parsed['links']

                            ## TARGET AGE AND EDITION ##
                            ta = []
                            parsed['has_target_age'] = ''
                            parsed['has_edition'] = 0
                            parsed['is_festival'] = False
                            parsed['language'] = None 
                            parsed['has_mode'] = None
                        

                        ## SISTEMO DURATION  + aggiungo ricorrenza se su più giorni x course event##
                        stagioni = set(['estate', 'inverno','primavera','autunno'])
                        giorni = set(['lunedì','martedì','mercoledì','giovedì','venerdì','sabato','domenica'])
                        mesi = set(['gennaio', 'febbario','marzo','aprile','maggio','giugno','luglio','agosto','settembre','ottobre','novembre','dicembre'])
                        seasonal = False
                        has_start = ''
                        has_end = ''
                        counter = 0
                        repeated = False
                        try:
                            duration = parsed['duration']
                            if (type(duration) != list) :
                                duration = duration.split()
                            for el in duration : 
                                if ('dalle' == el.lower()) :
                                    n = duration.index(el)
                                elif ('alle' == el.lower()) :
                                    m = duration.index(el)
                          
                                if ('.' in el) :
                                    p = el.index('.')
                                    if (el[:p].isnumeric()) and (el[p+1:].isnumeric()) :
                                        if (0 <= int(el[:p]) <= 7) or (int(el[p+1:]) not in set([15,30,25,0,45,40,55,50,35,10])) :
                                            if (has_start != '') and  (has_end == '') : 
                                                has_end = el[p+1:]
                                            elif (has_start == '') : 
                                                has_start = el[:p]
                                        else : 
                                            has_start += ' ' + duration[n:n+3]
                                            has_end += ' ' + duration[m:m+3]
                                if (el.lower() in giorni) :
                                    counter += 1
                                    if (counter > 1) : 
                                        repeated = True        
                                if ('-' in el) :
                                    check_date = el.split('-')
                                    if (len(check_date[0]) == 4) :
                                        if (has_start == '') :
                                            has_start = el 
                                        elif (has_start != '') and (has_end == '') :
                                            has_end = el 
                                        else:
                                            has_start = check_date[0]
                                            has_end = check_date[1]
                                if (el.lower() in stagioni) :
                                    seasonal = True 
                            parsed['has_start'] = has_start
                            parsed['has_end'] = has_end 
                            parsed['is_recurrent'] = repeated 
                            parsed['seasonal'] = seasonal
                            del parsed['duration']
                            
        
                        except:
                            
                            
                            try :
                                if (len(parsed['duration']) != 0 ) : 
                                    has_start = ' '.join(parsed['duration'])
                                check_description = parsed['description'].split()
                                
                                for el in check_description : 
                                    if (el.lower() == 'dalle') :
                                        n = check_description.index(el)
                                    if (el.lower() == 'alle') :
                                        m = check_description.index(el)
                                    if (el.lower() in mesi) : 
                                        if (has_start == '') : 
                                            idx_ = check_description.index(el) 
                                            has_start += ' '.join(check_description[idx_-1:idx_+1])
                                            if (n and m) :
                                                has_start += ' ' + ' '.join(check_description[n:n+3])
                                                has_end += ' ' + ' '.join(check_description[m:m+3])
                                            if (n and not m) :
                                                has_start += ' ' + ' '.join(check_description[n:n+3])
                                    if (el.lower().lstrip('u') in giorni) :
                                        counter += 1
                                        if (counter > 1) :
                                            repeated = True

                                    if (el.lower() in stagioni) :
                                        seasonal = True
                                parsed['has_start'] = has_start
                                parsed['has_end'] = has_end 
                                parsed['is_recurrent'] = repeated 
                                parsed['seasonal'] = seasonal
                                del parsed['duration']
                                    
                            except : 
                                pass
                            
                   
                try :
                    with open(os.path.join(self.writedir, parsed['name']) +'.json', 'w') as f : 
                        json.dump(parsed, f)   
                except :
                    self.scarti.append(parsed)              
                                 
    #def parse_for_tickets_ESN(self) :                    



                           





                               

                            
             ### TO DO ###
             # DURATION
             # FESTIVAL
             # EDITION
             # TITLE IN VARIE LINGUE
             # LANGUAGE
             # HAS_MODE              
                            

                            


         



landingr = r'C:\Users\Anna Fetz\Desktop\Data_Science\third_semester\KDI_2021\PARSING\scraped_websites\CRUSH\PARSED_CRUSHSITE'        
event = EventParser(dir, all_categories, {}, landingr )
event.fill_events_dict()
event.parse_for_tickets_CRUSHSITE()
#print(event.dict.keys())