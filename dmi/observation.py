import requests, json
import pandas as pd
import os, io, zipfile
from dmi.utils import dataframe_to_csv,multiple_txt_to_txt
from pathlib import Path
from datetime import datetime

class DMIOpenDataClient:
    
    def __init__(self, api_key: str, version: str = "v2", api: str = "lightningdata"):
        self.base_url = "https://dmigw.govcloud.dk/{}/{}/collections".format(
            version, api)
        self.api_key = api_key
        self.version = version

    def get_observations(self,limit: int = 1000, file_name: str = "lightning_observation"):
        """
        This function returns a list of 1000 observations on lightning data.
        """
        url = self.base_url + "/observation/items?api-key={}&limit={}".format(self.api_key,limit)
        response = requests.get(url).content
        my_json = response.decode('UTF-8')
        data = json.loads(my_json)
        df = pd.DataFrame(data['features'])
        final_df = dataframe_to_csv(df, file_name)

        return final_df

class DMIBulkDataClient:
    
    def __init__(self, api_key: str, version: str = "v2", api: str = "lightningdata"):
        self.base_url = "https://dmigw.govcloud.dk/{}/{}/collections".format(
            version, api)
        self.api_key = api_key
        self.version = version

    def get_bulk_observations(self,year: int = 2020):
        """
        This function returns a list of 1000 observations on lightning data.
        """
        months = ['01', '02', '03', '04', '05',
                  '06', '07', '08', '09', '10', '11', '12']
        path = Path(os.getcwd()+"/data")
        api = self.api_key
        for month in months:
            url = f"https://dmigw.govcloud.dk/v2/lightningdata/bulk/{year}-{month}.zip?api-key={api}".format(
                year, month, api)
            response = requests.get(url)
            z = zipfile.ZipFile(io.BytesIO(response.content))
            z.extractall(path)
        multiple_txt_to_txt(path)
        dir = Path(str(path) + "/all.txt")
        with open(dir, "r") as f:
            content = f.readlines()
        data = {'features': []}
        for i in content:
            data['features'].append(eval(i.strip('\n')))
        df = pd.DataFrame(data['features'])
        final_df = dataframe_to_csv(df, "bulk_lightning_observation")

        return final_df
