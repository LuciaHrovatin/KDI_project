import json
import requests

class meetupAPI:

    def __init__(self, url):
        self.url = url
        self.file_name = "meetup_data.json"

    def parsing_events(self):
        df = requests.get(self.url)
        data = df.json()

        with open(self.file_name,"w", encoding="utf-8") as f:
            final_str = json.dumps(data, indent=4,
                                   sort_keys=True,
                                   separators=(",", ": "),
                                   ensure_ascii=False)
            f.write(final_str)

