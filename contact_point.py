import pandas as pd 
import numpy as np
from geopy.geocoders import Nominatim
import math 

pdf = pd.read_csv("organization_trentino.csv")

pdf_contact = pd.DataFrame({"has_fax" : pdf.has_fax, 
                            "has_email": pdf.has_email, 
                            "has_website": pdf.has_website, 
                            "has_socialNetwork" : pdf.has_socialNetwork, 
                            "has_phone" : pdf.has_phone}, index=None) 

np.random.seed(1)

pdf_osm = pd.read_json("osm_data.json")
pdf_osm_ID = pd.DataFrame(columns = list(pdf_osm.index)) 
pdf_osm_ID["has_location"] = list(pdf_osm.columns) 

for ind, x in enumerate(list(pdf_osm.columns)):
    pdf_osm_ID.loc[ind, pdf_osm_ID.columns != "has_location"] = pdf_osm[x]


contact_location = pd.DataFrame([x for x in pdf_osm_ID["contact"]], 
                                columns = ["has_email",
                                            "has_phone", 
                                            "has_website", 
                                            "has_socialNetwork"])

addr_location = pd.DataFrame([x for x in pdf_osm_ID["address"]], 
                            columns = list(pdf_osm_ID["address"][0].keys()))
addr_location["osm_ID"] = list(pdf_osm.columns)
addr_location["has_latitude"] = pdf_osm_ID["has_latitude"]
addr_location["has_longitude"] = pdf_osm_ID["has_longitude"]

addr = pd.DataFrame({"city" : pdf['has_municipality'], 
                    "housenumber": pdf['has_addr:housenumber'], 
                    "postcode": pdf['has_addr:postcode'], 
                    "street" :  pdf['has_addr:street'],
                    "has_latitude": pdf["has_latitude"],
                    "has_longitude": pdf['has_longitude']})

addr_location = pd.concat([addr_location, addr])
addr_location["has_province"] = "TN"
addr_location["country"] = "it"
addr_location["region"] = "Trentino-Alto Adige"


res = pd.concat([pdf_contact, contact_location], axis=0, join="outer") 


# create a list of unique codes
codes = res.shape[0]

# generte ids
ids = ["cp_" + str(x) for x in list(np.random.randint(low=1e9, high=1e10, size = codes))]

# add new ids column
res['has_contact_ID'] = ids

pdf["has_contactPoint"] = ids[:pdf_contact.shape[0]]
pdf_osm_ID["has_contactPoint"] = ids[pdf_contact.shape[0]:]
 

for x in ["Unnamed: 0", 'has_fax', 'has_phone', 'has_email', 'has_website', 'has_socialNetwork', 'has_municipality', 
         'has_addr:housenumber', 'has_addr:postcode','has_addr:street']:
    pdf.drop(x,  inplace= True, axis = 1)

pdf_osm_ID.drop(["contact", "address"], inplace= True, axis = 1)

pdf["has_foundationYear"] = pd.to_datetime(pdf["has_foundationYear"], format='%Y', errors='coerce')

pdf_osm_ID.to_csv("facility_data.csv", encoding = "utf-8")
pdf.to_csv("organization.csv", encoding = "utf-8")
res.to_csv("contactPoint.csv", encoding = "utf-8")

addr_location.drop_duplicates(keep=False, inplace= True)

geolocator = Nominatim(user_agent="Chrome/86.0.4240.75")

def reverse_geocoding(lat, lon):
  latlon = str(lat) + "," + str(lon)
  location = geolocator.reverse(latlon)
  return location.raw["osm_id"]

osm_lst =[]

for ind, x in addr_location.iterrows():
    if math.isnan(x["osm_ID"]):
        osm_lst.append(reverse_geocoding(x["has_latitude"], x["has_longitude"]))
    else: 
        osm_lst.append(x["osm_ID"])

addr_location["osm_ID"] = osm_lst

addr_location.to_csv("location.csv", encoding = "utf-8")