from __future__ import absolute_import, annotations
import csv
from typing import Counter
from numpy import add
import pandas as pd
from pandas.core.reshape.merge import merge
import geopandas as gpd
import math 
import random 
from datetime import date
class accessibilityAPI():
    """
     Class getting the information from Convext Aware about the accessibility of facilities
     for people with physical disabilities.
     """

    def __init__(self):
        self.city = "trento"
        self.file_name = "accessibility_" + self.city + ".csv"

    def save_acc_file(self, path: str, city: str):
        """
        Open the files, clean them from wrongly encoded rows and save them locally.
        """
        self.city = city
        with open(path, "r", encoding="utf-8") as f:
            with open(self.file_name, "w", encoding="utf-8") as c:
                data = csv.reader(f, delimiter=";")
                my_writer = csv.writer(c, delimiter=";")
                not_save = ["ufficio", "unita'"]
                l = 250 # length of the rows
                if self.city == "trento":
                    l = 372
                for d in data:
                    if len(d) == l:
                        include = True
                        for word in d[0].split():
                            if word.lower() in not_save:
                                include = False
                                break
                        if include:
                            my_writer.writerow(d)

    def parse_acc_file(self):
        """
        Parse the information contained in the csv files
        and deleted specific columns, savinig them as separate files.
        """
        data = pd.read_csv(self.file_name, sep=";", engine='python')
        data.drop(labels=[x for x in data.columns if "NOTE" in x or "PM" in x or "AM" in x], axis=1, inplace=True)
        data.dropna(axis=1, inplace=True, thresh=20)
        if data['ID'].isnull().sum():  # check wheter some id's are missing
            data.dropna(axis=0, inplace=True, thresh=5)
        res = ["ID"] + [x for x in data.columns if "DESCRIZIONE" in x or "VALORE" in x]
        data[res].to_csv("Variables_acc_" + self.city + ".csv", sep = ",")
        data.drop(labels=res[1:], axis=1, inplace=True)
        data.to_csv("acc_" + self.city + "_parsed.csv", sep=",")

    def cleansing_file(self, file1, file2):
        pd_var = pd.read_csv(file1)
        pd_val = pd.read_csv(file2)

        pd_fin = merge(pd_var, pd_val, on="ID")
        pd_fin.drop("CATEGORIA 2", axis = 1)

        pdf = pd.DataFrame(pd_fin[["ID", "DENOMINAZIONE", "COMUNE", "PROVINCIA", "NAZIONE" , "SITO INTERNET", "LATITUDINE", "LONGITUDINE", 
        "ALTITUDINE", "CATEGORIA 1", "DATA RILEVAZIONE"]].copy())
        pdf.rename(columns = {"ID" : "ArchitecturalBarriers_ID", 
                            "DENOMINAZIONE": "has_officialName", 
                            "COMUNE" : "has_municipality", 
                            "PROVINCIA": "has_province", 
                            "NAZIONE" : "has_country", 
                            "SITO INTERNET": "has_website", 
                            "LATITUDINE": "has_latitude", 
                            "LONGITUDINE": "has_longitude", 
                            "ALTITUDINE": "has_elevation", 
                            "CATEGORIA 1": "has_facilityType", 
                            "DATA RILEVAZIONE" : "has_uploadDate"}, inplace = True)

        park = []
        elevator = []
        toilette = []
        guidance = []
        steps = []
        ramps = []
        ramp_descr =[]
        acc_level = []
        address =[]
        houseN =[]
        for ind, row in pd_fin.iterrows():
            row_dict = dict(row)
            pk = False 
            el = False
            san = False 
            guiS = False 
            descr = " "
            step = False 
            ramp = False 
            for case in list(row_dict.items()):
                if "AE-1a" in str(case[1]):
                    pk = True
                if "AI - 4f" in str(case[1]): 
                    el = True 
                if "AI-6e" in str(case[1]): 
                    san = True 
                if "AI-5b" in str(case[1]) or "AI-5a" in str(case[1]):
                    guiS = True
                if "AE-2c" in str(case[1]) or "AI - 4b" in str(case[1]):
                    step = True 
                if "AE-2d" in str(case[1]):
                    ramp = True 
                    if "DESCRIZIONE DECIMALE1 (ACCESSIBILITA' {})".format(case[0].split()[-1]) in row_dict.keys():
                        d3 = row_dict["DESCRIZIONE DECIMALE1 (ACCESSIBILITA' {})".format(case[0].split()[-1])]
                        d4 = row_dict["VALORE DECIMALE1 (ACCESSIBILITA' {})".format(case[0].split()[-1])]
                        if case[0].split()[-1] != "18" and case[0].split()[-1] != "17": 
                            if "DESCRIZIONE DECIMALE2 (ACCESSIBILITA' {})".format(case[0].split()[-1]) in row_dict.keys():
                                d5 = row_dict["DESCRIZIONE DECIMALE2 (ACCESSIBILITA' {})".format(case[0].split()[-1])]
                                d6 = row_dict["VALORE DECIMALE2 (ACCESSIBILITA' {})".format(case[0].split()[-1])] 
                                descr = "{}: {}; {}: {}".format(d3, d4, d5, d6)
                        else: 
                            descr = "{}: {}".format(d3, d4)
                    else:
                        descr = row_dict["DESCRIZIONE ACCESSIBILITA' {}".format(case[0].split()[-1])]
                if case[0] == "INDIRIZZO":
                    addr = " ".join([x.capitalize() for x in case[1].split(",")[0].lower().split()])
                    address.append(addr)
                    if case[1].find(",") > -1:   
                        houseN.append(case[1].split(",")[-1].strip("\t").split()[0].strip())
                    else: 
                        houseN.append(None)
                
            if not (pk + el + guiS + step + ramp): 
                acc_level.append("no")
            elif (pk + el + guiS + step + ramp) == 1: 
                acc_level.append("limited")
            else: 
                acc_level.append("yes")

            park.append(pk)
            elevator.append(el)
            toilette.append(san)
            guidance.append(guiS)
            steps.append(step)
            ramps.append(ramp)
            ramp_descr.append(descr)



        pdf["has_addr:street"] = address
        pdf["has_addr:housenumber"] = houseN
        pdf["has_accessibleElevator"] = elevator
        pdf["has_reservedParkinglots"] = park
        pdf["has_guidanceSystem"] = guidance
        pdf["has_accessibleToilette"] = toilette
        pdf["has_steps"] = steps
        pdf["has_ramp"] = ramps 
        pdf["has_staircaseSlope"] = ramp_descr
        pdf["has_levelOfAccessibility"] = acc_level

        return pdf 

