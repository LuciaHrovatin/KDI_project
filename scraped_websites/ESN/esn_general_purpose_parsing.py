import os, csv, json 
import pprint as pp 

dir = r"C:\Users\Anna Fetz\Desktop\Data_Science\third_semester\KDI_2021\KDI_project\scraped_websites\ESN\CSV"
list_dir = os.listdir(dir)
list_dir_paths = [os.path.join(dir, f) for f in list_dir]

new_dir = r"C:\Users\Anna Fetz\Desktop\Data_Science\third_semester\KDI_2021\KDI_project\scraped_websites\ESN\JSON"

dates = ['th','st','rd']
months = {'january': 1,'february' : 2,
            'march': 3,'april': 4,'may': 5,
            'june': 6, 'july': 7, 'august': 8, 
            'september': 9, 'october': 10, 'november': 11, 'december': 12}
mesi = {'gennaio': 1,'febbraio' : 2,
            'marzo': 3,'aprile': 4,'maggio': 5,
            'giugno': 6, 'luglio': 7, 'agosto': 8, 
            'settembre': 9, 'ottobre': 10, 'novembre': 11, 'dicembre': 12}
giorni = ['lunedì', 'martedì', 'mercoledì', 'giovedì', 'venerdì', 'sabato', 'domenica']
dayss = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']




