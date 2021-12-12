
from __future__ import absolute_import, annotations
import json
from numpy import nan
from pandas.io.parsers import read_csv
import requests
from datetime import date
import pandas as pd 
import random 
import math 
import re
from html import unescape

pd_open = pd.read_csv("org_trento.csv", encoding="utf-8", )

def foundationYear(str_year):
    if type(str_year) is str:
        year = re.search(r'\d+', str_year)
        if year is not None:
            if len(year.group()) == 4: 
                return year.group() 
    return None  

pdf = pd.DataFrame(columns=["has_organizationID", 
                                "has_name",
                                "has_description",
                                "has_addr:street",
                                "has_addr:housenumber",
                                "has_addr:postcode",
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
                                "has_administratorPhone", 
                                "has_administratorAddress",
                                 "has_fiscalCode"])

for int, case in pd_open.iterrows():
    lst = []
    if math.isnan(case["Codice"]) or case["Codice"] == 0.0:
        cod = str(random.randint(1000, 100000))
    else: 
        cod = str(round(case["Codice"]))
    lst.append("org_" + cod)
    lst.append(case["Nome"])  
    if type(case["Abstract (descrizione in breve)"]) is float and math.isnan(case["Abstract (descrizione in breve)"]):
        if type(case["Scheda"]) is float and math.isnan(case["Scheda"]):
            descr = None 
        else:
            descr = unescape(case["Scheda"])
    else: 
        descr = unescape(case["Abstract (descrizione in breve)"])
    lst.append(descr)
    addr = case["address"] or case["Indirizzo"]
    street = None 
    houseN= None 
    if addr is not None:
        addr = str(addr).split(",")
        if addr[0].startswith("Via") or addr[0].startswith("Vicolo") or addr[0].startswith("Corso") or addr[0].startswith("Piazza") or addr[0].startswith("Piazzale"): 
            street = unescape(addr[0])

        for x in addr: 
            if "Via" in x or "Vicolo" in x or "Corso" in x or "Piazza" in x: 
                street = unescape(x)

            if x.isnumeric():
                houseN = x
    
    lst.append(street)
    lst.append(houseN)
    if not math.isnan(case["CAP"]):
        cap = str(round(case["CAP"]))
        lst.append(cap)
    else: 
        lst.append(case["CAP"])
    if ("Trento" in str(case["Località"])) or ("Rovereto" in str(case["Località"])) or ("Mezzolombardo" in str(case["Località"])) or case["Località"]is None:
        lst.append(case["Località"])
        lst.append(case["Fax"])
        lst.append(case["Telefono"] or case["Telefono alternativo"])
        lst.append(case["E-mail"])
        lst.append(case["Sito WEB"])
        lst.append(case["Pagina Facebook"])
        lst.append(case["Categoria"]) 
        lst.append(case["Materia"] or case["Categoria"]) 
        lst.append(case["Parola chiave"]) 
        lst.append(case["Referente"])
        lst.append(case["Ruolo del referente"])
        lst.append(case["Immagine"])
        lst.append(foundationYear(case["Scheda"]) or str(case["Data di inizio validità"]).split("-")[0] or None)
        lst.append(case["Telefono del referente"])
        lst.append(case["Indirizzo del referente"])

        cf = case['Codice Fiscale']
        if math.isnan(cf):
            cf = None 
        lst.append(cf or case["Partita IVA"])

        pdf.loc[pdf.shape[0]]  = lst 


