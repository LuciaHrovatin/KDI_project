# KDI_project
Project repository for the course in Knowledge and Data Integration, academic year 2021/2022 (University of Trento). 

## Project objective 
"A website that helps the (future) university students to find events of interest in Trento and Rovereto area.” <br>

## Prerequisites 

In order to run this project, the following tools have to be installed on your machine: 
- Python, preferably [3.8](https://www.python.org/downloads/release/python-380/) or [3.9](https://www.python.org/downloads/release/python-390/).   

## Installation 

### Clone the repository 

Clone this repository in a local directory typing in the command line: 

```
git clone https://github.com/LuciaHrovatin/KDI.git ## CAMBIA 
```

### Environment 
The creation of a virtual environment is highly suggested. If not already installed, install virtualenv # AGGIUNGI REFERENCE:

- in Unix systems:
    ```
    python3 -m pip install --user virtualenv
    ```

- in Windows systems:
    ```
    python -m pip install --user virtualenv
    ```

And then create and activate the virtual environment named *venv* typing in the command line (inside the project folder): 

- in Unix systems:
    ```
    python3 -m venv venv
    source venv
    ```

- in Windows systems:
    ```
    python -m venv venv
    venv\Scripts\activate
    ```

### Requirements 

In the active virtual environment, install all libraries contained in the `requirements.txt` file:

```
pip install -r requirements.txt
```

## OpenStreetMap data 
The json file will follow this structure: 
{
"type": "FeatureCollection", # not interesting 
"crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:OGC:1.3:CRS84" } }, # descrizione del sistema di riferimento dei punti 

"features": [ # here starts the interesting part 
{ "type": "Feature", 
  "properties": {
                  "tags": {},  # di solito è un dizionario con roba interesting dentro <br>
                  "lon": 11.033347129821777, # in degree <br>
                  "id": 262147521,# openstreetmap identifier <br>
                  "lat": 45.869724273681641, # latitude in degree<br>
                  "addr:city": null, <br>
                  "addr:country": null,<br>
                  "addr:housenumber": null, <br>
                  "addr:housename": null, <br>
                  "addr:postcode": null, <br>
                  "addr:place": null, <br>
                  "addr:street": null, <br>
                  "email": null, <br>
                  "name": null, <br>
                  "opening_hours": null, <br>
                  "operator": null, <br>
                  "phone": null, <br>
                  "website": null, <br>
                  "information": null, <br>
                  "tourism": null, <br>
"leisure": null, <br>
"outdoor_seating": null,<br>
"amenity": null, <br>
"building": "yes", # POSSIAMO USARLO COME "is closed place"<br>
"internet_access": null, <br>
"parking": null, <br>
"wikipedia": null, <br>
"building:use": null, <br>
"shop": null, <br>
"building:levels": null, <br>
"ice_cream": null, <br>
"social_facility": null, <br>
"height": null, <br>
"landuse": null, <br>
"building:material": null, <br>
"craft": null },<br>
"geometry": { "type": "Point", "coordinates": [ LONGITUDINE, LATITUDE] } },
}

--> IDEA: 
intergrare queste info con quelle date dal magico dataset sulla accessibilità
POSSIBILI cose interessanti: 
-> nome dei posti 
-> indirizzi vari 
-> wheelchair: yes, no, maybe 
-> identificazione di posti turistici sotto Tourism 




"event": {
mode: {
	"online": 
	"offline":
	"blended": 
    },
category: { classID: {id:, 
		      further info}
    }, 
cost: {
	"isfree": "bool", 
	"ticket": { onlineBooking, 
		extraBenefits, 
		total,
		price,
		currency,
		seller,
		purchaser: {IDperson, reservedSeat: {}, status}
		}
organizer: {organizationID:
		    personID:}
edition:, 
festival:, 
isSubEvent: {macroEvent: eventID} 
targetAge: string,
totalParticipants: int, 
language: [], 
date: (giorno di inizio), 
duration: timestampFine-timestampInizio 
sponsoredBy: {organizationID:
		personID:
}
description: string
memory: [eventID]
taggedBy: [organizationID or personID], 
scheduled: {coveredPeriod: timestampFine-timestampInizio, 
	    pace: string 
	    }
link: (in teoria il link del sito)
ranking: ??? -> noi del futuro :) 
transport: ??? -> noi del futuro :) 
}



category: {
ID 
info
subcategory: {
creative work:{}}

