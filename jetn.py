import os, csv, json


class jetnData():

    def __init__(self, file_name='JETN_report_climbing_gap.csv'):
        self.file_name = file_name

    def clean_jetn(self):
        """
        Cleans the dataset obtained from Eventbrite.com. Due to privacy issues,
        the original data are neither displayed nor stored in the project repository.
        """
        path = os.getcwd()
        jd = {}
        with open(os.path.join(path, self.file_name), encoding="utf-8") as f:
            dic = csv.DictReader(f, delimiter=';')
            for d in dic:
                for k in d:
                    jd[k.replace('\ufeff', '')] = d[k]

                with open('{}\{}.json'.format(path, 'JETN_climbing_gap'), 'a', encoding='utf-8') as f:
                    json.dump(jd, f, ensure_ascii=False, indent=4, default=str)

    def parse_jetn(self):
        """
        Filters the participant state to detect possible changes among individuals.
        Summarises the event in an unique json by reporting the overall number of participants.
        """
        with open(self.file_name, "r", encoding="utf-8") as json_file:
            data = json.load(json_file)
            ret = set()
            for case in data:
                if case["Stato partecipante"] not in ret:
                    ret.add(case["Stato partecipante"])
            with open("jetn_event.json", "w", encoding="utf-8") as f:
                new_data = data[0]
                new_data["Stato partecipante"] = list(ret)
                new_data["Totale partecipanti"] = len(data)
                f.write(json.dumps(new_data, indent=4, ensure_ascii=True))