student_org = {
    'has_organizationID': ["org_172635", "org_29384746", "org_64927461", "org_283650", "org_5284351", "org_1723549", "org_227366", "org_1827364"],
    'has_name': ["ACROPOLI - Associazione di promozione sociale","AIESEC","ESN - Associazione Erasmus Student Network", "JETN - Junior Enterprise Trento", "L'Universitario", "UDU Trento - Unione Degli Universitari di Trento", "UNITN - Rete degli studenti dell'Università di Trento", "SAT Trento - Società degli Alpinisti Tridentini Sezione di Trento"],
    'has_description': ["Acropoli è una piattaforma per la promozione degli aspetti più innovativi dell’architettura. La nostra associazione mette in connessione giovani creativi come architetti, ingegneri e designer, con realtà professionali e culturali.", "AIESEC (Association Internationale des Etudiants en Sciences Economiques et Commerciales) è un'associazione studentesca, senza fini di lucro, indipendente, apartitica, apolitica. AIESEC, con la sua presenza in 127 paesi del mondo, è la più grande organizzazione internazionale al mondo, interamente gestita da studenti, con un network con più di 86.000 studenti provenienti da più di 2400 università, attiva da più di 65 anni","Sezione di Trento dell'Erasmus Student Network (ESN), organizzazione internaionale non-profit international. La missione principale è di rappresentare gli studenti internazionali, promuovere l'interculatirà e lo sviluppo personale secondo in principio: Students Helping Students.", "JETN nasce il 24 Febbraio 2015 per iniziativa di un gruppo di sette studenti dell’Università di Trento. Fa parte di JE Italy e JE Europe, rispettivamente le confederazioni italiana ed europea delle Junior Enterprises. Una JE è un’organizzazione no-profit costituita interamente da studenti universitari. Al pari di un’azienda, ha un consiglio di amministrazione e delle aree operative coordinate da responsabili, rispettivamente Area Commerciale, Marketing, Risorse Umane, Legale.", "L’Universitario è un giornale nato nel 2016 a Trento per riempire un vuoto. L’esigenza di dare spazio alla voce degli studenti, alla loro voglia d’interpretare la realtà con gli strumenti e la curiosità che li contraddistingue. L’idea partita da pochi si è allargata a molti. È nata un’associazione che fa da editore, una redazione strutturata per aree tematiche, uno statuto ed un codice etico che dettano le regole del gioco. L’Universitario ha un’edizione cartacea trimestrale (distribuita gratuitamente) e una versione online.", "L'UDU Trento - Unione degli Universitari di Trento è il sindacato degli studenti e delle studentesse dell'Università di Trento e nasce nel 2012 come membro confederato della più ampia associazione nazionale UDU - Unione degli Universitari.", "UNITiN è una realtà nata nel 2012 con l'obiettivo di unire e rappresentare tutti gli studenti del Trentino. Siamo un'associazione composta da più di 60 studenti di tutti i dipartimenti, che ha come obiettivo primario quello di costruire un'università di studenti e per gli studenti.", "Associazione di promozione sociale Sezione del Club Alpino Italiano (CAI)"],
    'has_addr:street': ["Via Mesiano", "Via Vigilio Inama", "Via Virgilio Inama", "Via Torre Verde", "Via degli Orbi", "Via Vigilio Inama", "Via Vigilio Inama", "Via Manci"],
    'has_addr:housenumber': ["77", "5", "5", "21", "4", "5", "5", "57"],
    'has_addr:postcode': ["38123", "38122", "38122","38122","38122", "38122", "38122", "38122" ],
    'has_municipality': ["Trento", "Trento", "Trento","Trento","Trento", "Trento", "Trento", "Trento"],
    'has_fax': [None, None, None, None, None, None, None, "80003990225"], 
    'has_phone': ["+393407716783", "+393495126105","+390461882248","", "", "+393406228305", "", "0461 987025"],
    'has_email': ["acropolitrento@gmail.com", "", "trento@esn.it", "info@jetn.it", "redattore@luniversitario.it", "udu.trento@gmail.com", "unitinews@gmail.com", "sat.trento@gmail.com"],
    'has_website': ["https://www.acropolitrento.com", "https://www.aiesec.it", "https://trento.esn.it", "https://www.jetn.it", "https://www.luniversitario.it", "https://www.udutrento.it", "https://www.unitintrento.it", "http://www.sattrento.it"],
    'has_socialNetwork': [["https://www.instagram.com/acropolitrento/", "https://www.facebook.com/Acropolitrento"], None, ["https://www.facebook.com/groups/2054507961289050/?fref=nf"],["https://www.facebook.com/jetn7/", "https://www.instagram.com/jetn_trento/", "https://www.linkedin.com/company/jetn/"], ["https://www.instagram.com/luniversitario/","https://www.facebook.com/luniversitario", "https://www.youtube.com/channel/UC-IGIS0eferm8nP3_ghlAlw"], ["https://www.facebook.com/udutrento/", "https://www.instagram.com/udutrento/"], ["https://www.facebook.com/unitintrento/", "https://www.instagram.com/unitintrento/?hl=it"], ["https://www.facebook.com/satcentrale/?ref=bookmarks", "https://www.instagram.com/sat_centrale/" , "https://www.youtube.com/channel/UCyOXYnF9dBk_7MrvzjYnR-w"]],
    'has_organizationType': ["associazione studentesca", "volontariato per studenti", "associazione studentesca internazionale", "associazione studentesca", "associazione studentesca", "associazione di rappresentanza politica studentesca", "associazione di rappresentanza politica studentesca", "associazione alpinistica"],
    'has_category': [["design", "architettura"], ["volontariato"], ["associazione no-profit"], ["associazione no-profit"], ["giornalismo studentesco"], ["rappresentanza studentesca"], ["rappresentanza studentesca"], ["alpinismo"]],
    'has_hashtag': [["design", "studenti"], ["volontariato", "studenti"], ["studenti internazionali"], ["studenti",  "università", "enterprise", "marketing"], ["giornalismo studentesco", "università", "studenti"], ["università", "studenti", "rappresentanza politica"], ["università", "studenti", "rappresentanza politica"], ["alpinismo", "montagna", "promozione sociale"]],
    'has_administrator': ["Federico Casagrande","", "Laura Cattoni", "Irene Ambrosi", "Niccolò Bonato", "", "", "Ugo Scorza"],
    'has_administratorRole': ["presidente","", "presidente", "presidente", "presidente", "", "", "presidente"],
    'has_logo': ["https://images.app.goo.gl/c7JA8WBEc1BrUoDQ6", "https://images.app.goo.gl/rTtYn1Y5Rgx6mm83A", "https://images.app.goo.gl/4Nubc9imHPeof8oE9", "https://images.app.goo.gl/nW1p7MXG8mwV6Q2N9", "https://images.app.goo.gl/TY47RXbDDbMtUFhK9", "https://images.app.goo.gl/PcNNb4TgxgG3S3tg6", "https://images.app.goo.gl/GZQwsXdYTwNiAZnq9", "https://images.app.goo.gl/PJQhFdvyRSMidhyCA"],
    'has_foundationYear':["2016", "1948", "1992", "2015", "2016", "2012", "2012", "1921"], 
    'has_administratorPhone':["+393407716783", "", "", "", "", "", "", ""],
    'has_administratorAddress': ["", "","laura.cat@gmail.com", "", "", "", "", ""],
    'has_fiscalCode':["96105250227", "97080730159", "92105850348", "02426890220", "00340520220","00340520220","00340520220", "80003990225"]}


student_org = pd.DataFrame(student_org)
pdf = pd.concat([pdf, student_org])

pdf.to_csv("organization_trentino.csv", encoding="utf-8")



