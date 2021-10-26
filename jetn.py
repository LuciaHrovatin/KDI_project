import os, csv, json 

path = os.getcwd()
jd = {}
with open(os.path.join(path,'JETN_report_climbing_gap.csv'), encoding ="utf-8") as f :
    dic = csv.DictReader(f, delimiter=';')
   
    for d in dic :
        for k in d :
            jd[k.replace('\ufeff','')] = d[k]  
         
            
        with open('{}\{}.json'.format(path,'JETN_climbing_gap'), 'a', encoding='utf-8') as f:
            json.dump(jd, f, ensure_ascii=False, indent=4, default=str)

