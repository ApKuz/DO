# This currently plots the field in line 61 ish, currently works with fields that are excusvley some number type data


import plotly.express as px
import pandas as pd
import numpy as np
import utm
import sys



sys.path.append("../DO")
import helper


with open('Data/blueroute1export.json') as f:
    _df = pd.read_json(f)
    
df = _df


# Create a new timeStamp column that is the '$date' entry in 'timeField'
df['timeStamp'] = df['timeField'].apply(lambda x: x['$date'])

# remove 'timeStamp' column and move it to the first column
firstColumn = df.pop('timeStamp')
df.insert(0, 'timeStamp', firstColumn)

# convert 'timeStamp' column to pandas timestamp
df['timeStamp'] = pd.to_datetime(df['timeStamp'])


# split df by topic, see '../helper/seperate.py' library
dict = helper.dfByTopic(df)

# remove these columns as the
for value in dict:
    dict.update({value: dict[value].reset_index()})
    
    colsTBD = ['index', 'timeField', 'topic', 'size', 'msg_type', 'metadataID', '_id', 'header']
    
    if value == 'df0':
        colsTBD = ['topic', 'size']
    
    for field in ['index', 'timeField', 'topic', 'size', 'msg_type', 'metadataID', '_id', 'header']:
        
        try:
            tempDF = dict[value].drop(columns=[field])
        except KeyError:
            continue
        else:
            dict.update({value: tempDF})
    

    dict.update({value: dict[value].sort_values(by=['timeStamp'])})
    
  
# merging and sorting by timeStamp  
for value in dict:
    
    if value == 'df0':
        mergedDF = dict[value]
        
    else:
        mergedDF = pd.merge_asof(mergedDF, dict[value], on=['timeStamp'])
        
mergedDF['timeStamp'] = mergedDF['timeStamp'].sort_values()

# fieldToPlot = 'brake'
fieldToPlot = 'speedMps'

df = mergedDF
df = df.dropna(subset=[fieldToPlot])
df = df.reset_index()

# Creating two new columns for lattitude and longitude
df['lat'] = ''
df['lon'] = ''

for index, row in df.iterrows():
    
    # extract easting and northing from transforms field
    easting = df['transforms_x'][index][0]['transform']['translation']['x']
    northing = df['transforms_x'][index][0]['transform']['translation']['y']
    
    # easting must follow the below parameters
    if not (easting >= 100_000 and easting <= 1_000_000):
        continue
    
    # finding the latlong with provided UTM
    latLong = utm.to_latlon(easting, northing, 17, 'N')
    
    # setting the lat and lon values in df
    df.at[index, 'lat'] = latLong[0]
    df.at[index, 'lon'] = latLong[1]
    
# dropping na values from lat and lon (if any)    
df['lat'].replace('', np.nan, inplace=True)

df = df.dropna(subset=['lat'])
df = df.dropna(subset=['lon'])

if __name__ == '__main__':
    fig = px.scatter_mapbox(df, lat='lat', lon='lon', color=fieldToPlot)
    fig.update_layout(mapbox_style="open-street-map")
    fig.show()