import pygeos
import geopandas as gpd
import pyrosm
import matplotlib.pyplot as plt
import os
import requests

class osmData():
    def __init__(self, city):
        self.city = city.lower()
        self.download_pbf_url = "https://osmit-estratti.wmcloud.org/dati/poly/comuni/pbf/022205_Trento_poly.osm.pbf"

    def download_and_save(self):
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



