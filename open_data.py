from __future__ import absolute_import, annotations
import argparse
import json
import time
import requests


class opendataAPI:
    def __init__(self, url):
        self.url = url

    def get_events(self, city):
        df = requests.get(self.url)
        data = df.json()
        file_name = "opendata_" + city.lower() + ".json"
        with open(file_name, "w", encoding="utf-8") as f:
            final_str = json.dumps(data, indent=4,
                                   sort_keys=False,
                                   separators=(",", ": "),
                                   ensure_ascii=False)
            f.write(final_str)


