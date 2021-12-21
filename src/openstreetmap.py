import pygeos
import geopandas as gpd
import pyrosm
import matplotlib.pyplot as plt
import os
import requests
import pandas as pd
import json

class osmData():
    def __init__(self):
        self.download_pbf_url = "https://osmit-estratti.wmcloud.org/dati/poly/comuni/pbf/022205_Trento_poly.osm.pbf"

    def download_and_save(self, city, download_pbf_url):
        """
        Download and save the data from OpenStreetMap via Protocol Buffer
        """
        # download the data
        self.download_pbf_url = download_pbf_url
        r = requests.get(self.download_pbf_url, allow_redirects=True)
        #save the file in a PROTOCOL BUFFER
        self.city = city 
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

    def cleansing_file(self, file1, file2):
        """
        Cleans and merges two osm file in a final GEOjson file. 
        """
        with open(file1, "r", encoding="utf-8") as s:
            my_read = json.load(s)
            osm_1 = pd.DataFrame(my_read)
            osm_1.drop(["building:levels", "building:use", "addr:housename", "addr:place", 'social_facility', 'landuse',
                        "building:material", "ice_cream", "operator", "outdoor_seating", "shop", "wikipedia", "craft", "height",
                        "internet_access"], axis=1, inplace=True)
            print(osm_1.columns)

        with open(file2, "r", encoding="utf-8") as f:
            my_reader = json.load(f)
            osm_2 = pd.DataFrame(my_reader)
            osm_2.drop(["building:levels", "operator", "outdoor_seating", "shop", "wikipedia", "addr:housename", "internet_access"], axis=1, inplace=True)

            osm = pd.concat([osm_1, osm_2], axis=0, join="outer")


            # to delete -> slipway, tanning_salon in leisure
            # to delete -> yes, kindergarten, detached, hospital, bunker per building
            del_dict={"amenity" : ["hunting_stand", "courthouse", "bench", "stripclub", "gambling"],
                    "leisure" : ["slipway", "tanning_salon"],
                    "building" : ["yes", "kindergarten", "detached", "hospital", "bunker"]}

            for key in del_dict:
                osm = osm.set_index(key)
                osm.drop(del_dict[key], axis=0, inplace=True)
                osm.reset_index(drop=False, inplace=True)

            tags_lst = ['wheelchair:description',
                'contact:tripadvisor',
                "wheelchair",
                'contact:phone',
                'diet:vegetarian',
                'official_name',
                'contact:email',
                'addr:suburb',
                'diet:gluten_free',
                'contact:facebook',
                'sport',
                        'short_name',
                        'smoking',
                        'contact:mobile',
                        'contact:website',
                        'capacity', 'description', 'hiking', 'name:en',
                        'cuisine', 'diet:vegan', 'name:it',
                        'toilets:wheelchair',
                        'contact:instagram']

            def find_tag(osm, name, ind):
                try:
                    found = osm.iloc[ind]['tags'][name]
                    return found
                except:
                    return None

            osm.dropna(subset=['lat', 'lon'], inplace=True)
            new_osm = {}
            for ind, case in enumerate(list(osm.iterrows())):
                new_dict = {"has_latitude": osm.iloc[ind]["lat"],
                            "has_longitude": osm.iloc[ind]["lon"],
                            "address": {"city": osm.iloc[ind]["addr:city"] or find_tag(osm, 'addr:suburb', ind),
                                        "country": osm.iloc[ind]["addr:country"] or "Italy",
                                        "housenumber": osm.iloc[ind]['addr:housenumber'],
                                        "postcode": osm.iloc[ind]["addr:postcode"],
                                        "street": osm.iloc[ind]["addr:street"],
                                        "region": "Trentino-Alto Adige"
                                        },
                            "contact": {"has_email": osm.iloc[ind]['email'] or find_tag(osm, "contact:email", ind),
                                        "has_phone": osm.iloc[ind]["phone"] or find_tag(osm, "contact:phone", ind) or
                                                    find_tag(osm, "contact:mobile", ind),
                                        "has_website": osm.iloc[ind]["website"] or find_tag(osm, "contact:website", ind),
                                        "has_socialNetwork": [x for x in [find_tag(osm, "contact:tripadvisor", ind)] + [
                                            find_tag(osm, "contact:facebook", ind)] + [
                                                                find_tag(osm, "contact:instagram", ind)] if x is not None]
                                        },
                            "information": osm.iloc[ind]["information"] or find_tag(osm, "description", ind) or "no information specified",
                            "opening_hours": osm.iloc[ind]["opening_hours"] or None,
                            "facility_type": osm.iloc[ind]["amenity"] or osm.iloc[ind]["building"] or osm.iloc[ind]["tourism"] or osm.iloc[ind]["leisure"] or osm.iloc[ind]["parking"],
                            "smoking": find_tag(osm, "smoking", ind) and False,
                            "architecturalBarriers": {
                                "levelAccessibility": find_tag(osm, "wheelchair", ind) or "no",
                                "has_accessibleToilets": find_tag(osm, 'toilets:wheelchair', ind),
                                "accessibilityDescription": find_tag(osm, "wheelchair:description", ind)
                            },
                            "name":{
                                "has_officialName": osm.iloc[ind]["name"] or find_tag(osm, 'official_name', ind) or find_tag(osm, "name:it", ind),
                                "has_shortName": find_tag(osm, 'short_name', ind),
                                "has_name_en": find_tag(osm, "name:en", ind)
                            },
                            "sport": find_tag(osm, "sport", ind),
                            "has_capacity": find_tag(osm, "capacity", ind),
                            "menu": {
                                "cuisine": find_tag(osm, "cuisine", ind),
                                "isVegetarian": find_tag(osm, 'diet:vegetarian', ind),
                                "isVegan": find_tag(osm, 'diet:vegan', ind),
                                "isGlutenFree": find_tag(osm, 'diet:gluten_free', ind),
                            },
                            "hiking": find_tag(osm, "hiking", ind)
                            }
                new_osm[str(osm.iloc[ind]["id"])] = new_dict

            with open('osm_data.json', 'w') as fp:
                json.dump(new_osm, fp)


osm = osmData()
osm.cleansing_file("rovereto_osm.json", "trento_osm.json")