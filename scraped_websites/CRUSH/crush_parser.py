from pprint import pprint as pp
import csv, os, json  
from datetime import datetime


class CrushParser() :

    def __init__(self) :
        self.dir_csv = r"C:\Users\Anna Fetz\Desktop\Data_Science\third_semester\KDI_2021\KDI_project\scraped_websites\CRUSH\CSV"
        self.new_dir_json = r"C:\Users\Anna Fetz\Desktop\Data_Science\third_semester\KDI_2021\KDI_project\scraped_websites\CRUSH\JSON"
        self.list_dir_paths =  [os.path.join(self.dir_csv, f) for f in  os.listdir(self.dir_csv)]
        self.to_save = r"C:\Users\Anna Fetz\Desktop\Data_Science\third_semester\KDI_2021\KDI_project\scraped_websites\CRUSH\JSON\JSON_PARSED"
        self.json_json =  r"C:\Users\Anna Fetz\Desktop\Data_Science\third_semester\KDI_2021\KDI_project\scraped_websites\CRUSH\JSON\JSON_PARSED"

        self.mesi =  {'gennaio': 1,'febbraio' : 2,
            'marzo': 3,'aprile': 4,'maggio': 5,
            'giugno': 6, 'luglio': 7, 'agosto': 8, 
            'settembre': 9, 'ottobre': 10, 'novembre': 11, 'dicembre': 12}
   
        self.giorni = ['lunedì', 'martedì', 'mercoledì', 'giovedì', 'venerdì', 'sabato', 'domenica']

    @staticmethod
    def create_parsed_dictionary_and_write(self) : 
        """PARSES THE HTML FILE INTO A DICTIONARY"""
            
        for i in range(len(self.list_dir_paths)) :
            name = self.list_dir_paths[i].split(r"CRUSH\\")
            file_name = name[-1]
            new = file_name.split('CSV')
            to_join = new[-1][1:-4]
            if (self.list_dir_paths[i].endswith('.csv')) : 

                with open(self.list_dir_paths[i], encoding = "ISO-8859-1") as f : 
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
                            
                            
                    ret = self.parse_dict(d)
                
                    self.write_dic_to_json(ret, to_join)
                               
              
        
    @staticmethod
    def parse_dict(self, dic):
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
    
    @staticmethod
    def write_dic_to_json(self,dic,title) :
        with open(os.path.join(self.new_dir_json, title)+'.json', 'w', encoding='utf-8') as f:
            json.dump(dic, f, ensure_ascii=False, indent=4, default=str)
    