def create_parsed_dictionary_and_write() :

    for i in range(len(list_dir_paths)) :
   

        path = os.path.normpath(list_dir_paths[i])
        name = path.split(os.sep)
        file_name = name[-1]
        
        if (list_dir_paths[i].endswith('.csv')) : 
            with open(list_dir_paths[i], encoding = "ISO-8859-1") as f : 
                d = {}
                d['name'] = file_name[:-4]
                d['duration_days'] = []
                d['duration_hours'] = []
                reader = csv.reader(f,delimiter=',')
                for row in reader:
                    to_replace = set(['<span','<div','</div>','</span>','<br/></span>','br/>','a class="colorbox"',
                                    '<br/>','<p','<p><span','</a></p>','</a>','</p>','/div','/p','br/', '/p','field-label-inline clearfix"',
                                    r'div class="field field-name-body field-type-text-with-summary field-label-hidden"div class="field-items"div class="field-item even"',
                                    '<', '>','/span','data-block=true','/h1',r'\t',r'<div class="group-image">\n</div>', r'\n', 
                                    r'\n</div>',r'div class="field field-name-field-image','field-type-image field-label-hidden"div class="field-items"div class="field-item even"a class="colorbox"', "data-cbox-img-attrs='",'{"title": "", "alt": ""}' ])
                    to_split = ''.join(row).lower()
                    parser = []
                    not_remove = set(['class="group-secondary"','class="group-content"', 'class="date-display-single"',
                    'class="field field-name-field-address','class="country"','date-display-end','date-display-start'])
                
                    for el in to_replace :
                        to_split = to_split.replace(el,'')

                    to_split = to_split.split() 

                    for k in range(len(to_split)) : 
                        if ('date-display' in to_split[k]) :
                            #print(to_split[k+5])
                            parser.append(to_split[k])
                        if ('class=' in to_split[k]) and (to_split[k] in not_remove) :
                            parser.append(to_split[k])
                        if ('country' in to_split[k] or 'italy' in to_split[k].lower()) :
                            parser.append(to_split[k])
                        
                        elif ('class=' not in to_split[k]) :
                            parser.append(to_split[k])
                        
                    
                    for k in range(len(parser)) :

                        if ('class=' in parser[k]) and ('group-content' in parser[k]) : 
                            w = k + 2
                            description = []
                            links = []
                            info = []
                        
                            while  w < len(parser)-1 and ('class="group-secondary"') not in parser[w] : 
                                if ('http' in parser[w]) :
                                    links.append(parser[w])
                                if ('th' in parser[w][-2:]) or ('rd' in parser[w][-2:]) or ('st' in parser[w][-2:]) : 
                                    if (parser[w] != 'with') and (parser[w] != 'just') : 
                                        d['duration_days'].append(parser[w])
                                if ('am' in parser[w]) : 
                                    d['duration_hours'].append(parser[w-1])
                                if ('pm' in parser[w]) :
                                    d['duration_hours'].append(parser[w-1])
                                if ("o'clock" in parser[w]) :
                                    d['duration_hours'].append(parser[w-1])
                                

                                if (parser[w] in mesi) :
                                    d['duration_days'].append(parser[w-1])
                                    d['duration_days'].append(mesi[parser[w]])
                                if (parser[w] in months) :
                                    
                                    d['duration_days'].append(parser[w-1])
                                    d['duration_days'].append(months[parser[w]])

                                if ('dalle' in parser[w]) :
                                    d['duration_hours'].append(parser[w+1])
                                if ('alle' in parser[w]) :
                                    d['duration_hours'].append(parser[w+1])
                                if ('mailto:' in parser[w]) :
                                    info.append(parser[w])
                                if (parser[w] in giorni) :
                                    d['duration_days'].append(parser[w])
                                    d['duration_days'].append(parser[w+1])
                                if (parser[w] in dayss) :
                                    d['duration_days'].append(parser[w])
                                    d['duration_days'].append(parser[w+1])
                                else :
                                    if ('-offset-' not in parser[w]) and ('data-block=' not in parser[w]) and ('title="' not in parser[w]) and ('style=' not in parser[w]) and ('style-' not in parser[w]) and ('font-' not in parser[w]) and ('class=' not in parser[w]) and ('field-' not in parser[w]): 
                                        description.append(parser[w])
                                
                                w +=1 
                        
                            d['duration_hours'] = ''.join(d['duration_hours']).replace('class="group-content"','').split()
                            d['description'] = ' '.join(description).replace(r'\x92',"'").replace('even"p', '')
                            d['links'] = links 
                            d['info'] = ' '.join(info)
                        
                        if ('class=' in parser[k]) and ('group-secondary' in parser[k]) :
                            date = []
                            hours = []
                        
                            for i in range(len(parser[k:])) : 
                                if ('date-display' in parser[k:][i]) :
                                
                                    d['duration_days'].append(parser[k:][i].replace('class="date-display-single"',''))
                                    d['duration_hours'].append(parser[k:][i+2].replace('div','').replace('field-group-div"',''))
                                if (len(d['duration_days']) == 0): 
                                    if (parser[k:][i] in months) :
                                        d['duration_days'].append(months[parser[k:][i].lower()])
                                    elif (parser[k:][i] in mesi) : 
                                        d['duration_days'].append(mesi[parser[k:][i].lower()])
                                    if (parser[k:][i] in dates) :
                                        d['duration_days'].append(parser[k:][i-1])
                    
                        
                    

                    

                        if ('class=' in parser[k]) and ('country' in parser[k]) : 
                            location = parser[k]

                            d['location'] = location.replace('class="country"','').rstrip('div')
                    new = []
                    new_2 = []
                    for v,l in zip(d['duration_days'], d['duration_hours']) :
                        if ('class=' not in str(v),str(l)) : 
                            if (str(v)[0].isdigit()) :
                                new.append(str(v).replace('div','').replace('most',''))
                            if (str(l)[0].isdigit()) :
                                new_2.append(str(l).replace('div',''))
                            if (str(l)  in months) :
                                new_2.append(str(l).replace('div',''))
                            if (str(l) in mesi) : 
                                new_2.append(str(l).replace('div',''))
                            if (str(l)  in dayss) :
                                new_2.append(str(l).replace('div',''))
                            if (str(l) in giorni) : 
                                new_2.append(str(l).replace('div',''))

                    d['duration_days'] =  new
                    d['duration_hours'] = new_2


                            



                with open('{}\{}.json'.format(new_dir,d['name']), 'w', encoding='utf-8') as f:
                    json.dump(d, f, ensure_ascii=False, indent=4, default=str)
   

create_parsed_dictionary_and_write()