import os, json, csv 
import pprint
from langdetect import detect_langs
from datetime import datetime, date
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
    
    def return_writer(self) :
        """Returns a new writer whenever needed"""
        writer = {'has_eventID':'',
            'has_title':'', 
            'has_type':'',
            'has_mode':None, 
            'has_cost': {
                'has_ticketID':'',
                'has_event':'',
                'has_freeEntrance': False,
                'has_onlineBooking': False, 
                'has_extraBenefits': "", 
                'has_totalPurchase': 0, 
                "has_price": "", 
                "has_currency": "EUR", 
                "has_purchaser": None
                        }, 
            "has_link": [], 
            "has_targetAge": "", 
            "has_edition": 0, 
            "has_festivalStatus": False, 
            "has_language": [], 
            "has_start": "", 
            "has_end": "", 
            "has_recurrency": False, 
            "has_organizer":"",
            "has_specialAnnouncements": "",
            "has_description" :"",
            "has_organizer": "",
            "has_terminated": False,
            "has_hashtag": [],
            "has_distance": False,
            "has_schedule": "",
            "has_transportMode": [],
            "has_venue":"",
            "has_virtualLocation":"",
            "has_superEvent":"",
            "has_terminated": False,
                            
            }
        return writer
   
    def fill_events_dict(self) :
        
        for current in self.listdir :
            
            if (current.endswith('.json')) :
                if (self.dir) in self.dict :
                    self.dict[self.dir].append(os.path.join(self.dir, current))
                else :
                    self.dict[self.dir] = [os.path.join(self.dir, current)]
            if (current.endswith('.csv')) :
                if (self.dir) in self.dict :
                    self.dict[self.dir].append(os.path.join(self.dir, current))
                else :
                    self.dict[self.dir] = [os.path.join(self.dir, current)]

            else : 
                dir = os.path.join(self.dir, current)
                try :
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
                except:
                    pass

    def parse_for_tickets_CRUSHSITE(self) :
        """Parses all crushsite events"""
        
        classes = ['danza-teatro', 'musica', 'cinema','didattica','incontri','mostre','iniziative-bambini']
        key = 'C:\\Users\\Anna Fetz\\Desktop\\Data_Science\\third_semester\\KDI_2021\\PARSING\\scraped_websites'
        mesi = ['gennaio','febbraio','marzo','aprile', 'maggio','giugno','luglio','agosto','settembre','ottobre','novembre','dicembre']
        giorni = ['lunedì','martedì','mercoledì','giovedì','venerdì','sabato','domenica']
        for item in self.dict[key] : 
            counter = 0
            if (item.endswith('.json')) : 
                with open(item, encoding='utf-8') as f : 
                    lo = json.load(f)
                    parsed = lo
                       
                   ## HAS START AND END FROM INFO AND DESCRIPTION
                        
                    writer = self.return_writer()
                    if ('description' in parsed) and ('info' in parsed) and ('location' in parsed) : 
                        # DESCRIZIONE + PROGRAMMAZIONE 
                       
                            
                        info = parsed['info']
                        if ('itemprop=startDate') in info :
                            info_lst = info.split()
                            i = 0
                            while (i < len(info_lst)-1) and ('itemprop=startDate' not in info_lst[i+1]) :
                                i +=1
                            writer['has_start'] = ''.join(info_lst[i]).replace('content=','')
                            writer['has_end'] = ''.join(info_lst[i+2]).replace('content=','') 
                        if ('itemprop=streetAddress' in info) :
                            info_lst = info.split()
                            while (i < len(info_lst)-1) and ('itemprop=streetAddress' not in info_lst[i+1]) :
                                i +=1
                            writer['has_venue'] = ' '.join(info_lst[i+1:i+10]).replace('content=','')
                        if ('ore' in info) :
                            info_lst = info.split()
                            i = 0
                            while (i < len(info_lst)-1) and ('ore' != info_lst[i+1]) :
                                i +=1
                            ora = ' '.join(info_lst[i+2:i+5])
                            if ('-' in ora) :
                                ora = ora.split('-')
                                writer['has_start'] += ' '  +ora[0] if (len(ora) >=1) else ' '
                                writer['has_end'] += ' ' + ora[1] if (len(ora) >1) else ' '
                            else :
                                ora = ora.split()
                                writer['has_start'] += ' ' + ora[0] if (len(ora) >=1) else ' '
                                writer['has_end'] += ' ' + '00:00' #Ipotesi che comunque finisca alla fine del giorno ()

                        if (writer['has_start'] == '') :
                            
                            desc = parsed['description'].split()
                            if ('title=' in ' '.join(desc)) :
                                i = 0
                                while (i < len(desc)-1) and ('title=' not in desc[i]) :
                                    i+=1
                                if ('Festival' in desc[i]) :
                                    writer['has_festivalStatus'] = True
                                if ('Stagione' in ' '.join(desc[i:])): 
                                    writer['has_schedule'] = 'Seasonal'
                                    
                                    writer['has_edition'] = int(desc[i][:-1].replace('title=','')) if desc[i][:-1].isnumeric() else 0
                                writer['has_organizer'] = ' '.join(desc[i:]).replace('title=','') #'Segnalato da
                            if ('dalle' in desc) and ('alle' in desc) :
                                i = 0
                                j = 0
                                while (i < len(desc)) and (desc[i] != 'dalle') : 
                                    i+=1
                                while (j < len(desc)) and (desc[j] != 'alle') : 
                                    j+=1
                                if ('.' in desc[i+1]) :
                                    idx_ = desc[i+1].index('.')
                                    if (desc[i+1][:idx_].isnumeric()) :
                                        writer['has_start'] = desc[i+1]
                                if ('.' in desc[j+1]) :
                                    idx_ = desc[j+1].index('.')
                                    if (desc[j+1][:idx_].isnumeric()) :
                                        writer['has_end'] = desc[j+1]
                                else:
                                    if (desc[i+1].isnumeric()) : 
                                        writer['has_start'] = desc[i+1]
                                    if (desc[j+1].isnumeric()) : 
                                        writer['has_start'] = desc[j+1]

                                writer['has_end'] = writer['has_end'].rstrip('.-:;)(')
                                writer['has_start'] = writer['has_start'].rstrip('.-:;)(')
                        
                            ## QUESTO E' PER LE ORE ORA GUARDA LA DATA
                            hours = parsed['duration_hours']

                            if (hours != 'Not specified') and (writer['has_start'] == ''):
                             
                                if (isinstance(hours,str)) : 
                                    hours = hours.replace(')','').split()
                                if (len(hours) == 1) :
                                    writer['has_start'] = hours[0]
                                    writer['has_end'] = '00:00'
                                elif (len(hours) == 2) :
                                    if ('-' not in hours[0]) :
                                        writer['has_start'] = hours[0]
                                        writer['has_end'] = hours[1]
                                    else :
                                        h = hours[0].split('-') #prendo un solo evento, dovrei prenderli tutti x il cinema
                                        writer['has_start'] = h[0]
                                        writer['has_end'] = h[1]
                                else :
                                    d = 0
                                    o = 0
                                    idx_1 = None
                                    idx_2 = None
                                    for el in hours :
                                        if (el.lower().replace('è','ì') in giorni) :
                                            d +=1 
                                        if (el == 'ore') :
                                            o += 1 
                                            if (o == 1) : 
                                                idx_ = hours.index(el)
                                                writer['has_start'] = hours[idx_+1]
                                            if (o == 2) :
                                                idx_ = hours.index(el)
                                                writer['has_end'] = hours[idx_+1]
                                        if (el == 'dalle') :
                                            idx_1 = hours.index(el) + 1
                                        if (el == 'alle') : 
                                            idx_2 = hours.index(el) +1 
                                        if (idx_1!= None and idx_2 != None) :
                                            writer['has_start'] = hours[idx_1]
                                            writer['has_end'] = hours[idx_2]
                                        if (idx_1 != None and idx_2 == None) or (idx_2 != None and idx_1 == None):
                                            if (idx_1 != None and hours[idx_1] not in set(['disposizioni', 'ore'])) or (idx_2 != None and hours[idx_2] not in set(['disposizioni','ore'])) : 
                                                writer['has_start'] = hours[idx_1] if (idx_1 != None) else (hours[idx_2])
                                                writer['has_end'] = '00:00'
                        if ( d > 1 ) :
                            writer['has_recurrency'] = True

                        l = writer['has_start'].split()
                        if (len(l) < 2) :
                            if (len(l) == 1) :
                                if ('-' in l[0]) :
                                    s = l[0].split('-')
                                    if (len(s[0]) < 4) :
                                        writer['has_start'] = s[0]
                                        writer['has_end'] = s[1]
                                else :
                                    if (':' in l[0]) or ('.' in l[0]) :
                                        writer['has_start'] = l[0]
                                        writer['has_end'] = '00:00'
                            if (len(writer['has_start']) <= 1) and (':' in writer['has_start']) or ('.' in writer['has_start']):
                                desc = parsed['description'].split()
                           
                                for i in range(len(desc)) :
                                    if (desc[i].lower() in mesi) :
                                        sp = desc[i-15:i+2]
                                
                                        for i in range(len(sp)-1) : 
                                            if (sp[i] not in ['1991', 'dal','al','dalle','a','oltre','alle','del','da','per','infatti','la']) :
                                                if (sp[i] == 'e') : # Becca solo i mesi
                                                    if (sp[i+1] in mesi and sp[i-1] in mesi) :
                                                        writer['has_recurrency'] = True
                                                        writer['has_schedule'] = 'monthly'
                                                if ('ore' in sp[i]) :
                                                    writer['has_schedule'] = 'weekly'
                                                    if (sp[i-1] in mesi) :
                                                        if (len(writer['has_start']) <= 5) :
                                                            writer['has_start'] = ' '.join(sp[i-2:i]) +' '+ writer['has_start']
                                                        if (len(writer['has_end']) <= 5) :
                                                            writer['has_end'] = ' '.join(sp[i-2:i]) +' '+ writer['has_end']
                        if (1< len(writer['has_start']) <= 5) :
                            desc = parsed['description'].split()
                            month_counter = 0
                            date = ''
                            for i in range(len(desc)-3) :
                                if (desc[i] in mesi) :
                                    period = desc[i-3:i+4]
                                   
                                    
                                    for dz in period :
                                        if (dz.isnumeric() and (len(dz) == 2)) or (dz in mesi and month_counter < 1) :
                                            if (dz not in date) :
                                                date += ' ' + dz
                                                if (dz in mesi) :
                                                    month_counter += 1
                                        if (month_counter >=2) :
                                            writer['has_recurrency'] = True
                                        if (type(dz[:-1]) == int) and (len(dz) <= 5) :
                                            date += ' ' + dz.strip(',.;:')
                            writer['has_start'] = date +' '+ writer['has_start'] 
                            writer['has_end'] = date + ' '+writer['has_end']
                        writer['has_start'] = writer['has_start'].replace(writer['has_end'],'')
                        # DATA FATTA ORA PENSA A LOCATION

                        writer['has_venue'] = writer['has_venue'].replace('itemprop=streetAddress','')
                        

                        loc = writer['has_venue'].split()
                        
                        
                               
                        c = ['(Tn)', 'Rovereto', 'Trento']
                        s = ['(Bz)','Merano', 'Bolzano', 'Innsbruck', 'Arco', 'Riva', 'Levico']
                        for e1, e2 in zip(s,c):
                           
                            if (e2 in loc) :
                                
                                writer['has_venue'] = ''.join(' '.join(loc).split(e2)[0]) +' ' + e2
                            if (e1 in loc) :
                                 writer['has_venue'] = ''
                        
                        if ('online' in loc) :
                            writer['has_virtualLocation'] = ' '.join(parsed['links']).replace('#','').split()[1] if ('https' in ' '.join(parsed['links']).replace('#','').split()[1]) else ' '.join(parsed['links']).replace('#','').split()[0]
                            writer['has_mode'] = 'online'
                        order = ('prim','second','terz','quart','quint','sest','settim','ottav','non','decim','undicesim')
                        ## ORA VADO AVANTI CON NOME ED EDIZIONE :
                        if ('edizione' in parsed['name'].lower()) :
                            name = parsed['name'].lower().split()
                            idx_ = name.index('edizione')
                            writer['has_edition'] = name[idx_-1].strip('°^')
                        if ('edizione' in parsed['description'].lower()) or ('stagione' in parsed['description'].lower()) :
                            desc = parsed['description'].lower().replace('\x92','').split()
                            for i in range(len(desc)) :
                      
                                if (desc[i].rstrip(',.:')[:-1] in order or  desc[i].rstrip(',.:')[:-1] in order) :
                                    if (desc[i+1] == 'stagione') or ('edizione'):
                                        for j in range(len(order)) :
                                            if (order[j] in desc[i]) :
                                                writer['has_edition'] = j+2
                                    
                                    if (desc[i+1] in giorni) :
                                        writer['has_schedule'] = ' '.join(desc[i:i+4]).strip(':;_.,')
                                        writer['has_recurrency'] = True 
                                      
                                    if ('stagione' in desc[i+2:]) :
                                        idx_ = desc[i+2:].index('stagione')
                                        if ('/' in desc[i+2:][idx_+1] or '-' in desc[i+2:][idx_+1]) :
                                            writer['has_edition'] = desc[i+2:][idx_+1]  #è da mettere stringa anche qui
                                if (desc[i] == 'edizione') :
                                    v = desc[i-1].lstrip('l')
                                    
                                    for j in range(len(order)) : 
                                        if (order[j] in v) :
                                            writer['has_edition'] = j+2
                                    if (writer['has_edition'] == 0) :
                                        writer['has_edition'] = v if (v != 'nuova') else 2 #AD HOC IPOTIZZO CHE SIA LA SECONDA
                                writer['has_schedule'] = 'yearly' if (writer['has_schedule'] == '') else writer['has_schedule']#standard per tutte e basta grazie
                        if ('fiera' in parsed['description'].lower() or 'festival' in parsed['description'].lower()) :
                            desc = parsed['description'].lower().replace('\x92','').split()
                            for i in range(len(desc)) :
                                if (desc[i] == 'fiera') :
                                    writer['has_festivalStatus'] = True #LA FIERA LA INTENDIAMO COME FESTIVAL
                                if (desc[i] == 'festival') :
                                    
                                    if ('coproduzione' in desc[:i] or 'collaborazione' in desc[:i]) :
                                        writer['has_superEvent'] = ''.join(desc[i:+5])
                                    if (desc[i-1] != 'al' and desc[i-1] != 'e' and desc[i-1] != 'dai') :
                                        writer['has_festivalStatus'] = True 
                      
                        ## ORA PROSEGUO CON VIRTUALLOCATION
                        desc = parsed['description'].replace('\x92','').lower().split()
                        if ('webinar' in desc) or ('online' in desc)  and ('online' not in writer['has_venue']):
                            
                            for j in range(len(desc)) :
                                if (desc[j] == 'webinar') :
                                    writer['has_virtualLocation'] = ' '.join(parsed['links']).replace('#','').split()[1] if ('https' in ' '.join(parsed['links']).replace('#','').split()[1]) else ' '.join(parsed['links']).replace('#','').split()[0]
                                    
                                if ('.' in desc[j] and desc[j][:desc[j].index('.')].isnumeric()) :
                                    if (writer['has_start'] == '') or (writer['has_start'] == 'precendenti,'):
                                        writer['has_start'] = desc[j]
                                if ('online' in desc[j] and 'prenot' not in desc[j-1] and 'privacy' not in desc[j-1] and 'acquist' not in desc[j-1]) :
                                    if ('sia' == desc[j-1])   :
                                        writer['has_mode'] = 'blended'
                                    else :
                                        writer['has_mode'] = 'online'
                                    writer['has_virtualLocation'] = ' '.join(parsed['links']).replace('#','').split()[1] if ('https' in ' '.join(parsed['links']).replace('#','').split()[1] and 'google' not in ' '.join(parsed['links']).replace('#','').split()[1]) else ' '.join(parsed['links']).replace('#','').split()[0]
                                    if ('google' in writer['has_virtualLocation']) :
                                       writer['has_virtualLocation'] = parsed['links'][2].rstrip('/a')
                        
                        info = info.lower().split()
                        
                        if ('webinar' in info) or ('online' in info)  and ('online' not in writer['has_venue']):
                            
                            for j in range(len(info)) :
                                if (info[j] == 'webinar') :
                                    
                                    if (writer['has_virtualLocation'] == "") :
                                        
                                        writer['has_virtualLocation'] = ' '.join(parsed['links']).replace('#','').split()[1] if ('https' in ' '.join(parsed['links']).replace('#','').split()[1]) else ' '.join(parsed['links']).replace('#','').split()[0]
                                    
                                if ('.' in info[j] and info[j][:info[j].index('.')].isnumeric()) :
                                    if ('tel' not in info[j-1:j]) and ('fax' not in info[j-1:j]) and ('n.' not in info[j-1:j]) : # QUI PER I CONTATTI !!
                                        if (writer['has_start'] == '') or (writer['has_start'] == 'precendenti,'):
                                            writer['has_start'] =info[j]
                                if ('online' in info[j] and 'prenot' not in info[j-1] and 'privacy' not in info[j-1] and 'acquist' not in info[j-1]) :
                                    if (info[j-1] not in mesi) :
                                        if ('sia' == info[j-1])   :
                                        
                                        
                                            writer['has_mode'] = 'blended'
                                        else :
                                            writer['has_mode'] = 'online'
                                        writer['has_virtualLocation'] = ' '.join(parsed['links']).replace('#','').split()[1] if ('https' in ' '.join(parsed['links']).replace('#','').split()[1] and 'google' not in ' '.join(parsed['links']).replace('#','').split()[1]) else ' '.join(parsed['links']).replace('#','').split()[0]
                        # VAI AVANTI CON TICKET 
                        info = ' '.join(info).replace('\x80', 'euro').split()
                        if ('ingresso gratuito' in parsed['info']) or ('ingresso libero' in parsed['info']):
                            writer['has_cost']['has_freeEntrance'] = True 
                        if ('prenotazione obbligatoria' in parsed['info']) or ('previa prenotazione' in parsed['info']) :
                            writer['has_specialAnnouncements'] = 'Prenotazione obbligatoria.'
                        if ('supplemento di' in parsed['info']) :
                            for i in range(len(info)):
                                if (info[i].lower() == 'euro') :
                                    writer['has_specialAnnouncements'] += ' ' + info[i]
                        if ('attestato di frequenza' in parsed['info']) :
                            freq = parsed['info'].split('/')[0]
                            writer['has_specialAnnouncements'] += ' ' + freq # QUESTO E' PER I WEBINAR !!!
                        if ('contributo' in parsed['info']) : 
                            writer['has_specialAnnouncements'] += ' ' + info[i] 
                        if ('online' in info and 'biglietto' in info) or ('online' in info and 'biglietti' in info) :
                            writer['has_cost']['has_onlineBooking'] = True 
                            if (writer['has_cost']['has_price'] == '') :
                                ticket_links = ' '.join(parsed['links']).replace('#','').split()
                                for t in ticket_links :
                                    if ('ticket' in t) or ('bigliett' in t) :
                                        save = t
                                        break
                                writer['has_cost']['has_price'] = save if save else parsed['links'][1]
                        
                        for i in range(len(info)-1) :
                            if (info[i] == 'euro') :
                                price = ''
                                if (info[i-1].isnumeric()) :
                                    price = info[i-1]
                                if (info[i+1].isnumeric()) :
                                    price = info[i+1]
                                writer['has_cost']['has_price'] = price
                                
                            if ('sconto' in info[i] or 'riduzion' in info[i] or 'ridotto' in info[i]) :
                                reduction = ' '.join(info[i-2:i+16]).replace('associativa','').replace('cristallo','').lstrip('./').lstrip(' / ')
                                reduction = reduction.replace(',','/').replace('(','/').replace(')','/')
                                reduction = reduction.split('/')
                            if (info[i] == 'ingresso' and info[i+1].isnumeric()) :
                                if (writer['has_cost']['has_price'] == '') :
                                    writer['has_cost']['has_price'] = info[i+1] 
                                for el in reduction :
                                    if ('sconto' in el) or ('riduzion' in el) or ('ridotto' in el) :
                                        writer['has_cost']['has_extraBenefits'] += ' ' + el
                                        break
                            
                        if (writer['has_venue'] != '') :
                            if (writer['has_cost']['has_price'] == '') and (writer['has_cost']['has_freeEntrance'] == False):
                                if (info[0] != 'img') :
                                    if ('/' in info) : 
                                        info = ' '.join(info).split('/') #CASO FACILE
                                        use = ""
                                        for i in range(len(info)-1) :
                                            if (info[i+1].rstrip().startswith('a')) :
                                                if ('euro' not in info[i]) :
                                                    for j in range(len(parsed['links'])) :
                                                        if ('https' in parsed['links'][j]) and ('ticket' in parsed['links'][j]) or ('https' in parsed['links'][j]) and ('bigliett' in parsed['links'][j]):
                                                            if (writer['has_cost']['has_price'] == ''):
                                                                writer['has_cost']['has_price'] = parsed['links'][j]
                                            if ('rido' in info[i+1]) :
                                                
                                                rid = info[i+1].split()
                                                k = 0
                                                while (k < len(rid)) and ('rid' not in rid[k]) :
                                                    k += 1
                                                if (len(rid[k:]) == 1) :
                                                    use = rid[:k+1]
                                                else :
                                                    if ('covid' not in ' '.join(rid[k:])) :
                                                        use = rid[k:]
                                            if ('grat' in info[i+1]) :
                                                rid = info[i+1].split()
                                                k = 0
                                                while (k < len(rid)) and ('grat' not in rid[k]) :
                                                    k += 1
                                                if (len(rid[k:]) == 1) :
                                                    use = rid[:k+1]
                                                else :
                                                    use = rid[k:]
                                            if ('costo' in info[i]) :
                                                writer['has_cost']['has_price'] = info[i].replace('costo:','').replace('unun',"un'un").replace('euro',' euro').replace('costo','').replace('. e', '. È').replace('.,',',').replace('allev',"all'ev")
                                                # CASO SPECIALE AD HOC
                                                if ('dal 6 agosto 2021' in info[i]) :
                                                    el = writer['has_cost']['has_price'].split('.')
                                                    writer['has_cost']['has_price'] = el[0]
                                                    writer['has_specialAnnouncements'] += ' '+el[-1]
                                        

                                        writer['has_cost']['has_extraBenefits'] += ' ' + ' '.join(use)
                                        if ('ingresso gratuito' in writer['has_cost']['has_price']) or (' ingresso libero' in writer['has_cost']['has_price']) :
                                            
                                            writer['has_cost']['has_freeEntrance'] = True 
                                            writer['has_cost']['has_extraBenefits'] = writer['has_cost']['has_price']
                                            writer['has_cost']['has_price'] = ''
                                    else :
                                        
                                        other = ' '.join(info)
                                        
                                        if ('ingresso gratuito' in other) or ('ingresso libero' in other) or ('entrata gratuita' in other) :
                                            
                                            writer['has_cost']['has_freeEntrance'] = True 
                                            writer['has_cost']['has_extraBenefits'] = info
                                            writer['has_cost']['has_price'] = ''
                                        if ('a' in info) and (writer['has_cost']['has_freeEntrance'] == False): 
                                            for el in parsed['links'] : 
                                                if ('ticket' in el) or ('bigliett' in el) :
                                                    writer['has_cost']['has_price'] = el
                                                    break
                                                if ('mailto'in el) :
                                                    writer['has_cost']['has_price'] = el.replace('mailto:','')
                                                    break
                                            if (writer['has_cost']['has_price'] == '') :
                                                writer['has_cost']['has_price'] = parsed['links'][1]
                             

                            # QUI X IL COVID 
                            info = ' '.join(info)
                            if ('green pass' in info) or ('covid' in info) or ('ottemperanza' in info) or ('6 agosto' in info) \
                            or ('normativa' in info) or ('mascherina' in info) or ('temperatura' in info):
                                el = info.replace('ingresso gratuito','').replace('entrata libera','').replace('ingresso libero','').replace(writer['has_cost']['has_price'],'')
                                if (type(writer['has_cost']['has_extraBenefits']) == list) :
                                    l = ' '.join(writer['has_cost']['has_extraBenefits'])
                                else :
                                    l = writer['has_cost']['has_extraBenefits']
                                    
                                el = el.replace(l,' ')
                                if (el.startswith(' p ')) or (el.startswith(' r ')) or (el.startswith(' i ')):
                                            
                                    el = el.replace('   ',',').split(',')
                                    el = ' '.join([e.replace(' ','') for e in el])
                                writer['has_specialAnnouncements'] = el.split()
                                nuovo = []
                                flag = False
                                counter = 0
                                for el in writer['has_specialAnnouncements'] : 
                                    n = el
                                    if (n.rstrip('.,:;') == 'a') and (counter == 0) :
                                        counter +=1
                                        for v in parsed['links'] :
                                            if ('google' not in v) :
                                                if ('prenot' in v) : 
                                                    n = el.replace('a', v).strip(';:;').replace('mailto:','')
                                                    flag = True
                                                elif (not flag and 'mailto' in v) :
                                                    n = el.replace('a','v').replace('mailto:','')
                                                    flag = True 
                                                else :
                                                    if ('google' not in parsed['links'][1]):
                                                        n = el.replace('a',parsed['links'][1].replace('mailto:',''))
                                                    else :
                                                        n = el.replace('a',parsed['links'][-1].replace('mailto:',''))    
                                                    flag = True 
                                                
                                    if (n.strip(':;.,') != 'a') :          
                                        nuovo.append(n.replace('/br','').replace('/a',''))
                                writer['has_specialAnnouncements'] = ' '.join(nuovo)
                            # STESSA COSA PER INFO TRENTINO + DESCRIZIONE 
                            info = info.split()
                            if ('orario:' in info) :
                                idx_ = info.index('orario:')
                                consider = info[idx_:]
                                
                                for i in range(len(consider)-2) :
                                    
                                    if ('dalle' == consider[i]) and ('alle' == consider[i+2]) :
                                        writer['has_start'] += ' ' + consider[i+1] if len(writer['has_start']) < 16  else ''
                                        writer['has_end'] += ' ' + consider[i+3] if len(writer['has_end']) < 16 else ''
                                   
                                    if ('dalle' != consider[i]) and ('alle' == consider[i+2]) :
                                        writer['has_start'] += ' ' + consider[i+3] if len(writer['has_start']) < 16 else ''
                            writer['has_start'] = writer['has_start'].rstrip(';:;.,')
                            ## PENSA A TICKET
                            special = []
                            desc = parsed['description'].replace('\x80','euro').replace('danticipo','di anticipo').replace('\x92',"'").split()
                            for i in range(len(desc)) :
                                counter = 0
                                if (desc[i] == 'massimo' and desc[i+2].strip(';.,:')  == 'persone') or (desc[i].strip(';.,:') == 'massimo' and desc[i+2].strip(';.,:')  == 'posti') :
                                    writer['has_specialAnnouncements'] += ' '.join(desc[i-7:i+3])
                                if (desc[i].lower() == 'euro') : 
                                    counter +=1 
                                    
                                    if (desc[i+1][0].strip(';:.,').isnumeric()) : 
                                    
                                       
                                        if (writer['has_cost']['has_price']  == '') :
                                            writer['has_cost']['has_price'] = desc[i+1]
                                    else :
                                        if (desc[i-1][0].strip(';:.,').isnumeric()) :
                                            if (writer['has_cost']['has_price']  == '') :
                                                writer['has_cost']['has_price'] = desc[i-1]
                                    if (counter > 1) :
                                        special.extend(desc[i-2:i+2])
                                writer['has_specialAnnouncements'] += ' '+ ' '.join(special)

                                if ('ridotto' in desc[i] or 'grat' in desc[i] or 'bambin' in desc[i]) :
                                    writer['has_cost']['has_freeEntrance'] = True 
                                    if ('prenotazione' in ' '.join(desc)) :
                                        writer['has_specialAnnouncements'] = 'Online Booking Required'
                            if (writer['has_cost']['has_price'] == '') and (writer['has_cost']['has_freeEntrance'] == False) : 
                                
                                for i in range(len(parsed['links'])) : 
                                    if ('google' not in parsed['links'][i] and 'https' in parsed['links'][i]) :

                                        if ('bigliett' in parsed['links'][i] or 'ticket' in parsed['links'][i] or 'prenot' in parsed['links'][i]) :
                                            writer['has_cost']['has_price'] = parsed['links'][i]
                                        else :
                                            if ('#' not in parsed['links'][i]) and ('https' in parsed['links'][i]) :
                                                writer['has_cost']['has_price'] = parsed['links'][i]
                                writer['has_cost']['has_onlineBooking'] = True

                            ## INFORMAZIONI COVID 
                            if ('prenotazione obbligatoria' in ' '.join(desc)) or ('anticipo' in ' '.join(desc)) :
                                writer['has_specialAnnouncements'] = 'Mandatory online Booking.'
                                if ('anticipo' in ' '.join(desc)) :
                                    idx_ = desc.index('anticipo')
                                    writer['has_specialAnnouncements'] +=' ' + ' '.join(desc[idx_-9:idx_+1])
                            
                            if ('online' in writer['has_venue']) :
                                writer['has_venue'] = ' '
                            if (writer['has_virtualLocation'] != '') :
                                writer['has_mode'] = 'online'
                            if (writer['has_venue'] != '') :
                                if (writer['has_mode'] != 'blended') :
                                    writer['has_mode'] = 'offline'
                            if (writer['has_mode'] == 'offline' and writer['has_virtualLocation'] != '') :
                                writer['has_mode'] = 'online'
                            writer['has_description'] = parsed['description'].replace(writer['has_specialAnnouncements'],'').replace(writer['has_cost']['has_extraBenefits'],'').replace('br/',' ').replace('\x92',"' ").replace('/','').split()
                            k = 0
                            while (k < len(writer['has_description']) and writer['has_description'][k] != 'segnalato') :
                                k += 1
                            writer['has_description'] = ' '.join(writer['has_description'][:k-1])
                            if (writer['has_description'][-1] == 'a') :
                                writer['has_description']=  (writer['has_description'][:-1] + ' ' + parsed['links'][1]).replace('pInformazioni:', '')
                            writer['has_description'] = writer['has_description'].replace('pInformazioni:', '')
                            
                            ## CERCA TARGET AGE 
                            if ('settimanale' in ' '.join(desc)) :
                                writer['has_schedule'] = 'weekly'
                                writer['has_recurrency'] = True 
                            
                            
                            if ('anni' in ' '.join(desc)) :
                                for i in range(len(desc)) :
                                    if ('anni' in desc[i]) :
                                        if (desc[i-1][0].isnumeric()) :
                                            if ('degustazione' not in desc[i-4]) :
                                                writer['has_targetAge'] = ' '.join(desc[i-4:i+1]).replace('e i', '-').replace('anni','').strip('?;.,!:').replace('gratuite per giovani ',' ').strip(' ')
                                                if ('gratuite per giovani' in desc) :
                                                    writer['has_cost']['has_extraBenefits'] = desc[i-4:i+1]
                    
                            ## Sistemo le date
                            if (len(writer['has_start'].lstrip(' ')) < 12) :
                 
                                if (len(writer['has_start']) == 6) or (len(writer['has_start']) == 5):
                                   
                                    
                                    idx1 = info.index('itemprop=startdate')
                                    start = info[idx1-1].replace('content=','')
                                    idx2 = info.index('itemprop=enddate')
                                    end = info[idx2-1].replace('content=','')
                                    writer['has_start'] = start +' ' + writer['has_start']
                                    writer['has_end'] = end +' ' + writer['has_end']
                                    
                                    
                                else :
                                    if ('-' in writer['has_start']) :
                                        for i in range(len(info)) :
                                            if (info[i] == 'dalle') and (info[i+1][0].isnumeric()) :
                                                writer['has_start'] += ' ' + info[i+1]
                                            if (info[i] == 'alle') and (info[i+1][0].isnumeric()) :
                                                writer['has_end'] += ' ' + info[i+1]
                                    else :
                                        writer['has_start'] = writer['has_start'][:5]
                                        idx1 = info.index('itemprop=startdate')
                                        start = info[idx1-1].replace('content=','')
                                        idx2 = info.index('itemprop=enddate')
                                        end = info[idx2-1].replace('content=','')
                                        writer['has_start'] = start +' ' + writer['has_start']
                                        writer['has_end'] = end +' ' + writer['has_end']      
                                if ('.' in writer['has_end']) :
                                    writer['has_end'] += '.00'                
                                if ('.' not in writer['has_end']) :
                                    writer['has_end'] += ' 00:00:00'
                                writer['has_end'] = writer['has_end'].replace('.',':')
                            # TITLE
                            name = ' '.join(info[info.index('width=128/')+1:info.index('itemprop=name')]).replace('content=','').replace('=',' ').replace('/','')
                            if (name[0].isnumeric()) or ('festival' in name):
                                writer['has_edition'] = name[:2]
                                writer['has_recurrency'] = True
                                writer['has_schedule'] = 'yearly'
                            name = name.replace(' ','-').strip(',').strip('^')
                            writer['has_title'] = name
                            writer['has_language'].append('it-IT')
                            if (len(writer['has_link']) == 0) :
                                if ('#' not in parsed['links']) :
                                    writer['has_link'] = parsed['links'][0]
                                elif ('#' in parsed['links'][0]) and ('google' not in parsed['links'][1]) :
                                    writer['has_link'] = parsed['links'][1]
                            # ORGANIZZATORE 
                            try:
                                o1 = info.index('itemprop=name')
                                o2 = info.index('itemprop=organizer')
                                use = ' '.join(info[o1+1:o2]).replace('content=','').replace('=','')
                            except:
                                use = ' '.join(info[info.index('dove:')+1:-2]).replace('itemprop=streetaddress','')
                            writer['has_organizer'] = use.strip(',.')
                            
                            # FILTRO 
                            if ('Roncegno Terme' not in writer['has_venue']) and ('Riva' not in writer['has_venue']) and ('Levico Terme' not in writer['has_venue']) \
                                and ('Folgaria' not in writer['has_venue']) and ('Pinzolo' not in writer['has_venue']) and ('Nomi' not in writer['has_venue']):
                               
                                
                                writer['has_end'] = writer['has_end'].replace('.',':')
                                new = []
                                for el in writer['has_end'].split() :
                                    

                                    if (el not in new) :
                                        v = el
                                        if (len(el) == 5) :
                                            v = el + ':00'
                                        new.append(v)
                                writer['has_end'] = ' '.join(new)
                         
                                if self.has_terminated(writer['has_end']) :
                                    writer['has_terminated'] = True
                               
                          
                                try :
                                    print('Writing {} to .json file'.format(writer['has_title']))
                                    self.write_to_json(os.path.join(self.writedir, name), writer)
                            
                                except :
                                    print('Appending {} to scarti list'.format(writer['has_title']))
                                    self.scarti.append(writer)              
                                 
    def parse_for_tickets_ESN(self) :    

        """parses all ESN events"""
        key = 'C:\\Users\\Anna Fetz\\Desktop\\Data_Science\\third_semester\\KDI_2021\\PARSING\\scraped_websites'
        for item in self.dict[key] : 
            writer = self.return_writer()
            if (item.endswith('JSON'))  : 
                sp = item.split('\\')
                if ('ESN' in sp[-2]) :
                    
                    for el in os.listdir(item) :
                        
                            
                        with open(os.path.join(item, el), encoding ='utf-8') as f:
                            loaded = json.load(f)
                            parsed = loaded 
                            ## STARTING WITH START AND END DATE ##
                            if (len(parsed['duration_hours']) != 0) and (len(parsed['duration_days']) != 0) :

                                duration_hours =  ''.join(parsed['duration_hours']).split()
                                if ('to' in duration_hours) :
                                    duration_hours = ' '.join(duration_hours).split('to') 
                                    writer['has_start'] = ' '.join(parsed['duration_days']) + ''.join(duration_hours[0])
                                    writer['has_end'] = ' '.join(parsed['duration_days']) + ''.join(duration_hours[-1])
                                elif ('to' in parsed['duration_days']) : 
                                    duration_days = ' '.join(parsed['duration_days']).split('to') 
                                    writer['has_start'] = ' '.join(duration_days[0]) + ' '.join(duration_hours)
                                    writer['has_end'] = ' '.join(duration_days[-1]) + ' '.join(duration_hours)
                                else :
                                    writer['has_start'] = ' '.join(parsed['duration_days']) + ' '.join(parsed['duration_hours'])
                                    writer['has_end'] = ' '.join(parsed['duration_days']) + ' '.join(parsed['duration_hours'])
                            writer['has_end'] = writer['has_end'].replace(writer['has_start'],'')
                            #Nell'else c'è welcome week senza info quindi no ELSE -> INUTILE

                            # Sistema recurrency
                            if ('recurrency' in parsed) : 
                                if (len(parsed['recurrency']) == 1) and (parsed['recurrency'][0] in parsed['duration_days']) :
                                    writer['has_recurrency'] = False
                                elif (len(parsed['recurrency'])> 1) :
                                    if (parsed['recurrency'][1] != parsed['duration_days']) and ('/' in parsed['recurrency'][1])  :
                                        
                                        writer['has_end'] = parsed['recurrency'][1] 
                            ## Sistema Ticket ##
                            ## DA FARE - METTICI IL LINK ALL'EVENTO
                            if ('description' in parsed) : 
                                desc = parsed['description'].replace('data-colorbox-gallery','').replace('gallery-node-30899-qFu866oJO6M','').replace('\x80','euro').replace('8hfj2-0-04','').replace('377hq-0-0','').replace('7fvej-0-0','').replace('4cab4-0-0','').replace('c4vmi-0-0','').replace('a6tp-0-0','').replace('cr2sm-0-0','')
                                to_replace = set(['group-image','Needed to activate contextual links class','text-align:justifyspan', 'style', 'background-color:transparent;', 'font-family:calibri;', 'font-size:16pxsleeping', 'bag;',
                                'gallery-node-30962-VGyNKh2S3W8','date-display-end', 'href', 'UFvb8DNH','colorbox','data-cbox-img-attrs',
                                'text-align:justifyspan',"'{title: , alt: }'",'date-display-single','data-editor','textformatter-listli class','IwAR2mH2Ow9zs3_ZLTipYXX', 'title img alt src OYhmWIWH title ','style', 'background-color:transparent;', 'font-family:calibri;', 'font-size:16pxT-shirt','gallery-node-30963-4zolJBOl7cU  SQjZyuWL title img alt src kdC0Nz-W title '])
                                for el in to_replace :
                                    desc = desc.replace(el,'')
                                split = desc.split()
                                new = []
                                for el in split:
                                    if ('-' not in el) or ('img' not in el) or ('class' not in el) :
                                        new.append(el.rstrip('/p').rstrip('a'))
                                desc = new
                                if ('euro' in desc) or ('Euro' in desc) or ('biglietto' in desc) or ('Biglietto' in desc)\
                                    or ('ticket' in desc) or ('Ticket' in desc) or ('fee' in desc) or ('subscription' in desc) \
                                        or ('iscrizione' in desc) or ('ingresso' in desc) or ('Ingresso' in desc) or ('pagamento' in desc): 
                                        for el in desc: 
                                            if (el.lower() in set(['ingresso','pagamento','euro','biglietto','ticket','fee','iscrizione','subscription'])) :
                                                idx_ = desc.index(el)
                                                writer['has_cost']['has_price'] = desc[idx_-1:idx_+10]
                                                
                                if ('NB:' in desc) :
                                    idx_ = desc.index('NB:') 
                                    writer['has_specialAnnouncements'] = ' '.join(desc[idx_:])
                                    
                                for el in desc :
                                    if ('covid' in el.lower()) or ('green pass' in el.lower()) or ('assembramenti' in el.lower()) \
                                        or ('mascherin' in el.lower()) :
                                        idx_ = desc.index(el)
                                        writer['has_specialAnnouncements'] += ' ' + ' '.join(desc[idx_:])
                                    if ('free'in el.lower()) or ('gratuito' in el.lower()) or ('gratis' in el.lower()) :
                                        writer['has_cost']['has_freeEntrance'] = True 
                                    if ('included' in el.lower()) or ('inclus' in el.lower()) :
                                        idx_ = desc.index(el)
                                        writer['has_cost']['has_extraBenefits'] = ' '.join(desc[idx_-10:idx_+10]).replace('/li','').replace('/ul','')
                                    if (el.isupper() and el != 'DOSS' and el != 'BBQ' and el != 'ESN') :
                                        idx_ = desc.index(el)
                                        writer['has_specialAnnouncements'] += ' ' + ' '.join(desc[idx_-10:idx_+10])
                                if ('for more info' in ' '.join(parsed['description'])) : 
                                    if (writer['has_cost']['has_price'] == '') and (writer['has_cost']['has_freeEntrance'] == False) :
                                        writer['has_cost']['has_price'] = parsed['link'][0]
                                if ('postponed' in ' '.join(parsed['description'])) or ('posticipato' in ' '.join(parsed['description'])) :
                                    idx_ = parsed['description'].index('postponed') 
                                    writer['has_specialAnnouncements']  += ' ' + ' '.join(parsed['description'][idx_-10:])   
                                if (writer['has_cost']['has_price'] != '') :
                                    writer['has_cost']['has_freeEntrance'] = False
                                writer['has_description'] = ' '.join(desc).replace(writer['has_specialAnnouncements'],'').replace(' '.join(writer['has_cost']['has_price']),'').replace(' '.join(writer['has_cost']['has_extraBenefits']),'')
                                # SET LANGUAGE #
                                
                                writer['has_language'] = ['it-IT', 'en-GB']
                                writer['has_title'] = parsed['name']
                                consider = []
                                n = writer['has_title'].replace('trento','').replace('bolzano','').replace('verona','').split('-')
                                if (n[0] == 'esn') :
                                    consider = n[1:]
                                if (n[-1] == 'esn') :
                                    consider = n[:-1]
                                if ('edition' in n) :
                                    idx_ = n.index('edition')
                                    writer['has_edition'] = n[idx_-1:idx_]
                                if (consider != []):
                                    writer['has_type'] = n[:2]
                                else :
                                    writer['has_type'] = n[:2]
                                writer['has_venue'] = ' '.join(parsed['location'])
                        
                        

                            ## FURTHER CLEANING 
                            new_desc = []
                            if ('class' in writer['has_description']) :
                                desc = writer['has_description'].split()
                                for i in range(len(desc)) :
                                    if ('-' not in desc[i]) and ('class' != desc[i]) and ('title' != desc[i]) and ('_' not in desc[i]) :
                                        if ('img' != desc[i]) and ('alt' != desc[i]) and ('src' != desc[i]) and ('country' not in desc[i]):
                                            if (desc[i].rstrip('/') != 'li') and (desc[i] != 'ul'):
                                                new_desc.append(desc[i].strip('/').replace('[/url]','').replace('\x92',"'").replace('strong',''))
                            to_replace = set(['X8jYzjkN', 'dblnMbuw&amp;c', '92d4a68efec566a4d792774e86f94cb7', '9yaRdkWn', 't4Hrk5u5', 'HIDqw01z','rg4CCXQ4',
                            'vaQFMnMJ', '2922d5a89fad89732c791c080a366b93', 'KtRHVBHP', 'f268b2ba8ebab55992b31a9b95a110cc','m16kMcg2', 'M0M1I6jy', 'qo1bbcxm', '0QUhk9cK',
                            'PueO5saP&amp;c', '9c773c95174a64a105e7063766b6029f','tiq1BNiv&amp;c', 'd5c762b61c41d41483f1c3d7e4a23004','pZXEIpN5', 'ZJtEBKY6','BklrsnR1', 'VaNhpuw5',
                            'pufXmM6s','oTe4WuKx', '7MJbcPO4', '', 'o9v6fnle', 'cxmmr5t8', 'oygrvhab', 'hcukyx3x', 'c1et5uql','slr8FqY', '7f8oVRF','j5onWS5H','vewj36iq','M8soQvT',  '.../aspan)',
                            'HOUlLqWY','SQjZyuWL','...)','ltr','h4','h3','/li','emoji sunny:sunny:','yUiAND6m', 'emoji', 'mushroom:mushroom:',
                            ']www.trentodoc.com/en/http://www.trentodoc.com/en/]www.trentodoc.com/en/ ','ehvca-0-0','3f4u6-0-0','3f4u6-0-0','duj81-0-0',
                            'f8ak7-0-0','f8ak7-0-0','9qfek-0-0','697nq-0-0','697nq-0-0','7t761-0-0 4hc0g-0-0','4hc0g-0-0***','698ps-0-0','bi8et-0-0','bi8et-0-0',
                            'e96pc-0-0',' f8ak7-0-0','f8ak7-0-0','9qfek-0-0','697nq-0-0','697nq-0-0','7t761-0-0 4hc0g-0-0 class ','4hc0g-0-0***','li font-size:16pxsome font-size:16pxsome',
                            'li font-size:16px','/strong ul dir'])

    
                        
                            new_desc = ' '.join(new_desc)
                            
                            for el in to_replace :
                                new_desc = new_desc.replace(el, '')
                                writer['has_specialAnnouncements'] = writer['has_specialAnnouncements'].replace(el,'')
                            writer['has_description'] = new_desc.replace(writer['has_end'],'').replace(writer['has_start'],'').lstrip(' ul')
                            
                            writer['has_end'] = writer['has_end'].replace('class','').rstrip(' ')
                            writer['has_start'] = writer['has_start'].rstrip(' ')

                            if (writer['has_end'] == '') :
                                writer['has_end'] = writer['has_start'][:10] + ' 00:00:00'
                            else :
                                writer['has_end'] +=':00'
                                writer['has_end'] = writer['has_end'].replace('-', '')
                            if (len(writer['has_start']) < 18) :
                                writer['has_start'] +=':00'
                            if ('/' in writer['has_end']) :
                                writer['has_end'] = datetime.strptime(writer['has_end'], "%d/%m/%Y %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
                                writer['has_start'] = datetime.strptime(writer['has_start'], "%d/%m/%Y %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
                            if ('-' in writer['has_end']) : 
                                writer['has_end'] = datetime.strptime(writer['has_end'], "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
                                writer['has_start'] = datetime.strptime(writer['has_start'], "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")

                            if (self.has_terminated(writer['has_end'])) :
                                writer['has_terminated'] = True 
                            # CHECK RECURRENCY 
                            if ('2018' in writer['has_title']) or ('2019' in writer['has_title']) or ('2020' in writer['has_title']) :
                                writer['has_recurrency'] = True 
                                writer['has_schedule'] = 'yearly'
                            if ('edition' in writer['has_title']) :
                                title = writer['has_title'].split('-')
                                idx_ = title.index('edition') 
                                n = title[idx_-1]
                                writer['has_edition'] = n
                            
                    
                            
                            if (' '.join(writer['has_cost']['has_price']) == '') :
                                writer['has_description'] = writer['has_description'].replace('lastE','last E').replace('lastB', 'last B').replace('ul', '').replace('lastA','last A')
                                writer['has_cost']['has_freeEntrance'] = True 
                            
                            writer['has_link'] = 'https://trento.esn.it/?q=events'+'/'+writer['has_title']
                                        
                        
                
                            writer['has_type'] = ' '.join(writer['has_type']) if (type(writer['has_type']) == list) else writer['has_type']
                            writer['has_cost']['has_price'] = ' '.join(writer['has_cost']['has_price']) if (type(writer['has_cost']['has_price']) == list) else writer['has_cost']['has_price']
                            writer['has_hashtag'] = parsed['links'] if ('link' in parsed) else []
                            writer['has_organizer'] = 'ESN'
                            #MODE
                            if ('zoom' in writer['has_venue'].lower() or 'teams' in writer['has_venue'].lower()) :
                                writer['has_venue'] = 'Trento, Italy'
                                writer['has_virtualLocation'] = writer['has_link']
                                writer['has_mode'] = 'online'
                            elif ('zoom' not in writer['has_venue'] and 'teams' not in writer['has_venue']):
                                new_loc = []
                                for el in writer['has_venue'].split() :
                                    if (el != 'will' and el != 'in' and el != 'before' and el != 'to' and el != 'at' and el!= 'on') :
                                        if (el.lower() not in new_loc) :
                                            new_loc.append(el.replace('?',''))
                                writer['has_mode'] = 'offline'
                            writer['has_venue'] = ' '.join(new_loc)
                        
                            if ('Trento' not in writer['has_venue'].lower()) :
                                writer['has_venue'] = writer['has_venue'] +' (Trento)'

                            for v1,v2,v3,v4 in zip(writer['has_cost']['has_price'].split(), writer['has_specialAnnouncements'].split(), writer['has_cost']['has_extraBenefits'].split(), writer['has_description'].split()) :
                                if (v1.lower() == 'train') or (v2.lower() == 'train') or (v3.lower() == 'train') or (v4.lower() == 'train')  :
                                    writer['has_transportMode'].append('Train')
                                if (v1.lower() == 'bus') or (v2.lower() == 'bus') or (v3.lower() == 'bus') or (v4.lower() == 'bus') :
                                    writer['has_transportMode'].append('Bus')
                                if (v1.lower() == 'car') or (v2.lower() == 'car') or (v3.lower() == 'car') or (v4.lower() == 'car') :
                                    writer['has_transportMode'].append('Car')
                            writer['has_transportMode'] = list(set(writer['has_transportMode']))
                        
                        ## DEVI SISTEMARE TICKET  !!!
                            try :
                                print('Writing {} to .json file'.format(writer['has_title']))
                                self.write_to_json(os.path.join(self.writedir, writer['has_title']), writer) 
                            except :
                                self.scarti.append(writer)   

    def parse_for_tickets_STAY(self) : 
        
        """parses all  STAY HAPPENING  events"""
        key = 'C:\\Users\\Anna Fetz\\Desktop\\Data_Science\\third_semester\\KDI_2021\\PARSING\\scraped_websites'
        for item in self.dict[key] : 
           
            if (item.endswith('JSON'))  : 
                sp = item.split('\\')
                if ('STAY' in sp[-2]) :
                    
                    for el in os.listdir(item) :
                        writer = self.return_writer()
                        
                        mesi = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04',
                                'May':'05','Jun':'06','Jul':'07','Aug':'08',
                                'Sep':'09','Oct':'10','Nov':'11','Dec':'12'}
                        with open(os.path.join(item, el), encoding ='utf-8') as f:
                            loaded = json.load(f)
                            parsed = loaded    
                            ## TAGS FOR CATEGORY AND LINKS
                            if ('tags' in parsed) : 
                                writer['has_type'] = parsed['tags'][-2].replace('float-left">','') +' '+ parsed['tags'][2].replace('href=','')
                            ## DURATION DAYS 
                            if (len(parsed['duration_days']) == 8) : 
                                writer['has_start'] = ' '.join(parsed['duration_days'][1:4]).replace('h6">','').split()
                                writer['has_start'][0] = mesi[writer['has_start'][0]]
                               
                                
                                writer['has_end'] =' '.join(parsed['duration_days'][5:]).split()
                                writer['has_end'][0] = mesi[writer['has_end'][0]]
                             
                            else :
                                writer['has_start'] = ' '.join(parsed['duration_days'][1:]).replace('h6">','').split()
                                writer['has_start'][0] = mesi[writer['has_start'][0]]
                    
                            writer['has_start'][0] , writer['has_start'][1] = writer['has_start'][1] , writer['has_start'][0]
                            if (len(writer['has_end']) > 0) : 
                                writer['has_end'][0] , writer['has_end'][1] = writer['has_end'][1] , writer['has_end'][0]
                               
                                   
                            #writer['has_start'] = datetime.strptime('/'.join(writer['has_start']), "%d/%m/%Y")
                            ## DURATION HOURS 
                            writer['has_start'] += parsed['duration_hours']
                            writer['has_end'] += parsed['duration_hours'] if (writer['has_end'] != '') else str(parsed['duration_hours'])
                            writer['has_start'] = ' '.join(writer['has_start'])
                            writer['has_end'] = ' '.join(''.join(writer['has_end']).replace('[','').replace(']','').split()) if type(writer['has_end'] == list) else ' '.join(writer['has_end'])
                            ## FIX DESCRIPTION AND FURTHER ANNOUNCEMENTS 
                            clean = set(['<article style="word-break: break-all;word-break: break-word;">','<img alt=',
                            'class="img-fluid rounded hover-translate-y-n3 hover-shadow-lg mb-4" height="274" src="https://cdn.stayhappening.com/events2/banners/f0ac06d52e123cb5d05d106344879bf5cba092f062d89b134e30d839d42dc3fb-rimg-w720-h274-gmir.png?v=1634999771" style="width: 100%;min-height: 150px;" width="720"/> ',
                            '<article style="word-break: break-all;word-break: break-word;">','class="img-fluid rounded hover-translate-y-n3 hover-shadow-lg mb-4" height="350" src="https://cdn.stayhappening.com/events5/banners/d3b18867332b2fb6b849ad3ac87c8b36d98271c696790652657cf570c562aa1b-rimg-w526-h350-gmir.jpg?v=1634999785" style="width: 100%;min-height: 150px;" width="526"/>',
                            'word-break', 'break-all','style="width: 100%;min-height: 150px;" width="526"/>','class="img-fluid rounded hover-translate-y-n3 hover-shadow-lg mb-4" height="394"',
                            'src="https://cdn.stayhappening.com/events5/banners/e88dc297f5d2b4f4da7ba1c9afc288469a58e5955fe29623373c7727192b8cdb-rimg-w526-h394-gmir.jpg?v=1634952509"',
                            'style="width: 100%;min-height: 150px;" width="526"/> '])
                            
                            

                            if ('description' in parsed) : 
                                for el in clean :
                                    parsed['description'] = parsed['description'].replace(el,'')
                                desc = parsed['description'].lower().replace('</p>','').replace('<br/>','').replace('<p>','').replace('<article style=": ;: break-word;">','').split()
                                new = []
                                for el in desc :
                                    if ('covid' in el.lower()) or ('green pass' in el.lower()) or ('assembramenti' in el.lower()) \
                                    or ('mascherin' in el.lower()) or ('normativ' in el.lower()) or ('rimborso' in el.lower()) or ('escluso' in el.lower()):
                                        idx_ = desc.index(el)
                                        
                                        writer['has_specialAnnouncements'] += ' ' + ' '.join(desc[idx_-5:]).replace('</p>','').replace('<br/>','').replace('<p>','')
                                    if ('src' not in el) and ('height=' not in el) and ('<' not in el) and ('>' not in el) \
                                        and ('width:' not in el) and ('height:' not in el) and ('=' not in el):
                                        new.append(el)
                                    if ('edizione' in el) or ('edition' in el) :
                                        idx_ = desc.index(el)
                                        writer['has_edition'] = desc[idx_-1:idx_+4] 
                                desc = ' '.join(new).lower().split()
                                if ('costo' in desc) :
                                    for el in desc :
                                        if (el == 'costo') and (desc[desc.index(el)+1].isnumeric()) :
                                            writer['has_cost']['has_price'] = desc[desc.index(el)+1] + 'euro'
                                if ('euro' in desc) or ('prezzo' in desc) : 
                                    for el in desc :
                                        if (el == 'euro') or (el =='prezzo') and (desc[desc.index(el)+1].isnumeric()) or (desc[desc.index(el)-1].isnumeric()) :
                                            writer['has_cost']['has_price'] = desc[desc.index(el)-1] + 'euro'+ desc[desc.index(el)+1] 
                                if ('sconto' in desc) or ('scontato' in desc) or ('ridotto' in desc) or ('riduzione' in desc)  :
                                    for el in desc :
                                        if ('sconto' in el) or ('scontato' in el) or ('ridotto' in el) or ('ridotto' in el) :
                                            writer['has_cost']['has_specialBenefits'] = desc[desc.index(el)-2:desc.index(el)+5]
                                        if (desc.index(el)+1 == 'online') :
                                            writer['has_cost']['has_onlineBooking'] = True 
                                if ('biglietteria online' in desc) or ('biglietto online' in desc) or ('prenotazione online' in desc) :
                                    writer['has_cost']['has_onlineBooking'] = True
                                if ('prenotazione gratuita' in desc) or ('biglietto gratuito' in desc) or ('ingresso gratuito' in desc) : 
                                    writer['has_cost']['has_freeEntrance'] = True 
                                else :
                                    if (writer['has_cost']['has_price'] == '') :
                                        writer['has_cost']['has_price'] = parsed['links'][-1].replace('data-url=','').replace('></div>','')
                                writer['has_description'] = parsed['description']
                            writer['has_venue'] = parsed['location']
                            if (len(writer['has_description']) > 0) :
                                
                                writer["has_language"] = detect_langs(writer['has_description'])
                                writer['has_language'] = str(writer['has_language']).replace('[','').replace(']','').split(',')
                                writer['has_language'] = [el.split(':')[0] +'-'+ el.split(':')[0].upper() for el in writer['has_language']]
                                
                            
                            ### FURTHER DETAILS FOR DISCOUNTS OR SUPEREVENTS
                            # LINK 
                            writer['has_link'] = parsed['links'][-1].replace('data-url=','').replace('></div>','') if len(parsed['links']) > 0 else ''
                            if (writer['has_link'] == '') and (len(writer['has_title']) > 0) :
                                writer['has_link'] = writer['has_title'][-1]
                            
                            ## check whether there are info :
                            if ('name' in parsed) : 
                                writer['has_title'] = parsed['name'].replace('csv','')
                            # DISCOUNTS 
                            clean = writer['has_description'].split()
                            to_replace = ['<br/>', '<article style=":',';:', 'break-word;">']
                            for el in to_replace :
                                writer['has_description'] = writer['has_description'].replace(el,'')
                            new = []

                            for word in clean:
                                if ('class=' not in word) and ('src=' not in word) and ('-' not in word) and ('&' not in word) and ('style' not in word) and (';:' != word):
                                    if ('rounded height' not in word) :
                                        new.append(word.replace('<br/>','').replace('\x92',"'").replace('00r','00 r').replace('00b','00 b').replace('\x80',' euro').replace('OBBLIGATORIOINGRESSO', 'OBBLIGATORIO INGRESSO').replace('LIBERA','LIBERA '))
                            writer['has_description'] = ' '.join(new).replace('ee', 'e e').replace('euro',' euro')
                            new = writer['has_description'].lower().split()
                            if ('entrata gratuita' in writer['has_description']) or ('ingresso libero' in writer['has_description']) or ('ingresso gratuito' in writer['has_description']) \
                                or ('entrata libera' in writer['has_description']) or ('gratis' in writer['has_description']) or ('ingresso gratuito' in writer['has_description'] or ('partecipazione' in writer['has_description'])) :
                                for i in range(len(new)) :
                                    if ('liber' in new[i] or 'gratuit' in new[i] ) :
                                        if ('ingress' in new[i-1] or 'entrat' in new[i-1] or 'access' in new[i-1] or 'workshop' in new[i-1].lower() or ('partecipazion') in new[i-1].lower()) :
                                            writer['has_cost']['has_freeEntrance'] = True
                                    if ('informazioni' in new[i].lower()) :
                                        if ('maggiori' in new[i-1] or 'per' in new[i-1]) :
                                            if (writer['has_cost']['has_price'] == '') :
                                                writer['has_cost']['has_price'] = parsed['links'][-1]
                                
                                # DISCOUNTS
                            if ('gravidanza' not in new) : #Filtriamo per evento
                                   
                                idx = None
                                save = None
                                if ('anni' in new):
                                    idx = new.index('anni') 
                                    if (new[idx-1]).isnumeric() : 
                                        for i in range(len(new)) : 
                                            if ('gratis' in new[i]) or ('gratuit' in new[i]) :
                                            
                                                save = i 
                                        if (save != None) and (idx != None) : 
                                                if (save > idx) :
                                                    writer['has_cost']['has_extraBenefits'] = ' '.join(new[idx-1:save+1])
                                                else :
                                                    writer['has_cost']['has_extraBenefits'] = ' '.join(new[save-1:idx+1])
                                ## TICKET PRICE
                                for i in range(len(new)) :
                                    if ('euro'in new[i]) :
                                        if (writer['has_cost']['has_price'] == '') or ('https' in writer['has_cost']['has_price']) : 
                                           
                                            if (new[i-1][-1].isnumeric()) :
                                                writer['has_cost']['has_price'] = new[i-1]
                                               
                                            else :
                                                writer['has_cost']['has_price'] = new[i+1][:2]
                                    if ('scont' in new[i].lower()) :
                                        
                                        select = new[i-2:i+3]
                                        writer['has_specialAnnouncements'] += ' ' + ' '.join(select)
                                writer['has_description'] = writer['has_description'].replace(writer['has_specialAnnouncements'],'')
                                writer['has_hashtag'] = parsed['links'][:-1]
                              
                                
                                
                                #FIX START AND END
                                if ('to' in writer['has_start']) :
                                    spl = writer['has_start'].split('to')
                                    end = spl[-1].split()
                                    if (end[0] == end[1]) :
                                        write = end[1:]
                                    else :
                                        write = end
                                    writer['has_end'] = ' '.join(write) 
                                    date = '/'.join(writer['has_start'].split()[:3])
                                    writer['has_start'] = date +' '+ ' '.join(writer['has_start'].split()[3:]).replace('</h2>','')
                                    writer['has_end'] = date +' '+writer['has_end'].replace('</h2>','')
                                    writer['has_start'] = ''.join(writer['has_start'].split('to')[0])
                                   
                                #VIRTUAL LOCATION -NO VIRTUAL EL
                                #MODE
                                writer['has_mode'] = 'offline'
                                desc = writer['has_description'].split()
                                # CHECK RECURRENCY 
                                if ('edizione' in writer['has_title']) : 
                                    writer['has_recurrency'] = True
                                    writer['has_schedule'] = 'yearly'
                                    
                                    for i in range(len(desc)) :
                                        if ('edizione' == desc[i].lower()) :
                                            if (desc[i-1][0].isnumeric()) or ('V' in desc[i-1] or ('I' in desc[i-1])) : 
                                                writer['has_edition'] = desc[i-1]
                                    
                                if ('Mondo Donna' in writer['has_description'] and writer['has_edition'] == 0) :
                                    writer['has_superEvent'] = 'Mondo Donna Fiera'



                                # FIX DATE AND HAS ENDED
                                
                                date = writer['has_start'].split()
                                if (not '/' in date[0]) :
                                    date = '/'.join(date[:3])
                                    writer['has_start'] = date + writer['has_start'][9:]
                                    if (date not in writer['has_end']) :
                                        writer['has_end'] = date +' '+writer['has_end'].replace('</h2>','').replace("'",'').replace(',','')
                                writer['has_start'] = writer['has_start'].replace('</h2>','')

                               
                                end = writer['has_end'].split()[0]
                                
                                end = datetime.strptime(end, "%d/%m/%Y").strftime("%Y-%m-%d")
                                
                                if (self.has_terminated(end)) :
                                    writer['has_terminated'] = True 
                                if (writer['has_language'] == []) :
                                    writer['has_language'] = ['it-IT']
                                name = ' '.join(writer['has_title'].split('-')[:-1])
                                if ('stream' in name) :
                                    writer['has_mode'] = 'online'
                                    writer['has_virtualLocation'] = parsed['links'][-1]
                                writer['has_title'] = name
                                writer['has_cost']['has_price'] = writer['has_cost']['has_price'].replace('massimo','')
                                # CLEANSE :
                                writer['has_description'] = writer['has_description'].replace('rounded height="275" <div <small sh_eventpage_desc_top <ins <script> (adsbygoogle = window.adsbygoogle || []).push({}); </script> </div> ','').replace('<div <small sh_eventpage_desc_top <ins <script> (adsbygoogle = window.adsbygoogle || []).push({}); </script> </div>','').replace('\u00e0','à').replace('<article','')
                                
                                if ('https' in writer['has_cost']['has_price']) :
                                    writer['has_cost']['has_onlineBooking'] = True 
                                
                                
                                try :
                                    print('Writing {} to file'.format(writer['has_title']))
                                    self.write_to_json(os.path.join(self.writedir, writer['has_title'].replace(' ','-')), writer)  
                                      
                                except :
                                    self.scarti.append(writer)

                        
    def parse_for_tickets_OPEN(self) : 
        """Parsing open data Events for Trento and Rovereto"""
        key = 'C:\\Users\\Anna Fetz\\Desktop\\Data_Science\\third_semester\\KDI_2021\\PARSING\\OpenData'
        for item in os.listdir(key) : 
           
            if (not item.endswith('json')) and (not item.endswith('pyc')) and (not item.endswith('py')) : 
                d = os.listdir(os.path.join(key,item))
               
                for file in d :
                    writer = self.return_writer()
                    
                    with open(os.path.join(os.path.join(key,item),file), encoding ='utf-8') as f : 
                        try:
                            loaded = json.load(f)
                            parsed = loaded 
                           
                            if ('metadata' in parsed) : #QUESTI SONO I DATI DI TN
                              
                                writer['has_start'] = parsed['data']['ita-IT']['from_time'] 
                                writer['has_end'] = parsed['data']['ita-IT']['to_time']
                                writer['has_description'] = parsed['data']['ita-IT']['text']
                                writer['has_language'] = parsed['data']['ita-IT']['tipo_evento'][0]['languages'] if (len(parsed['data']['ita-IT']['tipo_evento'])>0) else ['it-IT','en-GB']
                                writer['has_title'] = parsed['data']['ita-IT']['titolo']
                                if (parsed['data']['ita-IT']['url'] != None) :
                                    writer['has_link'] = parsed['data']['ita-IT']['url']  
                                else:
                                    if (parsed['data']['ita-IT']['image'] != None) :
                                        writer['has_link'] = parsed['data']['ita-IT']['image']['url']
                                    else :
                                        writer['has_link'] = parsed['data']['ita-IT']['email']
                                if (parsed['data']['ita-IT']['luogo_svolgimento'] != None) :
                                    writer['has_mode'] = 'online' if ('online' in parsed['data']['ita-IT']['luogo_svolgimento'] or 'streaming' in parsed['data']['ita-IT']['luogo_svolgimento']) else 'offline'
                                    writer['has_venue'] = parsed['data']['ita-IT']['luogo_svolgimento'] +', Trento' if ('Trento' not in parsed['data']['ita-IT']['luogo_svolgimento']) else parsed['data']['ita-IT']['luogo_svolgimento']
                                else :
                                  
                                    writer['has_venue'] = parsed['data']['ita-IT']['periodo_svolgimento'] 
                                if (parsed['data']['ita-IT']['costi'] != None) :
                                    if ('gratuit' in parsed['data']['ita-IT']['costi']) :
                                        writer['has_cost']['has_freeEntrance'] = True
                                        if ('covid' in parsed['data']['ita-IT']['costi'].lower()) :
                                            writer['has_specialAnnouncements'] = parsed['data']['ita-IT']['costi']
                                        if ('intero' in parsed['data']['ita-IT']['costi']) and ('ridotto' in  parsed['data']['ita-IT']['costi']) :
                                            intero =  parsed['data']['ita-IT']['costi'].split()[parsed['data']['ita-IT']['costi'].index('intero')+1]
                                            writer['has_cost']['has_price'] = intero
                                            ridotto = parsed['data']['ita-IT']['costi'].split()[parsed['data']['ita-IT']['costi'].index('ridotto'):parsed['data']['ita-IT']['costi'].index('ridotto') +2]
                                            writer['has_cost']['has_extraBenefits'] = ' '.join(ridotto)
                                            if (writer['has_cost']['has_price'] != '') and (writer['has_cost']['has_freeEntrance'] == True) :
                                                writer['has_cost']['has_freeEntrance'] = False
                                if (parsed['data']['ita-IT']['informazioni'] != None) :
                                    strip = parsed['data']['ita-IT']['informazioni'].strip('\t').replace('<ul>','').replace('</ul>','').replace('</a>','').replace('<li>','').replace('<a href=','').replace('</li>','').replace('  ','').lstrip()
                                    writer['has_specialAnnouncements'] = strip
                                if (writer['has_mode'] == 'online') and (writer['has_cost']['has_price'] == '') and (writer['has_cost']['has_freeEntrance'] == False):
                                    writer['has_cost']['has_freeEntrance'] = True
                                if (writer['has_mode'] == 'offline') and (writer['has_venue'] !='') and (writer['has_cost']['has_price'] == '') and (writer['has_cost']['has_freeEntrance'] == False) :
                                    writer['has_cost']['has_freeEntrance'] = True
                                desc = parsed['data']['ita-IT']['text'].lower().split()
                                if (writer['has_cost']['has_price'] == '') and (writer['has_cost']['has_freeEntrance'] == False) :
                                    
                                    if (parsed['data']['ita-IT']['informazioni'] != '') :
                                        flag = False
                                        info = parsed['data']['ita-IT']['informazioni'].split('\t')
                                        clean = []
                                        for i in range(len(info)) :
                                            el = info[i].replace('\n','').replace('<ul>','').replace('<li>','').replace('</li','').replace('</ul>','')
                                            if (el != '') : 
                                                clean.append(el)
                                        for el in clean :
                                            if ('href' in el) and (flag == False) and (not 'gmail' in el):
                                                spl = el.split('=')
                                                writer['has_cost']['has_price']  = spl[-1].replace('"Collegamento a sito esterno" >','').replace('</a>    >','')
                                                flag = True
                                    
                                        
                                flag = False 
                                for i in range(len(desc)) : 
                                    if ('prenotazione' in desc[i]) and ('obbligatoria' in desc[i+1]) :
                                        flag = True
                                        writer['has_specialAnnouncements'] = (desc[i] + desc[i+1])
                                        writer['has_cost']['has_freeEntrance'] = True 
                                
                                    if ('obbligatoria' in desc[i]) and ('prenotazione' in desc[i+1]) :
                                        flag = True
                                        writer['has_specialAnnouncements'] = (desc[i] + desc[i+1])
                                        writer['has_cost']['has_freeEntrance'] = True 
                                
                                    if ('gradita' in desc[i]) and ('prenotazione' in desc[i+1]) :
                                        flag = True
                                        writer['has_specialAnnouncements'] = (desc[i] + desc[i+1])
                                        writer['has_cost']['has_freeEntrance'] = True 
                                
                                    if ('prenotazione' in desc[i]) and ('gradita' in desc[i+1]) :
                                        flag = True
                                        writer['has_specialAnnouncements'] = (desc[i] + desc[i+1])
                                        writer['has_cost']['has_freeEntrance'] = True 
                                
                                    if ('prenotazione' in desc[i]) and (flag == False) :
                                        writer['has_specialAnnouncements'] = ' '.join(desc[i-1:i+2] + desc[i+1])
                                        writer['has_cost']['has_freeEntrance'] = True 
                                
                                writer['has_specialAnnouncements'] = writer['has_specialAnnouncements'].replace('</p>','').replace('<p>','') 
                                writer['has_description'] = writer['has_description'].replace(writer['has_specialAnnouncements'],'')

                                ## CANCELLAZIONI

                                for i in range(len(desc)) : 
                                    if ('annullato' in desc[i]) or ('cancellato' in desc[i]) or ('rinviato' in desc[i]) or ('rimandato' in desc[i]) :
                                        
                                       
                                        el = ' '.join(desc[i-6:]).replace('<div>','').replace('</div>','').replace('<p>','').replace('</p>','')
                                        writer['has_specialAnnouncements'] += ' '+ el 
                                
                                #pprint.pprint(writer)
                                # HAS TERMINATED
                                if (writer['has_end'] == None) :
                                    writer['has_end'] = writer['has_start']
                                
                                el = datetime.fromisoformat(writer['has_end']).strftime("%Y-%m-%d %H:%M:%S")
                               
                                
                                if (self.has_terminated(el)):
                                    writer['has_terminated'] = True 
                                if ('fiera' in writer['has_title']) or ('edizione' in writer['has_title']) : 
                                    writer['has_recurrency'] = True 
                                    writer['has_schedule'] = 'yearly'
                                
                            else :
                               
                                writer['has_description'] = parsed['abstract'].replace('<p>','').replace('</p>','') if ('abstract' in parsed) else parsed['description']
                                
                                if ('is_recurrent' in parsed) or ('repeated' in parsed) : 
                                    writer['has_recurrency'] = parsed['repeated'] if ('repeated' in parsed) else parsed['is_recurrent']
                                
                                writer['has_title'] = parsed['title'] if ('title' in parsed) else parsed['name']
                                ## START AND END
                                if ('duration_days' in parsed):
                                    date = parsed['duration_days'].replace('datetime.date(','').replace(')','').replace(']','').replace('[','')

                                    date = date.replace(' ','').split(',')
                                    start = '/'.join(date[:3])
                                    end = '/'.join(date[3:])
                                    time = parsed['duration_hours'].replace("'",'').replace('(','').replace(')','').split(',')
                                    t = []
                                    for el in time :
                                        val = el.strip()
                                        val = val[:2]
                                        mins = el.strip()[2:]
                                        
                                        if (val != '') :
                                           
                                            if (int(val) > 12) :
                                                num = int(val) - 12
                                               

                                                num = str(num)
                                                t.append(num+mins+':00 pm')
                                            else :
                                                t.append(el + ':00 am')
                                        else :
                                            t.append('')
                                    

                                    try : 
                                        if (time[0] != '') and (time[0] != '2021:') : 
                                            writer['has_start'] = datetime.strptime(start + ' ' + t[0] , "%Y/%m/%d %H:%M:%S %p").strftime("%Y/%m/%d %H:%M:%S  %p")
                                        else :
                                            writer['has_start'] = datetime.strptime(start + ' ' + '12:00:00 am' , "%Y/%m/%d %H:%M:%S  %p").strftime("%Y/%m/%d %H:%M:%S  %p")
                                        if (time[-1] != '') and (time[0] != '2021:') : 
                                            writer['has_end'] = datetime.strptime(end + ' ' + t[-1] , "%Y/%m/%d %H:%M:%S  %p").strftime("%Y/%m/%d %H:%M:%S  %p")
                                        else :
                                            writer['has_end'] = datetime.strptime(end + ' ' + '12:00:00 pm' , "%Y/%m/%d %H:%M:%S  %p").strftime("%Y/%m/%d %H:%M:%S  %p")
                                    except : 
                                        try : 
                                            if (time[0] != '') and (time[0] != '2021:') : 
                                                writer['has_start'] = datetime.strptime(end + ' ' +t[0], "%Y/%m/%d %H:%M:%S  %p").strftime("%Y/%m/%d %H:%M:%S  %p")
                                            else :
                                                writer['has_start'] = datetime.strptime(end + ' ' + '12:00:00 am' , "%Y/%m/%d %H:%M:%S  %p").strftime("%Y/%m/%d %H:%M:%S  %p")
                                            if (time[-1] != '') and (time[0] != '2021:') : 
                                                
                                                writer['has_end'] = datetime.strptime(end + ' ' +t[-1] , "%Y/%m/%d %H:%M:%S  %p").strftime("%Y/%m/%d %H:%M:%S  %p")
                                            else :
                                                writer['has_end'] = datetime.strptime(end + ' ' + '12:00:00 pm' , "%Y/%m/%d %HH:%M:%S  %p").strftime("%Y/%m/%d %H:%M:%S  %p")
                                        except :
                                            if (t[0][0] == 0) :
                                                new = t[0][1:]
                                                if (time[0] != '') and (time[0] != '2021:') : 
                                                    writer['has_start'] = datetime.strptime(new + ' ' +t[0], "%Y/%m/%d %H:%M:%S  %p").strftime("%Y/%m/%d %H:%M:%S  %p")
                                                else :
                                                    writer['has_start'] = datetime.strptime(t[-1] + ' ' + '12:00:00 am' , "%Y/%m/%d %H:%M:%S  %p").strftime("%Y/%m/%d %H:%M:%S  %p")
                                                if (time[-1] != '') and (time[0] != '2021:') : 
                                                    writer['has_end'] = datetime.strptime(end + ' ' +t[-1] , "%Y/%m/%d %H:%M:%S  %p").strftime("%Y/%m/%d %H:%M:%S  %p")
                                                else :
                                                    writer['has_end'] = datetime.strptime(end + ' ' + '12:00:00 pm' , "%Y/%m/%d %HH:%M:%S  %p").strftime("%Y/%m/%d %H:%M:%S  %p")
                                    if (writer['has_end'] != '') : 
                                        end = datetime.strptime(writer['has_end'], "%Y/%m/%d %H:%M:%S  %p").strftime("%Y-%m-%d %H:%M:%S")
                                    
                                        writer['has_terminated'] = True if (self.has_terminated(end)) == True else False
                                    else : 
                                        writer['has_terminated'] = True 
                                    ## LOCATION
                                    
                                    ven = parsed['indirizzo'].replace('dalle','').replace('alle','').replace('[','').replace(']','').replace("'",'').split(',') if 'indirizzo' in parsed else parsed['location'].replace('dalle','').replace('alle','').replace('[','').replace(']','').replace("'",'').split(',')
                                    for i in range(len(ven)) :
                                        el = ven[i].strip().lower()
                                        if  ('zoom' in el) or ('online' in el)  or ('stream' in el) or ('youtube' in el):
                                            writer['has_mode'] = 'online'
                                            if ('https' in el) :
                                                writer['has_virtualLocation'] = el
                                            else :
                                                writer['has_virtualLocation'] = 'Zoom' if ('zoom' in el) else parsed['url']
                                                writer['has_virtualLocation'] = 'Youtube' if ('youtube' in el) else parsed['url']
                                            if ('via' in ' '.join(ven).lower()) :
                                                writer['has_mode'] ='blended'
                                    if (writer['has_mode'] == None) or (writer['has_mode'] =='') :
                                            writer['has_venue'] = ' '.join(ven)
                                            writer['has_mode'] = 'offline'
                                    ## LANGUAGE
                                    writer['has_language'] = detect_langs(writer['has_description'])
                                    writer['has_language'] = str(writer['has_language']).replace('[','').replace(']','').split(',')
                                    writer['has_language'] = [el.split(':')[0] +'-'+ el.split(':')[0].upper() for el in writer['has_language']]

                                    writer['has_link'] = parsed['url'] if ('url' in parsed) else (parsed['has_link'])

                                    if (len(parsed['weekday']) > 0) :
                                        writer['has_schedule'] = 'weekly'
                                    ## TICKET
                                    writer['has_cost']['has_price'] = writer['has_link']

                                    #EDIZIONE/SUPEREVENT
                                    desc = writer['has_description'].lower().split()
                                    edizioni = ['prima','seconda','terza','quarta','quinta','sesta','settima','ottava','nona','decima']
                                    if ('edizione' in desc):
                                        for i in range(len(desc)-1) : 
                                            if ('edizione' in desc[i+1]) :
                                                el = desc[i].replace('<sup>','').replace('</sup>','').replace('^','').replace('&quot;','')
                                                if (el in edizioni) :
                                                    idx = edizioni.index(el)+1
                                                    writer['has_edition'] = str(idx)
                                                else :
                                                    writer['has_edition'] = el
                                    if ('festival' in desc) :
                                        writer['has_festivalStatus'] = True 
                                        writer['has_superEvent'] = 'Osvaldo 2021, Ricordi?' if ('osvaldo' in desc) else ''
                                    



                                
                                
                           
                               
                            
                            try :
                                print('Writing {} to file'.format(writer['has_title']))
                                title = writer['has_title'].replace('.json','').replace(' ','-')
                                self.write_to_json(os.path.join(self.writedir,title), writer)  
                                
                            except :
                                self.scarti.append(writer)

 
                        except: 
                            pass
                        
    def parse_for_tickets_MIXED(self) :
        key =r'C:\Users\Anna Fetz\Desktop\Data_Science\third_semester\KDI_2021\PARSING'

        for element in self.dict[key] :
            writer = self.return_writer()
            if ('json' in element) and ('trento' not in element) and ('rovereto' not in element) and ('jetn' not in element.lower()) :
                
                try :
                    with open(element, encoding = 'utf-8') as f : ## MEETUP ##
                        loads = json.load(f)
                        parsed = loads
                        writer['has_recurrency'] = parsed['date_in_series_pattern']
                        writer['has_description'] = parsed['description']
                        d = writer['has_description'] 
                        for el in d :
                            if ('covid' in el) or ('green' in el) or ('pass' in el) or ('greenpass' in el) or ('assembramento' in el)\
                                or ('capienza' in el) or ('normativa' in el) :
                                idx_ = d.index(el)
                                writer['has_specialAnnouncements'] = d[idx_-3:idx_+2]
                            writer['has_cost']['has_price'] = parsed['fee']['amount']
                            writer['has_venue'] = parsed['venue']['address_1'] + ' '+ parsed['venue']['city'] +' '+str(parsed['venue']['lat']) +' '+str(parsed['venue']['lon'])
                            writer['has_title'] = parsed['name']
                            writer['has_start'] = parsed['local_date'] +' '+parsed['local_time']
                            writer['has_mode'] = 'offline' if parsed['is_online_event'] == False else 'online'
                            


                except:
                    pass
            else :
                to_replace = ['<div>','</div>','<a>','</a>','<strong>','</strong>','<span>','</span>','\n', 
                'class="mm-btn stonda3 mm-btn-nocursor mm-padding-2 mm-letter-spacing btn-buy-no mm-margin-b4" style="background-color:#ffffff; border:1px solid #d2d2d2; padding:1px; min-width: 60px;">',
                'class="clear10" style="width:100%;"><span class="mm-medium mm-weight-700">','class="clear10" style="width:100%;">',
                'class="schedine-titolo mm-padding-8 mm-center mm-white">','<div','<br/>','<div class="clear10" style="width:100%;">','<div class="mm-medium" style="font-weight:400;">','class="mm-medium" style="text-transform: uppercase; font-weight:400;">',
                '<span class="mm-medium mm-weight-700">','<div class="clear10" style="width:100%;"></div></div>','>> style="padding-top:3px; float:left; font-weight:600;">',
                '<span class="link_tipo_menu link-bianco" style="cursor:auto;">',' <i class="material-icons" style="font-size:190%; vertical-align:middle;">',
                '<div style="padding-top:3px; float:left; font-weight:600;">','<div <div',' class="mm-medium" style="font-weight:400;">',
                '<div <span class="mm-medium mm-weight-700">','<br>','</br>','<div class="mm-medium" style="text-transform: uppercase; font-weight:400;">',
                'style="padding-top:3px; float:left; font-weight:600;">','class="schedine-separa">','\n','style="vertical-align:middle;"','class="mm-line-height-130','<a'
                ]
                
                if ('movies' in element.lower()) :
                    writer['has_originalLanguage'] = False
                
                    writer['has_subtitles'] = False
                 
                    with open(element, encoding='utf-8') as f:
                        counter = 0
                        reader = csv.reader(f, delimiter=',')
                        for row in reader:
                           
                            for i in range(len(row)) :
                                tmp = row[i]
                                for replacement in to_replace : 
                                    tmp = tmp.replace(replacement,'')
                                tmp = tmp.replace('class="schedine-titolo">','Titolo:')
                                split = tmp.strip().split()
                                
                                if ('Versione originale con sottotitoli:' in ' '.join(split)) :
                                    
                                    writer['has_originalLanguage'] = True
                                    writer['has_subtitles'] = True 
             
                                for j in range(len(split)) :
                                    if ('Titolo:' in split[j]) :
                                        counter += 1
                                        if (counter == 2) : 
                                            try :
                                                
                                                if ('.json' not in writer['name']) :
                                                    self.write_to_json(os.path.join(self.writedir, writer['name']+'.json'), writer)  
                                                else :  
                                                    self.write_to_json(os.path.join(self.writedir, writer['name']), writer)  
                                            except:
                                                print(writer)
                                            writer = self.return_writer()
                                        title = ''.join(' '.join(split[j+2:]).split('>')[-1])
                                        link = split[j+1].replace('href=','')
                                        writer['has_title'] = title
                                      
                                        writer['has_link'] = link 
                                            
                                        writer['has_cost']['has_onlineBooking'] = True
                                    if ('schedine-lancio' in split[j]) :
                                        k = j
                                            
                                        while (k < len(split)) and ('href=' not in split[k]): 
                                            k += 1 
                                        desc = ' '.join(split[j:k]).replace('schedine-lancio>','')
                                        writer['has_description'] = desc.replace('schedine-lancio">','')
                                        writer['has_genre'] = ''.join(''.join(split[k+2]).split('>')[-1]).strip(',')
                                       
                                    if ('Durata' in split[j]) :
                                        k = j
                                        while (k < len(split)) and ('Minuti' not in split[k]) :
                                            k +=1 
                                        writer['has_durationMin'] = ' '.join(split[j:k+1])

                                    if ('Consigli' in split[j]) :
                                        writer['has_targetAge'] = ' '.join(split[j:]) 
                                    if ('Trento">' in split[j]) : 
                                        writer['has_location'] = ' '.join(split[j+1:]).replace('</i','').replace('\ue409','') 
                                        writer['has_cost']['has_price'] = split[1].replace('href=','')
                                    if (':' in split[j]) and (split[j][:split[j].index(':')].isnumeric()):
                                        writer['has_start'] = split[j]
                                writer['has_mode'] = 'offline'
                if ('jetn' in element.lower()) :
                    with open(element, encoding='utf-8') as f:
                        loaded = json.load(f)

                        n_part = sum([int(object['Quantità']) for object in loaded])
                        lst = []
                        for object in loaded : 
                            writer = self.return_writer()
                            if (object['Tipologia biglietto'] == 'Biglietto gratuito') :
                                writer['has_cost']['has_freeEntrance'] = True 
                                writer['has_cost']['has_price'] = object['Totale pagato']
                            n_part += int(object['Quantità'])
                            writer['has_location'] = object['Nome della sede'] + ' ' + object['N. sede']
                            writer['has_title'] = object['Nome evento']
                            writer['has_cost']['has_onlineBooking'] = True if (object['Metodo di consegna'] == 'Biglietto elettronico') else False
                            writer['has_cost']['has_seller'] = object['Nome organizzatore']
                            writer['has_cost']['has_purchaser'] = 'Participant n. : %s Order n. : %s' %(object['Partecipante n.'], object['Ordine n.'])
                            writer['has_description'] = "L'11 novembre, alle ore 18:30, JETN - Junior Enterprise Trento presenta l'evento 'Quick commerce: le consegne del domani'.Ordinare un prodotto online e riceverlo a casa non in giornata ma in meno di un’ora o, addirittura, in una manciata di minuti. È questo quello che il consumatore di domani, sempre più impaziente nei confronti dell’attesa, si aspetterà quando effettuerà un ordine online.L’emergenza pandemica ha impresso una notevole spinta sul settore del delivery, facendo provare a molti la comodità e semplicità di poter far arrivare la spesa a casa o ordinare uno sfizioso gyros greco che dista 20 minuti a piedi scaricando una semplice app e senza varcare la porta della propria abitazione. Tuttavia, riuscire a garantire simili performance necessita di un’attenta riflessione su come garantire tali standard, dovendo puntare necessariamente ad un business model sostenibile che non rispecchia le attuali caratteristiche dei colossi del delivery. Approfondiremo l'argomento in compagnia di Michele Bassetto, expansion and innovation manager di Getir, azienda turca del delivery che sta ridefinendo gli standard del settore. A moderare l'evento sarà presente il professore Francesco Pilati, docente del Dipartimento di Ingegneria Industriale."
                            writer['has_start'] = "11/11/2021 18:30"
                            writer['has_specialAnnouncements'] = "Per partecipare sarà necessario essere muniti di Green Pass valido."
                            writer['has_cost']['ticket']['has_total'] = n_part
                            writer['has_mode'] = 'offline'
                            writer['has_link'] = 'https://www.eventbrite.it/e/biglietti-quick-commerce-le-consegne-del-domani-201494765267'
                            
                            lst.append(writer)
                writer = lst
                        

                               
            try :
               
                if ('JETN'in element): 
                        name = 'Quick-Commerce-JETN'
                    
                else :
                    name = writer['has_title'].replace('.json','')
                
                self.write_to_json(os.path.join(self.writedir, name), writer)  
                                
            except :
                self.scarti.append(writer)
        
    def write_to_json(self,name,what) : 
        with open(name +'.json', 'w') as f : 
            json.dump(what, f) 

    def has_terminated(self, writerval) :
        date = datetime.isoformat(datetime.now())
        end = datetime.isoformat(datetime.fromisoformat(writerval))
        return date > end 
        

landing = [r'C:\Users\Anna Fetz\Desktop\Data_Science\third_semester\KDI_2021\PARSING\scraped_websites\CRUSH\PARSED_CRUSHSITE',
    r'C:\Users\Anna Fetz\Desktop\Data_Science\third_semester\KDI_2021\PARSING\scraped_websites\ESN\PARSED_ESN',
    r'C:\Users\Anna Fetz\Desktop\Data_Science\third_semester\KDI_2021\PARSING\scraped_websites\STAY\PARSED_STAY',
    r'C:\Users\Anna Fetz\Desktop\Data_Science\third_semester\KDI_2021\PARSING\OpenDATA\PARSED_OPEN',
    r'C:\Users\Anna Fetz\Desktop\Data_Science\third_semester\KDI_2021\PARSING']

class Writer() : 
    def __init__(self, directories) :
        self.directories = directories 

    def consider_files(self) : 
        """Writes all files to the respective directories, DON'T RUN"""

        for i in range(len(self.directories)) :
            event = EventParser(dir, all_categories, {}, self.directories[i] )
            event.fill_events_dict()
            #if (i == 0) : 
            #    event.parse_for_tickets_CRUSHSITE()
            #if (i == 1) :
            #    event.parse_for_tickets_ESN()
            #if (i == 2) : 
            #    event.parse_for_tickets_STAY()
            #if (i == 3) : 
            #    event.parse_for_tickets_OPEN()
            #if (i == 4) : 
            #    event.parse_for_tickets_MIXED()
                                

                           
write = Writer(landing)
write.consider_files()







         


