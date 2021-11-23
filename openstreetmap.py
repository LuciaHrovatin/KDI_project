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

    osm = osm.set_index("amenity")
    osm.drop(["hunting_stand", "courthouse", "bench"], axis=0, inplace=True)
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
    type_tags = []
    for ind, x in enumerate(osm["tags"]):
        if x is not None:
            type_tags.extend(list(x.keys()))
    print(set(type_tags))
    #for ind, x in enumerate(osm["building"]):
    #    if x is not None:
    #        type_amenity.append(x)
    #print(set(type_amenity))

