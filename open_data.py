from __future__ import absolute_import, annotations
import argparse
import json
import time
import requests
from datetime import date, datetime


class opendataAPI:
    """
    Class getting the information from Open Trentino
    """

    def __init__(self):
        self.city = "trento"
        self.file_name = "opendata_" + self.city + ".json"

    def get_events(self, url, city):
        df = requests.get(url)
        data = df.json()
        self.city = city
        with open(self.file_name, "w", encoding="utf-8") as f:
            final_str = json.dumps(data, indent=4,
                                   sort_keys=False,
                                   separators=(",", ": "),
                                   ensure_ascii=False)

            f.write(final_str)

    @staticmethod
    def parse_events(file_name: str):
        with open(file_name, "rb") as f:
            months = {"genn": "01",
                      "febb": "02",
                      "marz": "03",
                      "apri": "04",
                      "magg": "05",
                      "giug": "06",
                      "lugl": "07",
                      "agos": "08",
                      "sett": "09",
                      "otto": "10",
                      "nove": "11",
                      "dice": "12"
                      }
            stopwords = ["ogni", "tutti"]
            content = json.load(f)
            list_dict = []
            for event in content:
                new_dict = {
                    "immagine": event["immagine"],
                    "url": event["url"],
                    "abstract_text": event["abstract_text"],
                    "abstract": event["abstract"],
                    "title": event["nome"],
                    "lon": event["lon"],
                    "modifica": event["modifica"],
                    "link": event["link"],
                    "lat": event["lat"]
                }
                try:
                    lst = event["indirizzo"].split()
                    weekday = []
                    duration = []
                    dates = []
                    month = []
                    location = []
                    year = []
                    for el in lst:
                        if el.lower() in ["lunedì", "martedì", "mercoledì", "giovedì", "venerdì", "sabato", "domenica"]:
                            weekday.append(el.lower())
                        elif ("." in el or "," in el or ":" in el) and len(el) == 5 and el[:2].isdigit():
                            if "." in el:
                                duration.append(el.replace(".", ":"))
                            elif "," in el:
                                duration.append(el.replace(",", ":"))
                        elif el.isdigit() and len(el) == 4:
                            year.append(el)
                        elif el.isdigit() and int(el) <= 31:
                            dates.append(el)
                        elif el.lower()[:4] in months:
                            month.append(months[el.lower()[:4]])
                        else:
                            location.append(el)

                    start_day = "01"
                    end_day = "30"
                    if len(dates):
                        start_day = min(dates)
                        end_day = max(dates)
                    start_month = "01"
                    end_month = "12"
                    if len(month):
                        if len(month) == 2:
                            start_month, end_month = month[0], month[1]
                        elif len(month) > 2:
                            start_month, end_month = month[0], month[0]
                            end_day = start_day
                        else:
                            start_month = month[0]
                            end_month = start_month
                    start_year, end_year = date.today().year, date.today().year
                    if len(year):
                        start_year = min(year)
                        end_year = max(year)
                    start_date = date(year=int(start_year), month=int(start_month), day=int(start_day))
                    end_date = date(year=int(end_year), month=int(end_month), day=int(end_day))
                    regular_basis = False
                    for word in location:
                        if word in stopwords:
                            regular_basis = True
                        if word == "sino" or word == "fino" and start_date == end_date:
                            start_date = "1"
                    if len(duration) >= 4:
                        new_dict["schedule"] = True
                        new_dict["indirizzo"] = event["indirizzo"]
                        list_dict.append(new_dict)
                    else:
                        if len(duration) > 2:
                            duration[0] = min(duration)
                            duration[1] = max(duration)
                            duration.pop()
                        new_dict["duration_days"] = str([start_date, end_date])
                        new_dict["duration_hours"] = str(tuple(duration))
                        new_dict["weekday"] = str(weekday)
                        new_dict["indirizzo"] = str(location)
                        new_dict["repeated"] = str(regular_basis)
                        list_dict.append(new_dict)
                except:
                    new_dict["indirizzo"] = event["indirizzo"]
                    list_dict.append(new_dict)
            return list_dict
    @staticmethod
    def parse_events_tn(filename: str):
        with open(filename, "rb") as f:
            content = json.load(f)
            lst = []
            for event in content["searchHits"]:
                new_dict = {
                    "metadata": event["metadata"],
                    "data": event["data"]
                }
                lst.append(new_dict)
            return lst




    def save_file(self):
        if self.city == "rovereto":
            with open("opendata_rovereto_parsed.json", "w") as s:
                data = self.parse_events(self.file_name)
                json.dump(data, s, indent=4)
        else:
            with open("opendata_" + self.city + "_parsed.json", "w") as s:
                data = self.parse_events_tn(self.file_name)
                json.dump(data, s, indent=4)
