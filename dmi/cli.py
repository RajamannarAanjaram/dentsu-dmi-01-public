import click
import os
import json
import pandas as pd
from pathlib import Path
import requests


@click.group()
def dmi():
    """Command line interface for DMI API"""


@dmi.group()
def lightning():
    """Access to lightning data"""


@lightning.command()
@click.argument("DATE_BEGIN")
@click.argument("DATE_END")
@click.option("--output", "-o", default=Path(str(os.getcwd()) + '/output/lightning_observation.csv'),
              help="Path to output file; default: write to stdout")
@click.option("--api-key", "-k",
              default=lambda: os.environ.get("DMI_API_KEY"),
              help="API key; default: read from DMI_API_KEY env var")
def download(output, api_key, date_begin, date_end):
    type_dict = {
        0.0: 'cloud to ground(-ve)',
        1.0: 'cloud to ground (+ve)',
        2.0: 'cloud to cloud'
    }
    if not api_key:
        click.get_current_context().fail("No API key specified")
    else:
        start_date = date_begin+'T00:01:12-00:00'
        end_date = date_end+'T23:59:12-00:00'
        base_url = "https://dmigw.govcloud.dk/v2/lightningdata/collections/observation/items?datetime={}/{}&api-key={}".format(
            start_date, end_date, api_key)
        response = requests.get(base_url).content
        my_json = response.decode('UTF-8')
        data = json.loads(my_json)
        df = pd.DataFrame(data['features'])
        geo_coor = []
        created = []
        observed = []
        types = []
        for i in range(len(df)):
            geo_coor.append(df['geometry'][i]['coordinates'])
            created.append(df['properties'][i]['created'])
            observed.append(df['properties'][i]['observed'])
            types.append(df['properties'][i]['type'])
        final_df = pd.DataFrame(geo_coor, columns=['lat', 'long'])
        final_df['created'] = created
        final_df['observed'] = observed
        final_df['lightning_type'] = types
        typ = final_df['lightning_type'].map(type_dict)
        final_df['lightning_type'] = typ
        final_df.to_csv(output, index=False,
                        encoding='utf-8-sig', header=False)
    return final_df
