import pandas as pd 
from geopy.geocoders import Nominatim

acc = pd.read_csv("accessibility.csv")
pl = pd.read_csv("facility_data.csv")

geolocator = Nominatim(user_agent="Chrome/86.0.4240.75")


pdf = pd.merge(acc, pl, how = "inner", on = ["has_latitude", "has_longitude"])
print(pdf.shape)

