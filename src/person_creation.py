import pandas as pd 
import random

## -----ELEMENTS IN THE ER -----
# organizes: Event 
# participatesin: Event  
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

student_db = pd.DataFrame()

org = pd.read_csv("organization.csv")

people = pd.DataFrame({"has_name": org["has_administrator"], 
                        "has_role": org["has_administratorRole"],
                        "has_contact": org["has_administratorPhone"]})
people.dropna(subset=["has_name"], inplace=True)
first = []
middle = []
surn = []

for name in people["has_name"]:
    n = name.split()
    if len(n) == 2: 
        first.append(n[0].strip())
        middle.append(" ")
        surn.append(n[1].strip())
    elif len(n) == 3:
        first.append(n[0].strip())
        middle.append(n[1].strip())
        surn.append(n[2].strip())
    else: 
        first.append(n[0].strip())
        middle.append(n[1:-1])
        surn.append(n[-1].strip())
        
people["has_firstName"] = first 
people["has_middleName"] = middle 
people["has_surname"] = surn 
people["has_identifier"] = ["pr_" + str(random.randint(1000, 100000)+i) for i, x in people.iterrows()]
people.drop("has_name", inplace=True, axis = 1)

for ind, role in people.iterrows():
    org.at[ind, 'has_administrator'] = role.has_identifier 

org.drop(["has_administratorRole", "has_administratorPhone", "has_administratorAddress", "Unnamed: 0"], axis = 1, inplace=True)

org.to_csv("organization_final.csv", encoding = "utf-8")
people.to_csv("person.csv")
