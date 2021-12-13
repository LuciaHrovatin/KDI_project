import pandas as pd 
import random 
from datetime import date



acc = pd.read_csv("accessibility.csv")
pl = pd.read_csv("facility_data.csv")


pdf = pd.merge(acc, pl, how = "inner", on = ["has_latitude", "has_longitude"])

arch_bar = []

id = []
name = []
city = []
pr = []
country = []
web = []
lat = []
lon = []
el = []
facType = []
upDate = []
street = []
house = []
elevator = []
parking = []
guidanceS = []
toilet = []
steps = []
ramp = []
stairSlpe = []
levAccess = []

locats = pd.read_csv("location.csv")
locats["osm_ID"] = [str(round(x)) for x in locats["osm_ID"]]


for ind, case in pl.iterrows():
    if str(round(case.has_location)) in str(round(pdf.has_location)): 
        arch_bar.append(pdf.loc[pdf["has_location"] == case["has_location"]]["has_ID"])
    else:
        index = "ab_" + str(random.randint(1000, 100000))
        id.append(index)
        arch_bar.append(index)
        n = case["name"].split(":")[1].split(",")[0].strip()
        if n == "None": 
            n = None 
        name.append(n)
        
        pr.append("TN")
        country.append("it")
        web.append(" ")
        lat.append(case["has_latitude"])
        lon.append(case["has_longitude"])
        el.append(0.0)
        facType.append(case["facility_type"])
        today = date.today()
        d1 = today.strftime("%Y-%m-%d")
        upDate.append(d1)

        condition = locats.loc[locats.osm_ID == str(round(case["has_location"])), :] 
        try: 
            street.append(condition.street[0])
            house.append(condition.housenumber[0])
            
        except:
            street.append(" ") 
            house.append(" ")
        try: 
            city.append(condition.city[0])
        except: 
            city.append("Trento")

        elevator.append(False)
        if case["facility_type"] == "parking": 
            parking.append(True)
        else: 
            parking.append(False)
        guidanceS.append(False)
        #{'levelAccessibility': 'no', 'has_accessibleToilets': None, 'accessibilityDescription': None}
        arc = case["architecturalBarriers"].lstrip("{").rstrip("}").split(",")
        if arc[1].split(":")[1].strip() == 'None': 
            toil = False 
        else: 
            toil = True 
        toilet.append(toil)
        steps.append(False)
        ramp.append(False)
        if arc[2].split(":")[1].strip() == "None": 
            ins = None 
        else: 
            ins = arc[2].split(":")[1].strip()
        stairSlpe.append(ins)
        levAccess.append(arc[0].split(":")[1].strip())

new = pd.DataFrame({
    "has_ID" : id, 
    "has_officialName": name,
    "has_municipality": city,
    "has_province": pr,
    "has_country": country,
    "has_website": web,
    "has_latitude": lat,
    "has_longitude": lon,
    "has_elevation": el,
    "has_facilityType": facType,
    "has_uploadDate": upDate,
    "has_addr:street": street,
    "has_addr:housenumber": house,
    "has_accessibleElevator": elevator,
    "has_reservedParkinglots": parking,
    "has_guidanceSystem": guidanceS,
    "has_accessibleToilette": toilet,
    "has_steps": steps,
    "has_ramp": ramp,
    "has_staircaseSlope": stairSlpe,
    "has_levelOfAccessibility": levAccess 
})

pl["architecturalBarriers"] = arch_bar 

names = []
for x in pl["name"]: 
    n = x.split(":")[1].split(",")[0].strip()
    if n == "None": 
        n = None 
    names.append(n)

pl["name"] = names

pl.to_csv("facility.csv")
