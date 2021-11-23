#import pygeos
#import geopandas as gpd
#import pyrosm
import matplotlib.pyplot as plt
import os
import requests
"""
class osmData():
    def __init__(self, city):
        self.city = city.lower()
        self.download_pbf_url = "https://osmit-estratti.wmcloud.org/dati/poly/comuni/pbf/022205_Trento_poly.osm.pbf"

    def download_and_save(self):
"""
"""
       # Download and save the data from OpenStreetMap via Protocol Buffer

        # download the data
        r = requests.get(self.download_pbf_url, allow_redirects=True)
        #save the file in a PROTOCOL BUFFER
        open('{}.pbf'.format(self.city), 'wb').write(r.content)
        osm = pyrosm.OSM("{}.pbf".format(self.city))
        custom_filter = {"tourism": True,
                         "leisure": True,
                         "building": True,
                         "amenity": ['cafe', 'casino','cinema', 'college','gambling','language_school', 'library', 'music_school',
                                    'nightclub', 'parking','planetarium','pub','restaurant','social_centre','social_facility',
                                    'spa','start_date','stripclub','taxi','theatre','university','wikipedia', "source"]}
        data_osm = osm.get_pois(custom_filter=custom_filter)
        colum_remove = ["osm_type", "version", "timestamp", "changeset", "source", "ref"]
        if self.city == "trento":
            colum_remove.append("start_date")
        for x in colum_remove:
            del data_osm[x]

        data_osm.to_file("./{}_osm.json".format(self.city), driver="GeoJSON")
    """

import pandas as pd
import json
#def merge_datasets(file1, file2):
accessibility = pd.read_csv("acc_trento_parsed.csv", encoding = "utf-8")


with open("trento_osm.json", "r", encoding = "utf-8") as f:
    my_reader = json.load(f)
    osm = pd.DataFrame([x["properties"] for x in my_reader["features"]])
    del osm["building:levels"]
    del osm["operator"]
    osm = osm.set_index("amenity")
    osm.drop(["hunting_stand", "courthouse", "bench", "stripclub", "gambling"], axis=0, inplace=True)
    osm.reset_index(drop=False, inplace=True)
    type_amenity = []

    # to delete -> slipway, tanning_salon in leisure
    # to delete -> yes, kindergarten, detached, hospital, bunker per building
    osm = osm.set_index("leisure")
    osm.drop(["slipway", "tanning_salon"], axis=0, inplace=True)
    osm.reset_index(drop=False, inplace=True)
    type_amenity = []

    osm = osm.set_index("building")
    osm.drop(["yes", "kindergarten", "detached", "hospital", "bunker"], axis=0, inplace=True)
    osm.reset_index(drop=False, inplace=True)
    type_amenity = []

    print(osm.shape)
    new_columns = {}
    lst = ['club', 'wheelchair:description', 'check_date:opening_hours', 'contact:tripadvisor',
           'direction', 'park_ride',
           "wheelchair", 'contact:phone', 'diet:vegetarian', 'parking:condition:time_interval', 'official_name', 'contact:email',
           'addr:suburb', 'diet:gluten_free', 'covered', 'payment:bancomat', 'reservation',
           'supervised', 'fee', 'contact:facebook', 'sport',
           'short_name', 'smoking', 'contact:mobile', 'contact:website', 'capacity', 'description', 'hiking', 'name:en',
           'social_facility:for', 'cuisine', 'access', 'destination', 'diet:vegan', 'note', 'maxstay', 'name:it', 'toilets:wheelchair',
           'contact:instagram', 'parking:condition', 'bicycle']

    for ind, x in enumerate(osm["tags"]):
        if x is not None:
            keys = list(x.keys())
            for k in keys:
                if k not in osm.columns and k not in new_columns.keys() and k in ['parking:condition', 'bicycle', 'wikidata', 'entrance']:
                    new_columns[k] = [(ind, x[k])]
                elif k in new_columns.keys():
                    new_columns[k].append((ind, x[k]))


    from pprint import pprint
    pprint(osm.columns)
    #contact{
    # --> website: url
    # --> email: string
    # --> mobile or phone: string
    # --> social: [] of url}
    # payment{
    # --> cash: string
    # --> card: string}

    # name{
    # name_it: string,
    # name_en: string,
    # short_name: string,
    # official_name: string}

    # wheelchair{
    # level_of_accessibility: "YES"/"NO"/"LIMITED",
    # description: string
    # toilettes: "yes"/"no"
    # }

    # parking{
    # condition: string}

    # cuisine {
    # type: cuisine(str)
    # isVegan:
    # isVegetarian:
    # isGlutenFree:
    # }