"""

    def second_parsing(self) : 
        self.dir_json = r"C:\Users\Anna Fetz\Desktop\Data_Science\third_semester\KDI_2021\KDI_project\scraped_websites\CRUSH\JSON"
        self._list_dir = os.listdir(self.dir_json)
        self.list_dir_paths_json = [os.path.join(self.dir_json, f) for f in self._list_dir]


        o = 0

        for file in self.list_dir_paths_json : 
      
        
            with open(file, encoding ="utf-8") as f :
                parsed = {}
                dic = json.load(f)
                name = file.split('\\')
                name = name[-1].split('html')
                name = name[0]
                dic['name'] = '  '.join(name.replace('-',' ').split()) 
                



              
                parsed = {k:[] for k in list(dic.keys())}
                other_loc = ''

                for e in dic :
                        
                    parsed[e] = dic[e]
                    if (e == 'name') :
                        parsed[e] = ' '.join(dic[e].split())
                    if (e == 'location') : 
                        if ('Dove:' in dic[e]) : 
                            i_where = dic[e].index('Dove:') + 2
                            flag_where = True
                        if ('Orario:' in dic[e]) :
                            i_when = dic[e].index('Orario:')
                                
                            if (dic['duration_hours'] == 'Not specified') : 
                                parsed['duration_hours'] = dic[e][i_when:]

                        if (dic['location'] != 'Not specified') and (len(dic['location']) != 0) : 
                            s1 = ' '.join(dic['location'][3:])
                            parsed[e] = dic['location']
                            if flag_where :
                                s2 = ' '.join(dic[e][i_where:])
                                if (s1 != s2) :
                                    other_loc = ' '.join(dic[e][i_where:]) 
                               
                               
                         

                parsed['recurrency'] = []   
                rev = []
              
                for key in parsed : 
                    if (key == 'location') :
                        k = 0
                        if (not type(parsed[key]) == list) :
                            parsed[key] = parsed[key].split()
                        while len(parsed[key]) > 0 : 
                            el = parsed[key].pop()
                            if (el.lower() in self.giorni) : 
                                parsed['recurrency'].append(el)
                            if ('.' in el and el[:el.index('.')].isnumeric() and el[el.index('.')+1:].isnumeric()): 
                                parsed['duration_hours'].append(el)

                            else :
                                rev.append(el)
                            k += 1
                rev = rev[::-1][2:]
                if ('Orario:' in rev) :
                    i = rev.index('Orario:') 
                    if ('Note:' in rev):
                        j = rev.index('Note:')
                        parsed['location'] = ' '.join(rev[:i]).replace('itemprop=streetAddress','')
                        parsed['info'] += ' '+' '.join(rev[j:])
                    else :
                        parsed['location'] = ' '.join(rev[:i]).replace('itemprop=street','')


                
                        
 
 
                parsed['duration_days'] = parsed['recurrency']
                if ('Orario:' in other_loc) : 
                    other_loc = other_loc[:other_loc.index('Orario:')]
                    parsed['location'] += ', ' + ''.join(other_loc)

                if (len(parsed['location']) == 0) :
                    if ('title=' in parsed['description']) : 
                        title = parsed['description'].index('title=')
                        parsed['location'] = parsed['description'][title:].replace('title=','')
                    inf = parsed['info'].split()
                    i = -1
                    for w in inf : 
                        if ('Dove:' in w) :
                            i = inf.index(w) 
                            print(inf[i+1:])
                            break 
                    
                    parsed['location'] += ', ' +' '.join(inf[i:]).replace('Dove: itemprop=streetAddress','')
                
                if (len(parsed['duration_days']) == 0) :
                    l = parsed['description'].split()
                    t = []
                    for i in range(len(l)) :
                            
                        if (l[i].lower() in self.mesi) : 
                            if (l[i-1].isnumeric()) :
                                t.append(l[i-1])
                                t.append((l[i],self.mesi[l[i].lower()]))
                                if (l[i+1].isnumeric()) :
                                    t.append(l[i+1]+ '|')
                        if (l[i].isnumeric() and l[i]not in t) and ('dalle' != l[i-1] and 'alle' != l[i-1]) :
                            t.append(l[i])
                    parsed['duration_days'] = t 
                    if (t == []) :
                        j = -1
                        i = 0

                        l = parsed['info'].split() 
                        for w in l :
                            if ('itemprop=startDate' in w) :
                                i = l.index(w) 
                            if ('itemprop=endDate' in w) : 
                                j = l.index(w)
                        if (i != 0) : 
                            parsed['duration_days'].extend(' '.join(l[i:j]).replace('itemprop=startDate','').replace('itemprop=endDate','').split())
                        
                if (parsed['duration_hours'] == 'Not specified') : """

                

 
                            
                    
                







            if (o > 56 and o < 67) :
                pp(parsed)
            if (o == 67) :
                break
            o += 1
"""    
    def date_time_location_parsing(self) : 
        # FINAL PARSING FOR CRUSH SITE 

        list_json = os.listdir(self.json_json)
        parse_path = [os.path.join(self.json_json, f) for f in list_json]

        i = 0
        
        for source in parse_path : 
    
            with open(source, encoding ="utf-8") as f :
                    
                    
                    

                    pp(parsed)
          
                                    
                                    

            if i == 3 :
                break
            i += 1


        
"""

ck = CrushParser()
ck.second_parsing()


                                


    
