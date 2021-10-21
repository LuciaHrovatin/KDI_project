import os, csv 

dir = r"C:\Users\Anna Fetz\Desktop\Data_Science\third_semester\KDI_2021\KDI_project\scraped_websites\ESN"
list_dir = os.listdir(dir)
list_dir_paths = [os.path.join(dir, f) for f in list_dir]


def create_parsed_dictionary_and_write() : 
    """PARSES THE HTML FILE INTO A DICTIONARY"""
    for i in range(len(list_dir_paths)) :
            name = list_dir_paths[i].split(r"CRUSH\\")
            file_name = name[-1]
            
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
                                '<br/>','<p','<p><span','</a></p>','</a>','</p>','/div'])
                                if (el not in to_remove) :
                                    analyse.append(''.join(el.replace('<','').replace('>','').replace('/span','').replace('"','')))
                            print(analyse)
            if (i == 18) :
                break
create_parsed_dictionary_and_write()