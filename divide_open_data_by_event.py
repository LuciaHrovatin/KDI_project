import os
import json
data = r"C:\Users\Anna Fetz\Desktop\Data_Science\third_semester\KDI_2021\KDI_project\OpenData"
dir = os.listdir(data) 
save_dir = r"C:\Users\Anna Fetz\Desktop\Data_Science\third_semester\KDI_2021\KDI_project\OpenData\by_event"
rovereto = os.path.join(data,dir[2])
trento = os.path.join(data, dir[4])


     
def entpack_city(file) : 
    
    with open(file, encoding ='utf-8') as f: 
        events = json.load(f)
       
        for e in events:
            if ('nome' in e) : 
                name = e['nome']
            else :
                
               
                name = e['data']['ita-IT']['titolo']
       
            name = name.replace('!','').replace('?','').replace('"', '').replace('|','-').replace('/','-').replace(':','-')
            with open(os.path.join(save_dir,name)+'.json', 'w', encoding = 'utf-8') as el :
                json.dump(e, el, ensure_ascii=False, indent=4, default=str) 

#entpack_city(rovereto)
entpack_city(trento)