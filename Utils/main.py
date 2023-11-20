# This currently plots the field in line 45 ish, currently works with fields that are excusvley some number type data


import plotly.express as px
import pandas as pd
import numpy as np
import utm
import sys

sys.path.append("../DO")
import helper


def main():
    
    with open('Data/blueroute1export.json') as f:
        _df = pd.read_json(f)
    
    df = _df
    
    # see '../helper/time.py'
    df = helper.timeField_to_timeStamp(df)

    # split df by topic, see '../helper/seperate.py' library
    dict = helper.dfByTopic(df)

    # see '../helper/prune.py'
    dict = helper.pruneCols(dict, ['index', 'timeField', 'topic', 'size', 'msg_type', 'metadataID', '_id', 'header', 'transforms'])
        
        
    # merging on timestamp
    for value in dict:
        
        if value == 'df0':
            mergedDF = dict[value]
            
        else:
            mergedDF = pd.merge_asof(mergedDF, dict[value], on=['timeStamp'])
            
    # sorting on timestamp
    mergedDF['timeStamp'] = mergedDF['timeStamp'].sort_values()

    # fieldToPlot = 'brake'
    fieldToPlot = 'speedMps'
    # fieldToPlot = 'throttle'

    df = mergedDF
    df = df.dropna(subset=[fieldToPlot])
    df = df.reset_index()
    
    # see '../helper/latLong'
    df = helper.extractLatLong(df)
    
    fig = px.scatter_mapbox(df, lat='lat', lon='lon', color=fieldToPlot)
    fig.update_layout(mapbox_style="open-street-map")
    fig.show()

if __name__ == '__main__':
    main()