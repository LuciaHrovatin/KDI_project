
import csv, os 

dir = r"C:\Users\Anna Fetz\Desktop\Data_Science\third_semester\KDI_2021\KDI_project\scraped_websites\CRUSH"
list_dir = os.listdir(dir)
list_dir_paths = [os.path.join(dir, f) for f in list_dir]
"""
i = 0
for file in list_dir_paths :
    if (file.endswith('.csv')) : 
        with open(file, encoding = "ISO-8859-1") as f : 
            d = {}
            reader = csv.reader(f,delimiter=',')
            itemprop = set(['name', 'organizer','startDate', 'endDate','streetAddress'])
            classe = set(["testo-boxgrigio-grassetto"]) #Orario + Schema.org + 
            for row in reader:
                analyse = []
                if (len(row) > 1) :
                    grezzo = ' '.join(row).replace(r'\n','')
                    grezzo = grezzo.split()
                    for el in grezzo :
                        to_remove = set(['<span','<div','</div>','</span>','<br/></span>','<br/>','<p','<p><span','</a></p>','</a>','</p>'])
                        if (el not in to_remove) :
                            analyse.append(el.replace('<','').replace('>','').replace('/span',''))

                if (len(analyse) > 0) :
                    i = 0 
                    save = None
                    while i < len(analyse) :
                        if ('class="colonnas-1-301ds"' in analyse[i]) :
                            save = i 
                            break 
                        i +=1
                    s = ''
                    while ('itemprop' not in analyse[i]) : 
                        save += 1
                        s += analyse[i]
                    d[analyse[i]] = s 
                    print(d[analyse[i]])
                    #if save:
                    #    d['ciao']

                    
    break 
"""