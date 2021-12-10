
from __future__ import absolute_import, annotations
import json
from pandas.io.parsers import read_csv
import requests
from datetime import date
import pandas as pd 
import random 

class opendataORG:
    """
    Class getting the information from Open Trentino
    """

    def __init__(self):
        self.city = "trento"
        self.file_name = "organization_" + self.city + ".json"

    def get_organization(self, url):
        df = requests.get(url)
        data = df.json()
        with open(self.file_name, "w", encoding="utf-8") as f:
            final_str = json.dumps(data, indent=4,
                                   sort_keys=False,
                                   separators=(",", ": "),
                                   ensure_ascii=False)

            f.write(final_str)

#pd_open = pd.read_csv("organization_open.csv", encoding="utf-8", )

with open("organization_trento.json", "r") as f: 
    fn = json.load(f)
    pdf = pd.DataFrame(columns=["has_organizationID", 
                                "has_name",
                                "has_description",
                                "has_address",
                                "has_postalcode", 
                                "has_municipality", 
                                "has_fax", 
                                "has_phone", 
                                "has_email", 
                                "has_website",
                                "has_socialNetwork", 
                                "has_organizationType", 
                                "has_category",
                                "has_hashtag", 
                                "has_administrator", 
                                "has_administratorRole", 
                                "has_logo", 
                                "has_foundationYear", 
                                "has_fiscalCode", 
                                "has_administratorPhone", 
                                "has_administratorAddress"]) 
                               # "has_fiscalCode"])
    
    for case in fn["searchHits"]:
        lst = []
        lst.append("org_" + (case["data"]["ita-IT"]["cod_associazione"] or str(random.randint(1000, 100000))))
        lst.append(case["data"]["ita-IT"]["titolo"])  
        lst.append(case["data"]["ita-IT"]["abstract"])
        lst.append(case["data"]["ita-IT"]["indirizzo"])
        lst.append(case["data"]["ita-IT"]["cap"])
        lst.append(case["data"]["ita-IT"]["localita"])
        lst.append(case["data"]["ita-IT"]["fax"])
        lst.append(case["data"]["ita-IT"]["telefono"] or case["data"]["ita-IT"]["numero_telefono1"])
        lst.append(case["data"]["ita-IT"]["email"])
        lst.append(case["data"]["ita-IT"]["url"])
        lst.append(case["data"]["ita-IT"]["url_facebook"])
        lst.append(case["data"]["ita-IT"]["categoria"]) #or case["data"]["ita-IT"]["materia"]["name"]["ita-IT"].lower()) 
        lst.append(case["data"]["ita-IT"]["categoria"] or case["data"]["ita-IT"]["argomento"])# or case["data"]["ita-IT"]["materia"]["name"]["ita-IT"].lower())
        lst.append(case["data"]["ita-IT"]["parola_chiave"]) 
        lst.append(case["data"]["ita-IT"]["referente_nome"])
        lst.append(case["data"]["ita-IT"]["referente_ruolo"])
        lst.append(case["data"]["ita-IT"]["image"])
        lst.append(case["data"]["ita-IT"]["data_inizio_validita"].split("-")[0]) 
        lst.append(case["data"]["ita-IT"]["referente_telefono"])
        lst.append(case["data"]["ita-IT"]["referente_indirizzo"])

        #lst.append(pd_open.iloc[pd_open["remoteID"] == case["metadata"]["remoteId"], "Codice Fiscale"])

        pdf = pdf.append(lst, ignore_index=True)

print(pdf.columns)