ap = accessibilityAPI()
f1 = ap.cleansing_file("Variables_acc_trento.csv", "acc_trento_parsed.csv")
f2 = ap.cleansing_file("Variables_acc_rovereto.csv", "acc_rovereto_parsed.csv")

acc = pd.concat([f1, f2])
acc["has_ID"] = ["ab_" + str(x) + str(i) for i,x in enumerate(acc["has_ID"])]


def address_to_latlon(address):
  """
  From an address retrieve the relative 
  coordinates reported in WSG84 reference system (=degree).
  The API provider is ArcGIS.   
  @ return: lat, lon 
  """
  p = gpd.tools.geocode(address, provider="arcgis") 
  return p.geometry.y[0], p.geometry.x[0]

lat_lst =[]
lon_lst = []

for ind, x in acc.iterrows():
    #has_municipality,has_province,has_country has_addr:street,has_addr:housenumber
    if (len(x["has_addr:street"]) != 0) or not math.isnan(x["has_addr:street"]):
      if type(x["has_addr:housenumber"]) is str:
        loc = x["has_addr:street"] + "," + x["has_addr:housenumber"] + "," + x["has_municipality"] + ", Italia"
      else: 
        loc = x["has_addr:street"] + ", Trento, Italia"
    else: 
      loc = "Trento, Italia"
    lat, lon = address_to_latlon(loc)
    lat_lst.append(lat)
    lon_lst.append(lon)

acc["has_latitude"] = lat_lst 
acc["has_longitude"] = lon_lst


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

acc_new = pd.concat([acc, new])
acc_new.drop(["Unnamed: 0","Unnamed: 0.1"], inplace=True, axis = 1)
pl["has_location"] = [str(x) for x in pl["has_location"]]
locats.drop("Unnamed: 0", inplace=True, axis =1)
locats["postcode"] = [str(x) for x in locats["postcode"]]

pl.to_csv("facility_final.csv")
acc_new.to_csv("accessibility_final.csv")

# administrativeArea 
com = pd.read_excel("comuni_italiani.xlsx")

trento = str(round(com.loc[com["Denominazione in italiano"] == "Trento", "Codice Comune formato alfanumerico"].values[0]))
rovereto = str(round(com.loc[com["Denominazione in italiano"] == "Rovereto","CCodice Comune formato alfanumerico"].values[0]))


adm_area =[]
for ind, x in locats.iterrows():
    if x.city == "Rovereto":
        adm_area.append(rovereto)
    else:
        adm_area.append(trento)

locats["has_administrativeArea"] = adm_area

locats.to_csv("location_final.csv")




        