import pandas as pd 
import random
import json, csv, pprint, os

## -----ELEMENTS IN THE ER -----
# organizes: Event - lo metto in organizes
# participatesin: Event  - tog
# medicalCondition: string
# posts: Review or Creativework
# tag: Person or Event or Organization 
# firsthame.string
# surname 
# middlename 
# nickname. string
# preferredName: string
# contact: ContactPoint
# motherTongue: string
# language: stringl
# birthdate
# nationality 
# has_role 
dir = r'C:\Users\Anna Fetz\Desktop\Data_Science\third_semester\KDI_2021\categories'
def check_id(val) :
    """CHECKS WHETHER THE ID IS ALREADY PRESENT"""
    with open(os.path.join(dir, 'person.csv'), encoding = 'utf-8') as f : 
        read = pd.read_csv(f)
        ids = set(read['has_identifier'].to_list()) 
        if (val in ids) :
            v = str(random.randint(1000,100000)) 
        else :
            v = str(val) 
        return v

def generate_person(val): 
    person = {
            'has_id': 'pr_'+check_id(val),
            'has_eventOrg': [],
            'has_firstName':'',
            'has_middleName':'',
            'has_surname':'',
            'has_preferredName':'',
            'has_nickname':'',
            'has_artistStatus':False
            }
    return person 





def divide_create(name) :
    strumenti = ['violoncello','flauto','pianoforte','piano']
    persons = []
    name = name.replace(' a ',' ').replace('<strong>','')
    for el in strumenti :
        name = name.replace(el,'')
    name.strip('"').replace('2021','').replace('-',' ').strip('-,').replace('  ',' ').strip().split()
    val = str(random.randint(1000,100000)) 
    if ('e' in name) and (name.index('e') != 0) :
        p1 = generate_person(val)
        val2 = str(random.randint(1000,100000))
        p2 = generate_person(val2)
        idx = name.index('e')
        person1 = ' '.join(name[:idx]).split()
        person2 = ' '.join(name[idx+1:]).split()    
        if (len(person1) == 1) :
            p1['has_firstName'] = person1[0]
            p1['has_preferredName'] = person1[0]
        if (len(person1) == 2) :
            p1['has_firstName'] = person1[0]
            p1['has_preferredName'] = person1[0]
            p1['has_surname'] = person1[1]
        if (len(person1) == 3) :
            p1['has_firstName'] = person1[0]
            p1['has_preferredName'] = person1[0]
            p1['has_surname'] = ' '.join(person1[1:])
        if (len(person2) == 1) :
            p2['has_firstName'] = person2[0]
            p2['has_preferredName'] = person2[0]
        if (len(person2) == 2) :
            p2['has_firstName'] = person2[0]
            p2['has_preferredName'] = person2[0]
            p2['has_surname'] = person2[1]
        if (len(person2) == 3) :
            p2['has_firstName'] = person2[0]
            p2['has_preferredName'] = person2[0]
            p2['has_surname'] = ''.join(person1[1:])
            persons.append(p1)
            persons.append(p2)
            
    else :
        p = generate_person(val)
        name = name.split() 
        if (len(name) == 1) :
            p['has_firstName'] = name[0]
        if (len(name) == 2) :
            if (name[0] !='dj') and (name[0] != "l'") and (name[0]!= 'e') :
                p['has_firstName'] = name[0]
                p['has_surname'] = name[-1]
            if (name[0] == 'dj') :
                p['has_nickname'] = ' '.join(name)
        if (len(name) == 3) :
            if (name[1] == 'de') :
                p['has_firstName'] = name[0] 
                p['has_surname'] = ' '.join(name[1:])
            else :
                if (name[0] == 'dottor') :
                    p['has_preferredName'] = name[0]
                    p['has_firstName'] = name[1]
                    p['has_surname'] = ' '.join(name[2:])
        if  (len(name) > 3) :
            for i in range(len(name)) :
                if (name[i] == 'di') or (name[i] == 'de') and (name[i-1] != 'ordinario'): 
                    name1 = name[:i+2]
                    name2 = name[i+2:]
                    p2 =  generate_person(int(val)+1)
                    p2['has_firstName'] = name2[0]
                    p2['has_surname'] = ' '.join(name2[1:]) 
                    p['has_firstName']  = name1[0] 
                    p['has_surname'] = ' '.join(name1[1:]) 
                    persons.append(p)
                    persons.append(p2)
                    
                  
                if ('intervengono' in name[i]) :
                    p['has_role'] = 'Speaker'
                    p['has_firstName'] = ' '.join(name[i+1 : i+3])
                    p['has_surname'] = name[i+3] 
                    
                     
                if ('giapponese' in name[i]) :
                    p['has_role'] = 'Speaker'
                    p['has_firstName'] = name[i-2]
                    p['has_surname'] = name[i-1]
                   
            else :
                if ('e' == name[0] and 'a' == name[-1]) :
                    p['has_firstName'] = name[1] 
                    p['has_surname'] = name[2] 
        if (p not in persons) :
            persons.append(p)
        
   
    return persons

people = pd.DataFrame({"has_firstName": '', 
                        'has_middleName':'',
                        'has_surname':'',
                        "has_role":'',
                        "has_contact":'',
                        'has_identifier':'',
                        'has_artistStatus': '',
                        'has_event':'' }, index = [0])
with open(r'C:\Users\Anna Fetz\Desktop\Data_Science\third_semester\KDI_2021\categories\Person.json') as f :
    load = json.load(f)
    persons = []
    i = 0
    prev = []
    for obj in load:
        
        if (obj['has_firstName'] != '') :
            dicts = divide_create(obj['has_firstName'])
            persons.extend(dicts)

            for person in persons : 
                person['has_eventOrg'] = obj['has_event']
                person['has_event'] = obj['has_event']
                del person['has_eventOrg']
                person['has_artistStatus'] = obj['has_artistStatus'] if ('has_artistStatus' in obj) else False
                person['has_artistStatus'] = obj['has_artistStatus'] if ('has_artistStatus' in obj) else False
                if ('has_artistStatus' in obj) and (obj['has_artistStatus'] == True) :
                    person['has_role'] = 'Performer'
                        
                else :
                    if ('_W_' in obj['has_event']) :
                        person['has_role'] = 'Tutor'
                    if ('_C_' in obj['has_event']) :
                        person['has_role'] = 'Guide / Performer'
                    if ('_P_' in obj['has_event']) : 
                        person['has_role'] = 'Sport Associate'
                    if ('_S_' in obj['has_event']) :
                        person['has_role'] = 'Performer'
                    if ('_E_' in obj['has_event']) :
                        person['has_role'] = 'Speaker'

            
                
                if (person not in prev) : 
                    if (person['has_id'] != '') and (len(person['has_event'])>=1):
                    
                        people = people.append(pd.DataFrame(person), ignore_index = True)
                        prev.append(person)
                
                    
    
#people.to_csv(r"C:\Users\Anna Fetz\Desktop\Data_Science\third_semester\KDI_2021\categories\person_to_merge.csv")
