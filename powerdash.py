from io import StringIO
import requests
import pandas as pd
import config


def get_data(start, end, dgm="x-pml:/diagrams/ud/41cooper.dgm", variables=None):
    payload = {'start': start, 'end': end, 'dgm': dgm, 'variables': variables, 'format': 'csv'}
    data = requests.get(url=config.powerdash_base_url + "/range", params=payload)
    csv_data = StringIO(data.text)
    csv = pd.read_csv(csv_data)
    return csv


if __name__ == "__main__":
    data = get_data(start=1475294400000, end=1477972800000)
    print(data)
