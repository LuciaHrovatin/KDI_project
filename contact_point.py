import pandas as pd 
import numpy as np
from pandas.core.indexing import convert_to_index_sliceable
import json 

pdf = pd.read_csv("organization_trentino.csv")

# Extract has_fax', 'has_phone', 'has_email', 'has_website', 'has_socialNetwork'

pdf_contact = pd.DataFrame({"has_fax" : pdf.has_fax, 
                            "has_email": pdf.has_email, 
                            "has_website": pdf.has_website, 
                            "has_socialNetwork" : pdf.has_socialNetwork, 
                            "has_phone" : pdf.has_phone}, index=None) 

np.random.seed(1)

pdf_osm = pd.read_json("osm_data.json")
pdf_osm_ID = pd.DataFrame(columns = "o") 
pdf_osm["osm_ID"] = list(pdf_osm.columns) 



# create a list of unique codes
codes = pdf_contact.shape[0]

# generte ids
ids = ["cp_" + str(x) for x in list(np.random.randint(low=1e9, high=1e10, size = codes))]

# add new id column
pdf_contact['contact_ID'] = ids 
pdf["has_contactPoint"] = ids
for x in ["Unnamed: 0", 'has_fax', 'has_phone', 'has_email', 'has_website', 'has_socialNetwork']:
    pdf.drop(x,  inplace= True, axis = 1)

pdf.to_csv("organization.csv", encoding = "utf-8")
pdf_contact.to_csv("contactPoint.csv", encoding = "utf-8")
