import os, json
from miniparsing import return_list_of_files
dir = r'C:\Users\Anna Fetz\Desktop\Data_Science\third_semester\KDI_2021\KDI_project\OpenData\by_event'
names = os.listdir(dir)

all_files = set([os.path.join(dir,n) for n in names])


dir_events = os.listdir(r'C:\Users\Anna Fetz\Desktop\Data_Science\third_semester\KDI_2021\KDI_PROJECT\EVENTS')
d = {os.path.join(r'C:\Users\Anna Fetz\Desktop\Data_Science\third_semester\KDI_2021\KDI_PROJECT\EVENTS',v): [] for v in dir_events}
d = return_list_of_files(dir_events, d)



crush = set(os.listdir(r'C:\Users\Anna Fetz\Desktop\Data_Science\third_semester\KDI_2021\KDI_PROJECT\scraped_websites\CRUSH\JSON\JSON_PARSED'))
stay = set(os.listdir(r'C:\Users\Anna Fetz\Desktop\Data_Science\third_semester\KDI_2021\KDI_PROJECT\scraped_websites\STAY\JSON'))
esn = set(os.listdir(r'C:\Users\Anna Fetz\Desktop\Data_Science\third_semester\KDI_2021\KDI_PROJECT\scraped_websites\ESN\JSON'))

def swap_files(subfolders, files_to_swap) : 
    """Swaps wrong Trento and Rovereto files"""
    global crush, stay, esn
    ret = []
    for directory in subfolders :
        for file in subfolders[directory] : 
            name = file.split('\\')
            name = name[-1]
            if ('erasmus' not in name) and ('report-QuickCommerce.xlsx.lnk' not in name) and ('JETN_climbing_gap' not in name): 
                if (name not in crush) and (name not in stay) and (name not in esn) : 
                        ret.append(file)
    return ret


to_swap = set(swap_files(d, all_files))


file_names = {file.split('\\')[-1] : file for file in to_swap}
file_original = {file.split('\\')[-1] : file for file in all_files}


def swap_content(original, names) : 
    change = []
    for name in original :
        if name in names :
            change.append((original[name], names[name]))

    for el in change :
        with open(el[1], encoding ='utf-8') as f : 
            replace = json.load(f)
        with open(el[0], encoding = 'utf-8') as f1 :
            move_content = json.load(f1)
        
        new = move_content
        if ('ticket' in replace) and ('is_online' in replace) and ('is_offline' in replace) and ('is_blended' in replace) : 
            new['ticket'] = replace['ticket']
            new['is_online'] = replace['is_online']
            new['is_offline'] = replace['is_offline']
            new['is_blended'] = replace['is_blended']
    
        with open(el[1],'w', encoding = 'utf-8') as f2 : 
            json.dump(new, f2)
  

swap_content(file_original, file_names)
