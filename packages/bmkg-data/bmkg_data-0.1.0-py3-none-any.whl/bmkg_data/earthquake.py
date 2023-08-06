import requests
import json
import pandas

BASE_URL = 'https://data.bmkg.go.id/DataMKG/TEWS/'
URL_FELT = BASE_URL + 'gempadirasakan.json'
URL_SIG = BASE_URL + 'gempaterkini.json'
URL_LATEST = BASE_URL + 'autogempa.json'

def __convert_to_dataframe(list_of_dict):
    df = pandas.DataFrame(list_of_dict)
    df.DateTime = df.DateTime.astype('datetime64[ms]')
    df.set_index('DateTime', inplace = True)

    return df

def get_felt_earthquakes():
    """
    Returns last 15 events of felt earthquake

    Returns
    -------
    Earthquake Table (pandas.DataFrame)
    """
    req = requests.get(URL_FELT)
    assert(req.status_code == 200)
    earthquakes = json.loads(req.text)['Infogempa']['gempa']

    return __convert_to_dataframe(earthquakes)

def get_significant_earthquakes():
    """
    Returns last 15 events of (M > 5.0) earthquake

    Returns
    -------
    Earthquake Table (pandas.DataFrame)
    """
    req = requests.get(URL_SIG)
    assert(req.status_code == 200)
    earthquakes = json.loads(req.text)['Infogempa']['gempa']

    return __convert_to_dataframe(earthquakes)

def get_latest_earthquake():
    """
    Return last event of earthquake

    Returns
    -------
    Earthquake Table (pandas.DataFrame)
    """
    req = requests.get(URL_LATEST)
    assert(req.status_code == 200)
    earthquake = json.loads(req.text)['Infogempa']['gempa']

    return __convert_to_dataframe([earthquake])
