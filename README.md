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
