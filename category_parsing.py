import json, csv, os, pprint 
import pandas as pd 
import random as rd  # da mille a centomila come integer
class EventType() :
    def __init__(self) :
        self.dir  = os.path.join(os.getcwd(), 'categories') 
        self.categories =  os.listdir(self.dir)

    
    
    def define_paths(self) :

        for t in self.categories : 
            if ('social' ==  t) :
                self.social =  os.listdir(os.path.join(self.dir, 'social'))
            if ('cultural' == t) : 
                self.cultural =  os.listdir(os.path.join(self.dir, 'cultural'))
            if ('education' == t) : 
                self.education =  os.listdir(os.path.join(self.dir, 'education'))
            if ('tour' == t) : 
                self.tour =  os.listdir(os.path.join(self.dir, 'tour'))
            if ('workshop' == t) : 
                self.workshop =  os.listdir(os.path.join(self.dir, 'workshop'))
            if ('sport' == t) :
                self.sport =  os.listdir(os.path.join(self.dir, 'sport'))
        self.social = [os.path.join(os.path.join(self.dir,'social'), file) for file in self.social]
        self.cultural = [os.path.join(os.path.join(self.dir,'cultural'), file) for file in self.cultural]
        self.tour = [os.path.join(os.path.join(self.dir,'tour'), file) for file in self.tour]
        self.workshop = [os.path.join(os.path.join(self.dir,'workshop'), file) for file in self.workshop]
        self.sport = [os.path.join(os.path.join(self.dir,'sport'), file) for file in self.sport]
        self.education = [os.path.join(os.path.join(self.dir,'education'), file) for file in self.education]
    
    def return_dict(self, category):
        if ('social' == category): 
            d = {
                    'has_challenge': False, 
                    'has_happyHour': False,
                    'has_djSet': False,
                    'has_season':'',
                    'has_music':{
                        'has_id': '',
                        'has_producer':'',
                        'has_license':'',
                        'has_copyright':'',
                        'has_type':'',
                        'has_artist': {
                            'has_firstName': '',
                            'has_middleName': '',
                            'has_lastName':'',
                            'has_preferredName':'',
                            'has_id' : '',
                            'has_event':[]
                            },
                        'has_durationMin':'',
                        'has_genre':'',
                        'has_description':'',
                        'has_visualReference':'', #VUOTO GRAZIE
                        'has_instrumentalness':'',
                        'has_speechiness':'',
                        'has_hashtag':[],
                        'has_dimensions':''
                        },
                    'has_organizer' : {
                        'has_name':'',
                        'has_id': '',
                        'has_event' : [],
                        'has_venue':''          
                        }    
                }
        if ('cultural' == category) :
            d = {
                'has_originalLanguage': False,
                'has_performer': '',
                'has_type' : '',
                'has_show': {
                        'has_id': '',
                        'has_producer':'',
                        'has_license':'',
                        'has_copyright':'',
                        'has_type':'',
                        'has_artist': {
                            'has_firstName': '',
                            'has_middleName': '',
                            'has_lastName':'',
                            'has_preferredName':'',
                            'has_id' : '',
                            'has_artistStatus' : False,
                            'has_event' : []
                            },
                        'has_durationMin':'',
                        'has_genre':'',
                        'has_description':'',
                        'has_visualReference':'', #VUOTO GRAZIE
                        'has_instrumentalness':'',
                        'has_speechiness':'',
                        'has_hashtag':[],
                        'has_dimensions':''
                        }, #CREATIVE WORK
                'has_music': {
                        'has_id': '',
                        'has_producer':'',
                        'has_license':'',
                        'has_copyright':'',
                        'has_type':'',
                        'has_artist':{
                            'has_firstName': '',
                            'has_middleName': '',
                            'has_lastName':'',
                            'has_preferredName':'',
                            'has_id' : '',
                            'has_artistStatus' : False,
                            'has_event' : []
                            },
                        'has_durationMin':'',
                        'has_genre':'',
                        'has_description':'',
                        'has_visualReference':'', #VUOTO GRAZIE
                        'has_instrumentalness':'',
                        'has_speechiness':'',
                        'has_hashtag':[],
                        'has_dimensions':''
                        }, #CREATIVE WORK
                'has_subtitles':'',
                'has_guidedTour':False,
                'has_organizer': {
                        'has_name':'',
                        'has_id': '',
                        'has_event' : [],
                        'has_venue':'',
                        }
                    }
        if ('education' == category) : 
            d = {
                'has_topic': "", 
                'has_finalCertificate':False,
                'has_speaker':  {
                    'has_artistStatus' : False,
                    'has_event' : [], 
                    'has_firstName': '',
                    'has_id':''
                    },
                'has_seminarStatus': False,
                'has_ECTS':False,
                'has_interaction': False,
                'has_organizer':{
                        'has_name':'',
                        'has_id': '',
                        'has_event' : [],
                        'has_venue':''          
                        }    
                }
        if ('sport' == category) :
            d = {
                'has_professionalLevel': False, 
                'has_paralympicStatus':False,
                'has_sport': "",
                'has_matchStatus': False,
                'has_courseStatus': False,
                'has_team' :{
                    'has_name':'',
                    'has_id': '',
                    'has_event': []
                    },
                'has_needOfMaterials': False,
                'has_organizer':{
                        'has_name':'',
                        'has_id': '',
                        'has_event' : [],
                        'has_venue':''          
                        }
                }
        if ('tour' == category) : 
            d = {
                'has_tourStart': {
                    'has_lat': '',
                    'has_lon':''
                }, 
                'has_tourEnd': {
                    'has_lat': '',
                    'has_lon':''
                },
                'has_tourIntermediateStops': "", # VUOTO GRAZIE 
                'has_skillRequirement':False,
                'has_hikingStatus': False,
                'has_map' : '', #VUOTO,
                'has_organizer': {
                        'has_name':'',
                        'has_id': '',
                        'has_event' : [],
                        'has_venue':''          
                        }     
                }
        if ('workshop' == category) : 
            d = {
                'has_finalProduct':{
                    'has_type':'',
                    'has_description':'',
                    'has_id':''
                    },
                'has_materialRequirement': False,
                'has_tutor' : {
                    'has_firstName':'',
                    'has_id':'',
                    'has_event':[]
                    },
                'has_organizer' : {
                        'has_name':'',
                        'has_id': '',
                        'has_event' : [],
                        'has_venue':''          
                        }    
                }

        return d

    def is_social(self) : 

        
        
        strumenti = ['chitarra', 'sax', 'sassofono', 'basso']
        for file in self.social : 
            
            with open(file, encoding ='utf-8') as f :
                d = self.return_dict('social')
                reader = json.load(f) 
                parse = reader 
                parse = parse | d  #MERGING DICTIONARIES 
                ## ID ##
                parse['has_eventID'] = 'EV_'+parse['has_title']+'_S'
                parse['has_cost']['has_ticketID'] = 'TI_'+parse['has_title']+'_S'
                


                ## RIPOSIZIONO LA CHIAVE ## 
                
                desc = parse['has_description'].lower().split()
                parse['has_freeEntrance'] = parse['has_cost']['has_freeEntrance'] 
                el = parse['has_cost']
                del el['has_freeEntrance']
                ## INIZIO ## 

                ## LOOKING FOR HAPPYHOUR AND DJSET

                for i in range(len(desc)) :
                    if (desc[i] in strumenti) :
                        parse['has_music']['has_type'] = 'live concert'
                        parse['has_music']['has_genre']  = desc[i+1] #TIPO DI STRUMENTO

                if ('festa' in desc) :
                    parse['has_djSet'] = True 
                if ('party' in desc) :
                    parse['has_djSet'] = True 
                    parse['has_music']['has_genre'] = 'electronic'
                if ('dj' in desc) or ('djset' in desc):
                    parse['has_djSet'] = True 
                if ('musica' in desc) and (parse['has_djSet'] == False):
                    parse['has_djSet'] = True
                if ('live' in desc) and (parse['has_djSet'] == False) :
                    idx = desc.index('live') + 1
                    parse['has_djSet'] = True #GUARDANDO ALLA DEFINIZIONE DI DJ SET
                    parse['has_music']['has_type'] = desc[idx] #METTI COME CREATIVE WORK
                if ('suoni' in desc) :
                    idx = desc.index('suoni') + 1
                    parse['has_music']['has_genre'] = desc[idx] #METTI COME CREATIVE WORK  
                if ('genere' in desc) : 
                    idx = desc.index('genere') + 1
                    parse['has_music']['has_genre'] = desc[idx] #METTI COME CREATIVE WORK
                if ('aperitivo' in desc) : 
                    parse['has_happyHour'] = True 
                if ('mangiare' in desc) or ('bere' in desc) or ('buffet' in desc) or ('cena' in desc) or ('pranzo' in desc) :
                    parse['has_happyHour'] = True
                    if ('20altro' in parse['has_specialAnnouncements']) :
                        parse['has_specialAnnouncements'] = parse['has_specialAnnouncements'][parse['has_specialAnnouncements'].index('20altro') :].replace('20','')[:726]
                    else :
                        if ('prenotazione' in parse['has_description']) :
                            for el in desc :
                                if ('prenotazione' in el) :
                                    idx = desc.index(el)
                                    parse['has_specialAnnouncements'] += ' '.join(desc[idx-1:])
                if ('drink' in parse['has_description']) :
                    parse['has_happyHour'] = True

                # CERCO PER CHALLENGE 
                if ('sfida' in parse['has_description']) :
                    for el in desc :
                        if ('sfida' in el) or ('sfide' in el):
                            parse['has_challenge'] = True 
                if ('game' in parse['has_description']) or ('prize' in parse['has_description']): 
                    i = 0 
                    save = None
                    for el in desc :
                        if ('game' == el) :
                                parse['has_challenge'] = True 
                        #if ('prize' in el) : # CERCO PER EXTRABENEFITS
                        #    save = i
                        #i +=1
                    #if (save != None) :
                        #parse['has_extraBenefits'] = ' '.join(desc[save-15:])
                    
                
                # CERCO PER EXTRABENEFITS 
                #if ('comprende' in parse['has_description']) or ('include' in parse['has_description']):
                    
                #    i = 0 
                #    save = None
                #    for el in desc:
                #        if ('comprende' in el) or ('include' in el) :
                #            save = i 
                #            
                #        if (save != None) and ('.' in el) :
                #            end = i 
                #            break
                #        i +=1
                #    if (save != None) :
                #        parse['has_extraBenefits'] = ' '.join(desc[save:end+1]) 
                #if ('omaggio' in desc) or ('omaggio' in parse['has_description']) and not ('omaggio a' in parse['has_description']):
                #    i = 0
                #    save = None
                #    for el in desc:
                #        if ('omaggio' in desc) :
                #            save = i 
                #        if (save != None) :
                #            if ('.' in el) :
                #                end = i 
                #                break 
                #        i += 1
                #    if (save != None) :
                #        parse['has_extraBenefits'] = ' '.join(desc[save-4:end+1]) 
                ## CONTROLLO SE NON MI E' SCAPPATO QUALCHE EVENTO GRATUITO
                for el in desc :
                    if ('gratuit' in el) or ('gratis' in el) or ('free' in el ):
                        parse['has_freeEntrance'] = True 
            
                ## CERCO HASHTAG 
                for el in desc :
                    if ('#' in el) :
                        parse['has_music']['has_hashtag'].append(el)
                        parse['has_tags'] = parse['has_tags'] + [el] if ('has_tags' in parse) else [el]
                
                ## CERCO LE PERSONAS e ORGANIZERS
                name = None
                org = None
                for i in range(len(desc)-1) :
                    if ('prender' not in desc[i-1]) and (desc[i] == 'cura') :
                        name = desc[i+1]
                    if ('dj' in desc[i]) :
                        name = ' '.join(desc[i:i+2])
                    if ('parrocchia' in desc[i]) :
                        org = ' '.join(desc[i:i+4])
                    if ('pro' == desc[i]) and ('loco' == desc[i+1]) :
                        org = ' '.join(desc[i:+4])
                    if ('esn' == desc[i]) :
                        org = 'ESN Trento'
                        parse['has_organizer']['has_venue'] = 'ESN Trento Sede Centrale'
                    if (desc[i] == 'bar') or ('caff' in desc[i]) or ('ristorante' in desc[i]):
                        org = ' '.join(desc[i-1:i+2])
                        parse['has_organizer']['has_venue'] = parse['has_venue'] 
                
                if ('esn' in parse['has_title'.lower()]) :
                    parse['has_organizer']['has_name'] = 'ESN Trento'
                    
                parse['has_organizer']['has_name'] =  org if (org != None) else ''
                if (parse['has_organizer']['has_name'] != '') :
                    #parse['has_organizer']['has_venue'] =  parse['has_venue'] if (org != None) else ''
                    organization['has_id'] = 'org_'+organization['has_venue'] # DA CAMBIARE CON LAT E LON !!! 
                    parse['has_organizer']['has_event'].append(parse['has_eventID'])
                    
                organization = parse['has_organizer'] #RICORDATI DI MATCHARE LAT LON DI ORG -> SALVA LAT LON

                ## SETTO ID PER CREATIVE WORK E PERSONA 
                parse['has_music']['has_id'] = 'CW_'+parse['has_eventID'] if (parse['has_music']['has_genre'] != '') else ''
                parse['has_music']['has_artist']['has_firstName'] = name if (name != None) else ''
                persona = parse['has_music']['has_artist']
                if (parse['has_music']['has_artist']['has_firstName'] != '') :
                    ids = [val.split('_')[1] for val in self.person_ids()]
                    value = rd.randint(1000,100000)
                    idx = self.check_id(value,ids)
                    persona['has_id'] = 'PR_'+str(idx)
                    persona['has_event'].append(parse['has_eventID']) # L'ID DI PERSONA CE L'HA CREATIVE WORK !!
                 #COSA USIAMO PER LE PERSONA ? PR_NUMERO RANDOM

                    
                
                ## DEFINISCO CREATIVE WORK 
                creative_work = parse['has_music']
                parse['has_MusicWork'] = creative_work['has_id'].replace(' ','_').replace('__','_') ##
                creative_work['has_artist'] = idx  #AGGIUNGO ARTIST INDEX -> L'ARTISTA PERO' NON HA UN CREATIVE WORK ! POST?
                ## DEFINISCO TICKET 
                ticket = parse['has_cost']
                ticket['has_eventID'] = parse['has_eventID']
                parse['has_ticket'] = ticket['has_ticketID'] ## TICKET ID 

                ## VIRTUAL LOCATION 
                vl = {'link':'', 'hostingService':'', 'has_id':''} 

                if (parse['has_virtualLocation'] != '') : 
                    if ('https:' in parse['has_virtualLocation'] ) :
                        vl['link'] = parse['has_virtualLocation'] 
                    else :
                        vl['hostingService'] = parse['has_virtualLocation'] 

                    if ('zoom' in virtual['link']) or ('zoom' in virtual['hostingService'].lower()) :
                        vl['link'] = 'https://zoom.us/'
                    if ('youtube' in vl['link']) or ('youtube' in vl['hostingService'].lower()) :
                        vl['link'] = 'https://www.youtube.com/'
                    if ('teams' in vl['link']) or ('teams'in vl['hostingService'].lower()) : 
                        vl['link'] = 'https://www.microsoft.com/en-us/microsoft-teams/group-chat-software'
                    vl['has_id'] = vl['has_ID'] = 'VL_'+vl['link'] if (vl['link'] != '') else 'VL_'+vl['hostingService']

                parse['has_VirtualLocation'] = vl['has_id']
               
                virtual = vl

                del parse['has_cost']
                del parse['has_music']
                ## RICORDATI LATLON  - NON HO SCRITTO NE PERSONA NE ORGANIZATIONS 
                parse['has_Archive'] = ''
                parse['has_organizer'] = organization['has_id']

            parse['has_language'] = self.check_language(parse) 
            parse['has_venue'] = self.create_venue(parse['has_venue'])
            del parse['has_type']
            ## RICORDATI DI SCRIVERE A FILE 
            print('Writing {} to file'.format(parse['has_title'])) 
            self.writer([(ticket, 'ticket'), (parse,'socialEvents'),(virtual,'virtualLocation'),(creative_work,'CreativeWork'), (persona,'Person'),(organization,'Organization')])
  

    def is_cultural(self) :
        i = 0 
        for file in self.cultural : 
            parse = {}
            strumenti = ['orchestra','pianoforte','violino','viola','violoncello', 'piano', 'flauto']
            with open(file, encoding = 'utf-8') as f :
                ## RICORDATI CHE CI SONO I FILM CHE HANNO GIA' LE CHIAVI QUINDI SISTEMALI SUBITO CHE POI TI DIMENTICHI :
                #print(file)
                d = self.return_dict('cultural')
                reader = json.load(f)
                parse = reader
                parse = parse | d
                parse['has_eventID'] = 'EV_C_'+parse['has_title']
                parse['has_cost']['has_ticketID'] = 'TI_C_'+parse['has_title']
            
                desc = parse['has_description'].lower().split()
                title = parse['has_title'].lower().split()

                if ('has_genre' in parse) :
                    parse['has_show']['has_genre'] = parse['has_genre']
                    parse['has_show']['has_durationMin'] = int(parse['has_durationMin'].replace('Durata','').replace('Minuti.','').replace('minuti','').replace('minuti','').replace('Min.','').replace('Min','').replace('durata','').replace('min','').strip())
                    parse['has_show']['has_originalLanguage'] = parse['has_originalLanguage']
                    parse['has_show']['has_subtitles'] = parse["has_subtitles"]
                
                ## GUARDO PER PERFORMER - SHOW E MUSICA CLASSICA 
                person_show = parse['has_show']['has_artist']
                person_music = parse['has_music']['has_artist']
                
                for i in range(len(desc)) : 
                    if (desc[i] in strumenti) : 
                        parse['has_music']['has_type'] = ' '.join(desc[:i+1]) + ' ' + 'live concert'
                        parse['has_music']['has_genre'] = 'classical music' 
                        parse['has_show']['has_type'] = 'concert or orchestra'
                        
                        
                        if ('/' in parse['has_music']['has_type']) :
                            music = parse['has_music']['has_type'].split('/')
                            person_music['has_firstName'] = ''.join(music[0]).replace('\\','').replace('<strong>','')
                            parse['has_music']['has_type'] = parse['has_music']['has_type'].replace(person_music['has_firstName'], '')
                        if ('con' in parse['has_music']['has_type']) :
                            sp = parse['has_music']['has_type'].split()
                            for j in range(len(sp)) :
                                if (sp[j] == 'con') :
                                    person_music['has_firstName'] = ' '.join(sp[j+1:j+3])
                        else :
                            person_music['has_firstName'] += ' '+ ' '.join(desc[i-2:i+2])
                        parse['has_music']['has_artist'] = person_music 
                    

                for i in range(len(title)) : 
                    if (title[i] in strumenti) : 
                        parse['has_music']['has_type'] = ' '.join(title[:i+1]) + ' ' + 'live concert'
                        parse['has_music']['has_genre'] = 'classical music' 
                        parse['has_show']['has_type'] = 'concert or orchestra'
                        
                        if ('/' in parse['has_music']['has_type']) :
                            music = parse['has_music']['has_type'].split('/')
                            person_music['has_firstName'] = ''.join(music[0]).replace('\\','').replace('<strong>','')
                            
                            parse['has_music']['has_type'] = parse['has_music']['has_type'].replace(person_music['has_firstName'], '')
                        if ('con' in parse['has_music']['has_type']) :
                            sp = parse['has_music']['has_type'].split()
                            for j in range(len(sp)) :
                                if (sp[j] == 'con') :
                                    person_music['has_firstName'] = ' '.join(sp[j+1:j+3])
                        if (person_music['has_firstName'] == '') :
                            person_music['has_firstName'] = ' '.join(title[i-3:i])
                        n = ' '.join(title[i-3:i]).replace('con','').strip().replace("certo  l'",'')
                        if (person_music['has_firstName'] != '') and (n not in person_music['has_firstName']):
                            
                            person_music['has_firstName'] += ' ' + ' '.join(title[i-3:i])
                person_music['has_firstName'] = person_music['has_firstName'].replace('con', '').replace('"katharsis 2021 third stream" rounded height="280" 150px;" width="514"','').replace('con virginia benini','').replace('<strong>','').replace('</strong>','')       
                parse['has_music']['has_artist'] = person_music 
                
                
                ## GUARDO PER ATTORI E SPETTACOLI 
                
                if ('teatro' in parse['has_venue'].lower().strip()) or ('filarmonica' in parse['has_venue'].lower().strip()):
                    if ('compagnia teatrale' in parse['has_title'].lower()) or ('compagnia' in parse['has_title'].lower()) or ('compagnia teatrale' in parse['has_description'].lower()) or ('compagnia' in parse['has_description'].lower()):
                        for i in range(len(desc)-1) : 
                            if ('spettacolo' in desc[i]) and ('teatrale' in desc[i+1]) or ('produzione' in desc[i]) and ('teatrale' in desc[i+1]) or ('spettacoli' in desc[i]):
                                parse['has_show']['has_type'] = 'Theater show'
                            if ('dramma' in desc[i]) :
                                parse['has_show']['has_genre'] = 'Drama'
                            if ('commedia' in desc[i]) :
                                parse['has_show']['has_genre'] = 'Comedy'
                            if ('danza' in desc[i]) :
                                parse['has_show']['has_type'] = 'Dance show'
                            if ('tribut' in desc[i]) :
                                parse['has_show']['has_type'] = 'concert'
                            if ('documentar' in desc[i]) or ('docufilm' in desc[i]) :
                                parse['has_show']['has_type'] = 'Socumentary'
                            ## CERCO PER ATTORI e REGIA - ORGANIZERS 
                            if ('attor' in desc[i]) or ('sopran' in desc[i]) : 
                                person_show['has_firstName'] = ' '.join(desc[:i]).replace('circus sono:','') if ('attor' in desc[i]) else ' '.join(desc[i:i+2]).replace('soprano','')
                            if ('cura' in desc[i-1]) and ('di' == desc[i]) :
                                parse['has_organizer']['has_name'] = ' '.join(desc[i+1:i+8]).replace('info','')
                        for i in range(len(title)) :
                            if ('spettacolo' in title[i]) and ('teatrale' in title[i+1]) or ('produzione' in title[i]) and ('teatrale' in title[i+1]):
                                parse['has_show']['has_type'] = 'Theater show'
                            if ('dramma' in title[i]) :
                                parse['has_show']['has_genre'] = 'Drama'
                            if ('commedia' in title[i]) :
                                parse['has_show']['has_genre'] = 'Comedy'
                            if ('danza' in title[i]) :
                                parse['has_show']['has_type'] = 'Dance show'
                            if ('tribut' in title[i]) :
                                parse['has_show']['has_type'] = 'Concert'
                            if ('documentar' in title[i]) or ('docufilm' in title[i]) :
                                parse['has_show']['has_type'] = 'Documentary'

                        if (parse['has_show']['has_type'] == '') :
                            parse['has_show']['has_type'] = 'Theater event'

                if ('multisala' in parse['has_venue'].lower().strip()) or ('cinema' in parse['has_description'].lower()):
                    if ('cinema' in parse['has_title'].lower()) or ('film' in parse['has_title'].lower()) :
                        parse['has_show']['has_type'] = 'Movie'
                else :
                    if (parse['has_show']['has_type'] == '') :
                        for i in range(len(desc)) :
                            if ('mostra' == desc[i]) :
                                parse['has_show']['has_type'] = 'Art show'
                            if (parse['has_show']['has_type'] == 'Art show') : 
                                if ('fotografica' in desc[i]) and (parse['has_show']['has_genre'] == ''):
                                    parse['has_show']['has_genre'] = 'Photography'
                                if ('arte' in desc[i]) and (parse['has_show']['has_genre'] == '') :
                                    parse['has_show']['has_genre'] = 'Art gallery'
                       
                        for i in range(len(title)) :
                            if ('mostra' == title[i]) :
                                parse['has_show']['has_type'] = 'Art show'
                            if (parse['has_show']['has_type'] == 'Art show') : 
                                if ('fotografica' in title[i]) and (parse['has_show']['has_genre'] == ''):
                                    parse['has_show']['has_genre'] = 'Photography'
                                if ('arte' in title[i]) and (parse['has_show']['has_genre'] == '') :
                                    parse['has_show']['has_genre'] = 'Art gallery'

            if (parse['has_show']['has_type'] == '') and (parse['has_music']['has_type'] == '') :
                for i in range(len(desc)-1) :
                    if ('visita' in desc[i] and 'guidata' in desc[i+1]) or ('visite' in desc[i] and 'guidate' in desc[i+1] ) :
                       parse['has_show']['has_type'] = 'Guided tour'
                       parse['has_guidedTour'] = True
                    if ('cinema' == desc[i]) or ('film' == desc[i]):
                        parse['has_show']['has_type'] = 'Movie'
            
            if (parse['has_show']['has_type'] == '') or (parse['has_music']['has_type'] == '')  :
                for i in range(len(desc)-1) : 
                    if ('comedy' in desc[i] and 'up' in desc[i-1]) :
                        parse['has_show']['has_type'] = 'Stand up comedy' 
                    if ('poetry' == desc[i] and 'slam' in desc[i+1]) or ('slam' in desc[i] and 'poetry' in desc[i+1]):
                        parse['has_show']['has_type'] = 'Poetry Slam' 
                    if ('musica' in desc[i]) :
                        parse['has_show']['has_type'] = 'Music Show'
                    if ('danza' in desc[i]) :
                        parse['has_show']['has_type'] = 'Dance Show'   
                    if ('teatr' in desc[i]) or ('spettacol' in desc[i]) or ('performance' in desc[i]):
                        parse['has_show']['has_type'] = 'Theater Show'
                    if ('film' in desc[i]) :
                        parse['has_show']['has_type'] = 'Movie'  
                    if ('concerti' in desc[i]) :
                        parse['has_show']['has_type'] = 'Concert or Orchestra' 
                    if ('poesia' in desc[i]) :
                        parse['has_show']['has_type'] = 'Poetry Event'
                    if ('visit' in desc[i] and 'guidat' in desc[i+1]) :
                        parse['has_show']['has_type'] == 'Guided tour'
                    if (parse['has_show']['has_type'] != '') :
                        break
                if (parse['has_show']['has_type'] == '') : 
                    for i in range(len(title)-1) :
                        if ('comedy' in title[i] and 'up' in title[i-1]) :
                            parse['has_show']['has_type'] = 'Stand up comedy' 
                        if ('poetry' == title[i] and 'slam' in title[i+1]) or ('slam' in title[i] and 'poetry' in title[i+1]):
                            parse['has_show']['has_type'] = 'Poetry Slam' 
                        if ('musica' in title[i]) :
                            parse['has_show']['has_type'] = 'Music Show'
                        if ('danza' in title[i]) :
                            parse['has_show']['has_type'] = 'Dance Show'   
                        if ('teatr' in title[i]) or ('spettacol' in title[i]) or ('performance' in title[i]):
                            parse['has_show']['has_type'] = 'Theater Show'
                        if ('film' in title[i]) :
                            parse['has_show']['has_type'] = 'Movie'  
                        if ('concerti' in title[i]) :
                            parse['has_show']['has_type'] = 'Concert or Orchestra' 
                        if ('poesia' in title[i]) :
                            parse['has_show']['has_type'] = 'Poetry Event'
                        if ('visit' in title[i] and 'guidat' in title[i+1]) :
                            parse['has_show']['has_type'] == 'Guided tour'
                            parse['has_guidedTour'] = True
                        if (parse['has_show']['has_type'] != '') :
                            break
            if (parse['has_show']['has_type'] == '') :
                if ('visita' in parse['has_title'].lower()) :
                    parse['has_show']['has_type'] = 'Guided tour'
                if ('festa patronale' in parse['has_title'].lower()) :
                    parse['has_show']['has_type'] = 'City feast day'
                if ('concerto' in parse['has_title']) :
                    parse['has_show']['has_type'] = 'Concert'
                if ('scoperta'in parse['has_title']) :
                    parse['has_show']['has_type'] = 'Tour'
                if ('memorial' in parse['has_title']) :
                    parse['has_show']['has_type'] = 'Memorial'
                else :
                    parse['has_show']['has_type'] = 'Theater event'

          
            ## LOOK FOR SOME PERSONS TO WRITE AS ORGANIZERS
            for i in range(len(desc)) :
                if ('di' == desc[i] and 'cura' == desc[i-1]) :
                    parse['has_organizer']['has_firstName'] = ' '.join(desc[i+1:i+3])
        

            ## SETTING PERSON IDS SHOW AND MUSIC
            ids = [val.split('_')[1] for val in self.person_ids()]
            value = rd.randint(1000,100000)
            idx = str(self.check_id(value,ids))

            if (person_show['has_firstName'] != '') :
                if (person_show['has_firstName'] != person_music['has_firstName']) : 
                    el = rd.randint(1000,100000)
                    i1 = str(self.check_id(el,ids))
                    person_show['has_id'] = 'PR_'+i1
                else : 
                    person_music['has_id'] = 'PR_'+idx
                    person_show['has_id'] = person_music['has_id']  # LO IDENTIFICO COME LA STESSA PERSONA STESSO ID

            if (person_music['has_firstName'] != '') : 
                if (person_show['has_firstName'] != person_music['has_firstName']) :
                    el = rd.randint(1000,100000)
                    i2 = str(self.check_id(value,ids))
                    person_music['has_id'] = 'PR_'+i2
                else : 
                    person_music['has_id'] = 'PR_'+idx
                    person_show['has_id'] = person_music['has_id']  # LO IDENTIFICO COME LA STESSA PERSONA STESSO ID

            ## ORGANIZATION -IT IS A PERSON OR AN ORG TO US !
            organization = parse['has_organizer'] #RICORDATI DI MATCHARE LAT LON DI ORG -> SALVA LAT LON
            organization['has_event'].append(parse['has_eventID'])
            if (parse['has_organizer']['has_name'] != '') :
                    parse['has_organizer']['has_venue'] =  parse['has_venue'] 
                    organization['has_id'] = 'org_'+organization['has_venue'] # DA CAMBIARE CON LAT E LON !!! 
            parse['has_organizer'] = organization['has_id']
            ## TICKET ENTITY
            ticket = parse['has_cost']
            ticket['has_eventID'] = parse['has_eventID']
            parse['has_ticket'] = ticket['has_ticketID'].replace(' ','_').replace('__','_')


            ## CREATIVE WORK ENTITY
            parse['has_music']['has_id'] = 'CW_'+parse['has_eventID'].replace('__','_') if (parse['has_music']['has_genre'] != '') else ''
            parse['has_show']['has_id'] = 'CW_'+parse['has_eventID'].replace('__','_') if (parse['has_music']['has_genre'] != '') else ''
            creative_music = parse['has_music']
            creative_show = parse['has_show']
            if (parse['has_music']['has_genre'] != '') : 
                parse['has_MusicWork'] = creative_music['has_id'].replace(' ','_').strip()
            if (parse['has_show']['has_genre'] != '') :
                parse['has_ShowWork'] = creative_show['has_id'].replace(' ','_').strip()

            ## PERSONA ENTITY
            if (person_music['has_firstName'] != '') :
                creative_music['has_artist']['has_artistStatus'] = True 
                creative_music['has_artist'] = person_music['has_id']
                person_music['has_event'].append(parse['has_eventID'])
            else :
                creative_music['has_artist'] = ''
            if (person_show['has_firstName'] != '') :
                creative_show['has_artist']['has_artistStatus'] = True 
                creative_show['has_artist'] = person_show['has_id']
                person_show['has_event'].append(parse['has_eventID'])
            else : 
                creative_show['has_artist'] = ''
               

            ## VIRTUAL LOCATION 
            vl = {'link':'', 'hostingService':'', 'has_id':''}
            if (parse['has_virtualLocation'] != '') : 
                if ('https:' in parse['has_virtualLocation'] ) :
                    vl['link'] = parse['has_virtualLocation'] 
                else :
                    vl['hostingService'] = parse['has_virtualLocation'] 
                
                if ('zoom' in vl['link']) or ('zoom' in vl['hostingService'].lower()) :
                   vl['link'] = 'https://zoom.us/'
                if ('youtube' in vl['link']) or ('youtube' in vl['hostingService'].lower()) :
                    vl['link'] = 'https://www.youtube.com/'
                if ('teams' in vl['link']) or ('teams'in vl['hostingService'].lower()) : 
                    vl['link'] = 'https://www.microsoft.com/en-us/microsoft-teams/group-chat-software'
                vl['has_ID'] = 'VL_'+vl['link'] if (vl['link'] != '') else 'VL_'+vl['hostingService']

            parse['has_VirtualLocation'] = vl['has_id']
            virtual = vl

            ## ORIGINAL LANGUAGE CHECK
            parse['has_originalLanguage'] = True if ('it-IT') in parse['has_language'] or ('en-EN' in parse['has_language']) or ('en-GB' in parse['has_language']) else False

            del parse['has_cost']
            del parse['has_music']
            del parse['has_show']
            parse['has_Archive'] = ''
            parse['has_language'] = self.check_language(parse) 
            parse['has_venue'] = self.create_venue(parse['has_venue'])
            print('Writing {} to file'.format(parse['has_title'])) 
            del parse['has_type']
            self.writer([(ticket, 'ticket'), (parse,'culturalEvents'),(virtual,'virtualLocation'),(creative_music,'CreativeWork'),(creative_show,'CreativeWork'),(person_music, 'Person'),(person_show,'Person'),(organization,'Organization')])
           

    def is_education(self) :

        for file in self.education :   
            
            d = self.return_dict('education')
            with open(file, encoding ='utf-8') as f :
                reader = json.load(f)
                parse = reader 
                try :
                    parse = parse | d 
                except : 
                    parse = parse[0] | d

                desc = parse['has_description'].lower().split()
                title = parse['has_title'].lower().split()
                parse['has_cost']['has_ticketID'] = ('TI_E_'+parse['has_title']).replace(' ','_').replace('__','_')
                parse['has_eventID'] = ('EV_E_'+parse['has_title']).replace(' ','_').replace('__','_')
                ## FINAL CERTIFICATE 
                for i in range(len(desc)) : 
                    if ('certificazione' in desc[i]) or ('attestato' in desc):
                        parse['has_finalCertificate'] = True 
                ## TOPIC & SPEAKER
                for i in range(len(desc)) : 
                    if ('presentazione' in desc[i-1]) :
                        parse['has_topic'] = 'Book presentation'
                    if ('di' == desc[i] and parse['has_topic'] != '') or ('con' == desc[i] and parse['has_topic'] != '') : 
                        if ('miti' not in ' '.join(desc[i:]) and 'racconti' not in ' '.join(desc[i:]) and 'iconografia' not in ' '.join(desc[i:])) : 
                            if (parse['has_speaker']['has_firstName'] == '') :
                                parse['has_speaker']['has_firstName'] = ' '.join(desc[i: i+6]).replace('di ','').replace(' e ','').replace('con ','').replace('presidente','').rstrip(',.:').replace('a confronto','').replace(' del,','').replace(' con','').replace('  del','')
                    
                for i in range(len(title)) : 
                    if ('scienz' in title[i]) or ('neuroscienz' in title[i]) or ('astronomi' in title[i]) or ('bologia' in title[i]):
                        parse['has_topic'] += ' & ' +'Science' if ('Science' not in parse['has_topic']) else ''
                    if ('teologia' in title[i]) :
                        parse['has_topic'] += ' & ' +'Teleology' if ('Teleology' not in parse['has_topic']) else ''
                    if ('intelligenza' in title[i-1]) and ('artificiale' in title[i]) :
                        parse['has_topic'] += ' & ' + 'AI' if ('AI' not in parse['has_topic']) else ''
                    if ('psicologia' in title[i]) :
                        parse['has_topic']  += ' & Psychology' if ('Psychology' not in parse['has_topic']) else ''
                    if ('sperimentare' in title [i]) :
                        parse['has_topic'] += '& ' +'Science' if ('Science' not in parse['has_topic']) else ''
                    if ('stori' in title[i]) or ('archeolog' in title[i]) :
                        parse['has_topic'] += ' & ' +'History' if ('History' not in parse['has_topic']) else ''
                    if ('informatic' in title[i]) or ('digital' in title[i]) or ('tecnolog'):
                        parse['has_topic'] += ' & ' + 'Informatics & Technology' if ('Informatics & Technology' not in parse['has_topic']) else ''
                    if ('etica' in title[i]) or ('privacy' in title[i]):
                        parse['has_topic'] += ' & ' + 'Ethics' if ('Ethics' not in parse['has_topic']) else ''
                    if ('isf' == title[i]) :
                        parse['has_topic'] += ' & ' + 'Ethics & Informatics' if ('Ethics & Informatics' not in parse['has_topic']) else ''
                    if ('imprenditor' in title[i]) :
                        parse['has_topic'] += ' & ' + 'Business' if ('Business' not in parse['has_topic']) else ''
                    if ('yoga' in title[i]) or ('flessibili' in title[i]) or ('cibo' in title[i]):
                        parse['has_topic'] += ' & '+'Wellness & Sport' if ('Wellness & Sport' not in parse['has_topic']) else ''
                    if ('govern' in title[i]) :
                        parse['has_topic'] += ' & '+'Politics' if ('Politics' not in parse['has_topic']) else ''
                    if ('art' in title[i]) or ('pittur' in title[i]) or ('spettacol' in title[i]) or ('teatr' in title[i]):
                        parse['has_topic'] += ' & '+'Arts' if ('Arts' not in parse['has_topic']) else ''
                if (parse['has_topic'] == '') :
                    parse['has_topic'] = ' Open Debate' 
                parse['has_topic'] = parse['has_topic'].lstrip('&')

                ## CERCA LO SPEAKER 
                for i in range(len(desc)) :
                    if ('cura' == desc[i] and 'di' == desc[i+1]) :
                        parse['has_speaker']['has_firstName'] +=' '+ ' '.join(desc[3:])
                    if ('dottor' in desc[i]) :
                        parse['has_speaker']['has_firstName'] += ' '+' '.join(desc[i:i+3])
                    if ('coordinat' in desc[i]) and ('da' in desc[i+1]) :
                        parse['has_speaker']['has_firstName'] += ' '+' '.join(desc[i+2:i+4])
                    if ('nippolog' in desc[i]) :
                        parse['has_speaker']['has_firstName'] += ' '+ ' '.join(desc[i+1:i+3])
                    if ('antropolog' in desc[i]) :
                        parse['has_speaker']['has_firstName'] += ' '+ ' '.join(desc[i+1:i+3])
                    if ('compagnia' in desc[i] and 'di' == desc[i+1]) :
                        parse['has_speaker']['has_firstName'] += ' '+ ' '.join(desc[i+2:i+4])
                    if ('professor' in desc[i]) or ('prof.' in desc[i]):
                        parse['has_speaker']['has_firstName'] += ' '+ ' '.join(desc[i+1:i+3])
                    if ('scienziat' in desc[i]) :
                        parse['has_speaker']['has_firstName'] += ' '+ ' '.join(desc[i+1:i+3])
                ## SEMINAR STATUS 
                if ('webinar' in parse['has_title'].lower()) or ('seminar' in parse['has_title'].lower()) : 
                    parse['has_seminarStatus'] = True 
                if ('seminario' in parse['has_description']) :
                    parse['has_seminarStatus'] = True
                
                ##NO CREDITI AGGIUNTIVI

                ## INTERACTION 
                if ('tavola rotonda' in parse['has_description'].lower()) or ('dibattito' in parse['has_description'].lower()) :
                    parse['has_interaction'] = True
                if ('incontro' in parse['has_title']) or ('dibattito' in parse['has_title']) :
                    parse['has_interaction'] = True 
                if ('dialog' in parse['has_description'].lower()) or ('dialog' in parse['has_title'].lower()) :
                    parse['has_interaction'] = True
                
               
                ## PERSONA ENTITY
                person = parse['has_speaker']
                ## SETTING PERSON IDS SHOW AND MUSIC
                ids = [val.split('_')[1] for val in self.person_ids()]
                value = rd.randint(1000,100000)
                idx = str(self.check_id(value,ids))

                if (person['has_firstName'] != '') :
                        person['has_id'] = 'PR_'+idx
                        person['has_event'].append(parse['has_eventID'])
                parse['has_speaker'] = person['has_id']
                ## ORGANIZATION
                if ('jetn' in parse['has_title'].lower()) : 
                    parse['has_organizer']['has_name'] = 'JETN Trento'
                    parse['has_organizer']['has_id'] = 'org_'+parse['has_venue']
                    parse['has_organizer']['has_venue'] = 'JETN Trento Sede Centrale'
                    parse['has_organizer']['has_event'].append(parse['has_eventID'])
                    parse['has_organizer'] = parse['has_organizer']['has_id']
                organizer = parse['has_organizer']
                parse['has_organizer'] = organizer['has_id']
                    
                
                ## TICKET
                ticket = parse['has_cost']
                ticket['has_eventID'] = parse['has_eventID']
                parse['has_ticket'] = ticket['has_ticketID'].replace(' ','_').strip()

                vl = {'link':'', 'hostingService':'', 'has_id':''}
                if (parse['has_virtualLocation'] != '') : 
                    
                    if ('https:' in parse['has_virtualLocation'] ) :
                        vl['link'] = parse['has_virtualLocation'] 
                    else :
                        vl['hostingService'] = parse['has_virtualLocation'] 
                        vl['has_id'] =  'VL_'+parse['has_virtualLocation'].replace(' ','_') 
                
                  

                    if ('zoom' in vl['link']) or ('zoom' in vl['hostingService'].lower()) :
                        vl['link'] = 'https://zoom.us/'
                    if ('youtube' in vl['link']) or ('youtube' in vl['hostingService'].lower()) :
                        vl['link'] = 'https://www.youtube.com/'
                    if ('teams' in vl['link']) or ('teams'in vl['hostingService'].lower()) : 
                        vl['link'] = 'https://www.microsoft.com/en-us/microsoft-teams/group-chat-software'
                    vl['has_ID'] = 'VL_'+vl['link'] if (vl['link'] != '') else 'VL_'+vl['hostingService']
                    
                parse['has_virtualLocation'] = vl['has_id']
                virtual = vl  
                
                del parse['has_cost']
               
                parse['has_Archive'] = ''
            parse['has_language'] = self.check_language(parse) 
            parse['has_venue'] = self.create_venue(parse['has_venue'])
            del parse['has_type']
            print('Writing {} to file'.format(parse['has_title'])) 
            self.writer([(ticket, 'ticket'), (parse,'educationEvents'),(virtual,'virtualLocation'),(person,'Person'),(organizer,'Organization')])
           
    def is_sport(self) :

        for file in self.sport :
            d = self.return_dict('sport')
            with open(file, encoding ='utf-8') as f: 
                reader = json.load(f) 
                parse = reader 
                parse = parse | d 
                parse['has_eventID'] = ('EV_P_'+parse['has_title']).replace(' ','_')
                parse['has_cost']['has_ticketID'] = 'TI_P_'+parse['has_title'].replace(' ','_')
                desc = parse['has_description'].lower().split()
                title = parse['has_title'].lower().split()

                ## PROFESSIONAL LEVEL 
                if ('avanzato' in title) or ('agonis' in title) or ('intermedio' in title) or ('campionato' in title) or ('agonis' in title) :
                    parse['has_professionalLevel'] = True 
                ## PARALYMPIC 
                if ('paralim' in title) or ('paralim' in parse['has_description']) or ('disabilit' in parse['has_description']):
                    parse['has_paralympicStatus'] = True 
                if ('sorde' in title) or ('sorde' in desc) :
                    parse['has_paralympicStatus'] = True

                ## SPORT TYPE 
                for i in range(len(desc)) :
                    if ('appassionat' in desc[i-1]) and ('di' in desc[i]) :
                        parse['has_sport'] = desc[i+1]
                    if ('rafting' in desc[i]) :
                        parse['has_sport'] += ' & Rafting'
                    if ('calcio' in desc[i]) :
                        parse['has_sport'] += ' & Football'
                    if ('pallavolo' in desc[i]) or ('volley' in desc[i]) : 
                        parse['has_sport'] += ' & Volleyball'
                    if ('atletic' in desc[i]) :
                        parse['has_sport'] += ' & Athletics'
                    if ('marzial' in desc[i]) :
                        parse['has_sport'] += ' & Martial Arts'
                    if ('yoga' in desc[i]) or ('pilates' in desc[i]) :
                        parse['has_sport'] += ' & '+ desc[i]
                    if ('arrampica' in desc[i]) :
                        parse['has_sport'] += ' & Outdoor Sports'
                    if ('italia' in desc[i]) and ('giro' in desc[i-1]) or ('podistico' in desc[i]):
                        parse['has_sport'] += ' & Cycling'
                parse['has_sport'] = parse['has_sport'].lstrip('& ')
                ## HAS OPENAIRSTATUS
                #venue = parse['has_venue'].lower()
                #if ('parco' in venue or 'giardin' in venue or 'monte' in venue  or 'val di' in venue) :
                #    parse['has_openAirStatus'] = True 
                ### HAS MATCH
                if ('partita' in title) or ('sfida' in title) or ('match' in title) or ('gara' in title) or ('torneo' in title) or ('vs' in title):
                    parse['has_match'] = True 
                if ('partita' in desc) or ('sfida' in desc) or ('match' in desc) or ('gara' in desc) or ('torneo' in desc) or ('vs' in desc) or ('podistico' in desc):
                    parse['has_match'] = True
                ## COURSE STATUS
                if ('incontri' in desc) or ('corsi' in desc) or ('corso' in desc):
                    parse['has_courseStatus'] = True
                
                ## TEAM
                if ('squadra' in desc) or ('vs' in desc) or ('team' in desc) or ('squadra' in title) or ('vs' in title) or ('team' in title) or ('gruppo' in desc) :
                    if ('vs' in title) :
                        idx = title.index('vs')
                        team1 = title[:idx]
                        team2 = title[idx+1:]
                        parse['has_team']['has_name'] = ' '.join(team1)+ ' '+ ' '.join(team2)
                        parse['has_team']['has_event'].append(parse['has_eventID'])
                    else :
                        for i in range(len(desc)) :
                            if (desc[i] == 'gruppo') :
                                parse['has_team']['has_name'] = ' '.join(desc[i:i+3]).replace('</strong>','')
                                parse['has_team']['has_event'].append(parse['has_eventID'])
                ## SETTO ORGANIZATION
                organization = parse['has_team']
                if (organization['has_name'] != '') : 
                    organization['has_id'] = 'org_'+parse['has_venue']
                    organization['has_venue'] = parse['has_venue']  # DA CANCELLARE SERVE X LAT LON
                   
                ## NEED OF MATERIAL
                for i in range(len(desc)) :
                    if ('consiglia' in desc[i]) and ('si' == desc[i-1]) :
                        parse['has_needOfMaterials'] = True 
                    if ('bring' == desc[i]) :
                        parse['has_needOfMaterials'] = True
                    if ('portare' in desc[i]) :
                        parse['has_needOfMaterials'] = True 


                ## TICKET ENTITY 
                ticket = parse['has_cost']
                ticket['has_eventID'] = parse['has_eventID']
                parse['has_ticket'] = ticket['has_ticketID'].replace(' ','_')
                
                ## VIRTUAL LOCATION 
                vl = {'link':'', 'hostingService':'', 'has_id':''}
                if (parse['has_virtualLocation'] != '') : 
                    
                    if ('https:' in parse['has_virtualLocation'] ) :
                        vl['link'] = parse['has_virtualLocation'] 
                    else :
                        vl['hostingService'] = parse['has_virtualLocation'] 
                    if ('zoom' in vl['link']) or ('zoom' in vl['hostingService'].lower()) :
                        vl['link'] = 'https://zoom.us/'
                    if ('youtube' in vl['link']) or ('youtube' in vl['hostingService'].lower()) :
                        vl['link'] = 'https://www.youtube.com/'
                    if ('teams' in vl['link']) or ('teams'in vl['hostingService'].lower()) : 
                        vl['link'] = 'https://www.microsoft.com/en-us/microsoft-teams/group-chat-software'
                    vl['has_ID'] = 'VL_'+vl['link'] if (vl['link'] != '') else 'VL_'+vl['hostingService']
                
                parse['has_VirtualLocation'] =  vl['has_id'] 
                parse['has_organizer'] = organization['has_id']
                virtual = vl
                
            
            del parse['has_cost']
            del parse['has_type']
            ## MANCA ORGANIZATION !!
            parse['has_Archive'] = ''
            parse['has_language'] = self.check_language(parse)
            parse['has_venue'] = self.create_venue(parse['has_venue'])
            print('Writing {} to file'.format(parse['has_title'])) 
            self.writer([(ticket, 'ticket'), (parse,'sportEvents'),(virtual,'virtualLocation'), (organization, 'Organization')])
                   
    def is_tour(self) :
        for file in self.tour: 
            d = self.return_dict('tour') 
            with open(file, encoding ='utf-8') as f: 
                reader = json.load(f) 
                parse = reader 
                parse = parse | d 
                parse['has_eventID'] = ('EV_T_'+parse['has_title']).replace(' ','_')
                parse['has_cost']['has_ticketID'] = 'TI_T_'+parse['has_title'].replace(' ','_')
                desc = parse['has_description'].lower().split()
                title = parse['has_title'].lower().split()

                ## HAS_TOURSTART & SKILLS 
                for i in range(len(desc)) :
                    if ('ritrovo' in desc[i]) and ('presso' in desc[i:]) :
                        j = i 
                        while (desc[j] != 'presso') :
                            j +=1 
                        parse['has_tourStart']['lat'] = ' '.join(desc[i+1: i+10])  # SOLO MOMENTANEO !!!!
                    
                    if ('monte' in desc[i]) :
                        parse['has_tourEnd']['lat'] = ' '.join(desc[i:i+2]) # SOLO MOMENTANEO !!
                    if ('valle' in desc[i]) or ('val' == desc[i]) :
                        parse['has_tourEnd'] = ' '.join(title[i:i+2]) if (parse['has_tourEnd'] == ' ') else parse['has_tourEnd'] 
                    if ('avanzato' in desc[i]) or ('intermedio' in desc[i]) or ('base' in desc[i]) : 
                        parse['has_skillRequirement'] = desc[i].strip('"')    
                    if ('trekking' in desc[i]) :
                        parse['has_hikingStatus'] = True 
                    if ('hiking' in desc[i]) :
                        parse['has_hikingStatus'] = True      
                                  
                if ('monte' in parse['has_title']) :
                    monte = title.index('monte')
                    parse['has_tourEnd'] = ' '.join(title[monte:monte+2])
                if ('trekking' in parse['has_title']) :
                    parse['has_hikingStatus'] = True 
                
                ## TICKET
                ticket = parse['has_cost']
                ticket['has_eventID'] = parse['has_eventID']
                parse['has_ticket'] = ticket['has_ticketID'].replace(' ','_').replace('__','_')

                ## VIRTUAL LOCATION
                vl = {'link':'', 'hostingService':'', 'has_id':''}
                if (parse['has_virtualLocation'] != '') : 
                    if ('https:' in parse['has_virtualLocation'] ) :
                        vl['link'] = parse['has_virtualLocation'] 
                    else :
                        vl['hostingService'] = parse['has_virtualLocation'] 
                   
              

                    if ('zoom' in vl['link']) or ('zoom' in vl['hostingService'].lower()) :
                        vl['link'] = 'https://zoom.us/'
                    if ('youtube' in vl['link']) or ('youtube' in vl['hostingService'].lower()) :
                        vl['link'] = 'https://www.youtube.com/'
                    if ('teams' in vl['link']) or ('teams'in vl['hostingService'].lower()) : 
                        vl['link'] = 'https://www.microsoft.com/en-us/microsoft-teams/group-chat-software'
                    vl['has_ID'] = 'VL_'+vl['link']

                ## ORGANIZER 
                if ('esn' in parse['has_title'].lower()) or ('esn' in desc) :
                    parse['has_organizer']['has_name'] = 'ESN Trento'
                    parse['has_organizer']['has_venue'] = 'ESN Trento Sede Centrale'
                    parse['has_organizer']['has_id'] = 'org_'+parse['has_venue']
                    parse['has_organizer']['has_event'].append(parse['has_eventID'])

                organizer = parse['has_organizer']
                parse['has_organizer'] = organizer['has_id']
                parse['has_virtualLocation'] = vl['has_id']
                virtual = vl
            
                del parse['has_cost']
                parse['has_Archive'] = ''
                parse['has_language'] = self.check_language(parse) 
                parse['has_venue'] = self.create_venue(parse['has_venue'])
                del parse['has_type']
            print('Writing {} to file'.format(parse['has_title'])) 
            self.writer([(ticket, 'ticket'), (parse,'tourEvents'),(virtual,'virtualLocation'),(organizer,'Organization')])
                
    def is_workshop(self) : 
        for file in self.workshop :
            d = self.return_dict('workshop')
            with open(file, encoding ='utf-8') as f :
                reader = json.load(f) 
                parse = reader 
                parse = parse | d 
                parse['has_eventID'] = 'EV_W_'+parse['has_title'].replace(' ','_').replace('__','_')
                parse['has_cost']['has_ticketID'] = 'TI_W_'+parse['has_title'].replace(' ','_')

                desc = parse['has_description'].lower().split()
                title = parse['has_title'].lower().split()

                ## FINAL PRODUCT
                if ('corso' in title) :
                    idx = title.index('corso') 
                    parse['has_finalProduct']['has_type'] = title[idx:idx+7] if (idx+7 < len(title)) else title[idx:]
                    parse['has_finalProduct']['has_description'] = parse['has_description']
                    parse['has_finalProduct']['has_id'] = 'CW_'+parse['has_title'].replace(' ','_')
                if ('creare' in title) : 
                    idx = title.index('creare') 
                    parse['has_finalProduct']['has_type'] = title[idx:idx+7] if (idx+7 < len(title)) else title[idx:]
                    parse['has_finalProduct']['has_description'] = parse['has_description']
                    parse['has_finalProduct']['has_id'] = 'CW_'+parse['has_title'].replace(' ','_')
                if ('workshop' in title) :
                    idx = title.index('workshop') 
                    parse['has_finalProduct']['has_type'] = title[idx:idx+7] if (idx+7 < len(title)) else title[idx:]
                    parse['has_finalProduct']['has_description'] = parse['has_description']
                    parse['has_finalProduct']['has_id'] = 'CW_'+parse['has_title'].replace(' ','_')
                if (parse['has_finalProduct']['has_type'] == '') :
                    for i in range(len(desc)) :
                        if ('laborator' in desc[i]) :
                            parse['has_finalProduct']['has_type'] = desc[i:i+7]
                            parse['has_finalProduct']['has_description'] = parse['has_description']
                            parse['has_finalProduct']['has_id'] = 'CW_'+parse['has_title'].replace(' ','_')
                        if ('dedicat' in desc[i]) : 
                            parse['has_finalProduct']['has_type'] = desc[i:i+7] 
                            parse['has_finalProduct']['has_description'] = parse['has_description']
                            parse['has_finalProduct']['has_id'] = 'CW_'+parse['has_title'].replace(' ','_')
                        if ('corso' in desc[i]) :
                            parse['has_finalProduct']['has_type'] = desc[i:i+7] 
                            parse['has_finalProduct']['has_description'] = parse['has_description']
                            parse['has_finalProduct']['has_id'] = 'CW_'+parse['has_title'].replace(' ','_')
                        ## NEED OF MATERIAL
                        if ('fotografia' in desc[i]) :
                            parse['has_materialRequirement'] = True 
                        ## TUTOR
                        if ('cura' in desc[i-1] and 'di' == desc[i]) or ('cura' in desc[i-1] and 'del'in desc[i]) :
                            parse['has_tutor']['has_firstName'] = ' '.join(desc[i+1:i+5]).replace('<em>','').replace('</strong>','').replace('<strong>','')
                            parse['has_tutor']['has_eventID'] = parse['has_eventID']
                

                ## ORGANIZATION ENTITY
                organizer = parse['has_organizer']
                parse['has_organizer'] = organizer['has_id']

                ## PERSON
                person = parse['has_tutor']
                if (person['has_firstName'] != '') : 
                    ids = [val.split('_')[1] for val in self.person_ids()]
                    value = rd.randint(1000,100000)
                    idx = str(self.check_id(value,ids))
                    person['has_id'] = 'PR_'+idx
                    person['has_event'].append(parse['has_eventID'])
                parse['has_tutor'] = person['has_id']
                


                # CREATIVEWORK
                creative = parse['has_finalProduct'] 
                if (parse['has_finalProduct']['has_type'] != '') :
                   parse['has_finalProduct'] = 'CW_'+parse['has_eventID'].replace(' ','_').replace('__','_')
                parse['has_finalProduct'] = creative['has_id']
                    
                ## TICKET 
                ticket = parse['has_cost']
                ticket['has_eventID'] = parse['has_eventID']
                parse['has_ticket'] = ticket['has_ticketID'].replace(' ','_')
                
                ## VIRTUAL LOCATION
                vl = {'link':'', 'hostingService':'', 'has_id':''}
                if (parse['has_virtualLocation'] != '') : 
                    
                    if ('https:' in parse['has_virtualLocation'] ) :
                        vl['link'] = parse['has_virtualLocation'] 
                    else :
                        vl['hostingService'] = parse['has_virtualLocation'] 
                    

                    if ('zoom' in vl['link']) or ('zoom' in vl['hostingService'].lower()) :
                        vl['link'] = 'https://zoom.us/'
                    if ('youtube' in vl['link']) or ('youtube' in vl['hostingService'].lower()) :
                        vl['link'] = 'https://www.youtube.com/'
                    if ('teams' in vl['link']) or ('teams'in vl['hostingService'].lower()) : 
                        vl['link'] = 'https://www.microsoft.com/en-us/microsoft-teams/group-chat-software'

                    vl['has_ID'] = 'VL_'+vl['link']
                 
                virtual = vl
                parse['has_virtualLocation'] = vl['has_id']

            
            del parse['has_cost']
            ## MANCA TUTOR DA INSERIRE!!
            parse['has_Archive'] = ''
            parse['has_language'] = self.check_language(parse) 
            parse['has_venue'] = self.create_venue(parse['has_venue'])
            del parse['has_type']
            
            print('Writing {} to file'.format(parse['has_title'])) 
            self.writer([(ticket, 'ticket'), (parse,'workshopEvents'),(virtual,'virtualLocation'), (creative,'CreativeWork'), (person, 'Person'), (organizer,'Organization')])
                             

    def writer(self, values) :
        """WRITES TO THE RESPECTIVE FILES"""
  
        for value,name in values: 
            print('From the file, writing {} to {}'.format(value, name))
            filename = os.path.join(self.dir, name)+'.json'
            with open(filename , 'a+') as f :
               
                json.dump(value, f, indent=4)
    
        print('DONE !')

    def person_ids(self) : 
        with open(os.path.join(self.dir, 'person.csv'), encoding = 'utf-8') as f : 
            read = pd.read_csv(f)
            ids = set(read['has_identifier'].to_list()) 

            return ids 
    def check_id(self, val, lista) :
        if (val in lista) :
            v = str(rd.randint(1000,100000)) 
        else :
            v = val 
        return v
    
    def check_language(self, dic) :
        """CHECKS THAT LANGUAGES ARE WRITTEN IN ISO 639-2 FORMAT"""

        new = []
        lang = dic['has_language'] 
        for l in lang:
            if ('it' in l) :
                new.append('it-IT')
            if ('en' in l) :
                new.append('en-GB')
            if ('de' in l) :
                new.append('de-DE')
            if ('fr' in l) :
                new.append('fr-FR')
        
        return new

    def create_venue(self,address) :
        d = {'lat':'','lon':'','address':address}
        return d 


ev = EventType() 
ev.define_paths()
#ev.is_cultural()
#ev.is_social()
#ev.is_education()
#ev.is_sport()
#ev.is_tour()
#ev.is_workshop()
