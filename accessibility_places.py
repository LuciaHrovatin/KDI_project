from __future__ import absolute_import, annotations
import csv
import pandas as pd

class accessibilityAPI():
    """
     Class getting the information from Convext Aware about the accessibility of facilities
     for people with physical disabilities.
     """

    def __init__(self):
        self.city = "trento"
        self.file_name = "accessibility_" + self.city + ".csv"

    def save_acc_file(self, path: str, city: str):
        """
        Open the files, clean them from wrongly encoded rows and save them locally.
        """
        self.city = city
        with open(path, "r", encoding="utf-8") as f:
            with open(self.file_name, "w", encoding="utf-8") as c:
                data = csv.reader(f, delimiter=";")
                my_writer = csv.writer(c, delimiter=";")
                not_save = ["ufficio", "unita'"]
                l = 250 # length of the rows
                if self.city == "trento":
                    l = 372
                for d in data:
                    if len(d) == l:
                        include = True
                        for word in d[0].split():
                            if word.lower() in not_save:
                                include = False
                                break
                        if include:
                            my_writer.writerow(d)

    def parse_acc_file(self):
        """
        Parse the information contained in the csv files
        and deleted specific columns, savinig them as separate files.
        """
        data = pd.read_csv(self.file_name, sep=";", engine='python')
        data.drop(labels=[x for x in data.columns if "NOTE" in x or "PM" in x or "AM" in x], axis=1, inplace=True)
        data.dropna(axis=1, inplace=True, thresh=20)
        if data['ID'].isnull().sum():  # check wheter some id's are missing
            data.dropna(axis=0, inplace=True, thresh=5)
        res = ["ID"] + [x for x in data.columns if "DESCRIZIONE" in x or "VALORE" in x]
        data[res].to_csv("Variables_acc_" + self.city + ".csv", sep = ",")
        data.drop(labels=res[1:], axis=1, inplace=True)
        data.to_csv("acc_" + self.city + "_parsed.csv", sep=",")
