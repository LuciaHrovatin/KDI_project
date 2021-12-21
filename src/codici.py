import pandas as pd
import json 

fac = pd.read_csv("facility_final.csv")

fac.drop(["Unnamed: 0.1", "information", "smoking"], axis = 1, inplace=True)
fac.rename(columns={"has_location": "has_osmID"}, inplace=True)

menu = []

for x in fac.menu: # "{'cuisine': None, 'isVegetarian': None, 'isVegan': None, 'isGlutenFree': None}"
    row = x.strip("{").strip("}").split()
    add = ""
    if row[3].strip(",") != "None" or row[5].strip(",") != "None" or row[-1] != "None":
        if row[3].strip(",") != "None":
            add += ", vegetarian"
        if row[5].strip(",") != "None":
            add += ", vegan"
        if row[-1] != "None":
            add += ", gluten free."
    if add != "":
        if row[1].strip(",") == "None":
            m = add.lstrip(",") 
        else:
            m = row[1].strip(",") + add
    elif row[1].strip(",") == "None":
        m = None 
    else: 
        m = row[1].strip(",").strip("\'")
    menu.append(m)

fac["menu"] = menu


loc = pd.read_csv("location_final.csv")
loc.drop(["Unnamed: 0.1", "Unnamed: 0.1.1", "osm_ID"], axis = 1, inplace = True)

loc.to_csv("locations.csv")
fac.to_csv("facilities.csv")