import glob
import pandas as pd
from datetime import datetime

type_dict = {
            0.0: 'cloud to ground(-ve)',
            1.0: 'cloud to ground (+ve)',
            2.0: 'cloud to cloud'
        }

def dataframe_to_csv(df, filename, index=False):
    """
    Save a pandas dataframe to csv
    """
    geo_coor = []
    geo_types = []
    amp = []
    created = []
    observed = []
    sensors = []
    strokes = []
    types = []
    for i in range(len(df)):
        geo_coor.append(df['geometry'][i]['coordinates'])
        geo_types.append(df['geometry'][i]['type'])
        amp.append(df['properties'][i]['amp'])
        created.append(df['properties'][i]['created'])
        observed.append(df['properties'][i]['observed'])
        sensors.append(df['properties'][i]['sensors'])
        strokes.append(df['properties'][i]['strokes'])
        types.append(df['properties'][i]['type'])
    final_df = pd.DataFrame(geo_coor, columns=['lat', 'long'])
    final_df['Geometry_types'] = geo_types
    final_df['id'] = df['id']
    final_df['type'] = df['type']
    final_df['amp'] = amp
    final_df['created'] = created
    final_df['observed'] = observed
    final_df['sensors'] = sensors
    final_df['strokes'] = strokes
    final_df['lightning_type'] = types
    typ = final_df['lightning_type'].map(type_dict)
    final_df['lightning_type'] = typ
    final_df.to_csv(filename +'.csv', index=index, encoding='utf-8-sig', header=False)
    return final_df


def multiple_txt_to_txt(path):
    """
    Convert multiple txt files to a single txt file
    """
    read_files = [i for i in path.glob('*.txt')]
    with open(str(path) + '/all.txt', 'w') as outfile:
        for f in read_files:
            with open(f) as infile:
                outfile.write(infile.read())
