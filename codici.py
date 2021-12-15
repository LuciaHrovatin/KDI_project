import pandas as pd


fac = pd.read_csv("facility_final.csv")

fac.drop(["Unnamed: 0.1", "information"], axis = 1, inplace=True)
fac.rename(columns={"has_location": "has_osmID"}, inplace=True)

loc = pd.read_csv("location_final.csv")

loc.drop(["Unnamed: 0.1", "Unnamed: 0.1.1", "osm_ID"], axis = 1, inplace = True)

loc.to_csv("locations.csv")
fac.to_csv("facilities.csv")