import json, os
import pprint as pp 
dir = r"C:\Users\Anna Fetz\Desktop\Data_Science\third_semester\KDI_2021\KDI_project\scraped_websites\ESN\JSON"
list_dir = os.listdir(dir)
list_dir_paths = [os.path.join(dir, f) for f in list_dir]

class json_parser(): 

    def __init__(self, files) : 
        self.files = files

    def return_days_and_months(self) :
        days = ["luned","marted","mercoled","gioved","venerd","sabato","domenica"]
        days_eng = ["monday","tuesday","wednesday","thursday","friday", "saturday","sunday"]
        months = ["gennaio","febbraio","marzo","aprile","maggio","giugno","luglio","agosto","settembre","ottobre","novembre","dicembre"]
        months_eng = ["january","february","march","april","may","june","july","august","september","october","november","december"]

        return days, days_eng, months, months_eng
    
    
    def parse_file(self) :
        j = 17
        for file in self.files :  
            with open(file) as json_file:
                data = json.load(json_file)
                indexes = []
                to_pop = set(["colorbox data-cbox-img-attrs","", "'{title:","'alt:'","}","data-colorbox-gallery","gallery-node-30903-PUTIkrhRsVU","href, 'X8jYzjkN','title', 'img alt",  
                "src", "dblnMbuw&amp;c 92d4a68efec566a4d792774e86f94cb7", "title countr",'data-cbox-img-attrs','colorbox',
                "gallery-node-",'font-family', 'font-size','style','background-color','text-align','strong'])
                data['name'] = ''.join(data['name']).replace('-',' ')
                split = data['description'].split() 
                
                for i  in range(len(split)) :
                    if (split[i] in to_pop) : 
                        indexes.append(i)
                j = 0
                for ind in indexes :
                    split.pop(ind-j)
                    j +=1
                if ('field-item' in split):
                    ind = split.index('field-item')
                    data['description'] = ' '.join(split[ind+1:]).replace(", alt: }'",'').replace('/br','').replace('/li','').replace('/ul','').replace('br/','').replace('/p','')
                    data['description'] = data['description'].replace('background-color:transparent;','').replace('font-family:calibri;','').replace('text-align:justifyspan','').replace('font-size:16pxextra','').replace('data-editor','')
                

                else :
                    data['description'] = ' '.join(split).replace('/br','').replace('/li','').replace('/ul','').replace('br/','').replace('/p','').replace(", alt: }'",'')
                    data['description'] = data['description'].replace('background-color:transparent;','').replace('font-family:calibri;','').replace('text-align:justifyspan','').replace('font-size:16pxextra','').replace('data-editor','')
                split = data['description'].replace(',','').replace('countryItaly','').split()
               
                duration_days = []
                duration_hours = []
                
                days_ita, days_eng, months_ita, months_eng = self.return_days_and_months()
                for i in range(len(split)) :
                    if ('program' in split[i].lower()) :
                        data['info'] = ' '.join(split[i:])
                        data['description'] = ' '.join(split[:i])
                    if ('meeting' in split[i].lower()) or ('meet' in split[i].lower()) :
                        
                        data['info'] = ''.join(split[:i])
                        data['description'] = ' '.join(split[:i])
                     
                   

                    if ('date-display-end' in split[i]) :
                        duration_days.append(split[i].replace('date-display-end', ''))
                    if ('date-display-single' in split[i]) :
                        duration_days.append(split[i].replace('date-display-single', ''))
                    
                    if (split[i][-2:] == 'th') or (split[i][-2:] =='st') or (split[i][-2:]=='rd') :
                        if (split[i][:-2].isnumeric()) :
                            duration_days.append(split[i][:-2])
                        
                    if (split[i].lower() in months_eng) :
                        duration_days.append(split[i])
                    if (split[i].lower() in days_eng) :
                        duration_days.append(split[i])
                    if (':00' in split[i]) or ('.00' in split[i]) or ('.OO' in split[i]):
                        if ('da' in split[i-1]) or ('a' in split[i-1]) :

                            duration_hours.append(split[i-1].replace('li',''))
                            duration_hours.append(split[i].replace('li',''))
                        
                        if (i+1 < len(split)) :
                            if ('am' in split[i+1]) or ('pm' in split[i+1]) :

                                duration_hours.append(split[i+1].replace('li',''))
                    if (':' in split[i]) :
                        ind = split[i].index(':') 
                        if (split[i:ind].isnumeric()) and (split[ind+1:].isnumeric()) : 
                            duration_hours.append(split[i])
                    if ('.' in split[i]) :
                        ind = split[i].index('.')
                        if (split[i][:ind].isnumeric()) and ind+1 < len(split[i]) and (split[i][ind+1:].isnumeric()) : 
                            duration_hours.append(split[i])

                    data['duration_days'] = ' '.join(duration_days)
                    data['duration_hours'] = ' '.join(duration_hours)
                    data['description'] = data['description'].replace('date-display-single','').replace('date-display-end','')
                #with open(file, 'w') as f:
                #    json.dump(data, f)
                
                pp.pprint(data)
            if j == 27 :
                break
            j += 1
            


jss = json_parser(list_dir_paths)
jss.parse_file()