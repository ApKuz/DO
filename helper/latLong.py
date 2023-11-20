import pandas as pd
import numpy as np
import utm

def extractLatLong(df: pd.DataFrame) -> pd.DataFrame:
    """converts values in the transforms column to create a new 'lat' and 'lon' column
    to represent latitude and longitude respectivley

    Args:
        df (pd.DataFrame): df with a transforms column

    Returns:
        pd.DataFrame: df with new lat and long column
    """
    
    # Creating two new columns for lattitude and longitude
    df['lat'] = np.nan
    df['lon'] = np.nan

    for index, row in df.iterrows():
        
        # extract easting and northing from transforms field
        easting = df['transforms'][index][0]['transform']['translation']['x']
        northing = df['transforms'][index][0]['transform']['translation']['y']
        
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
    
    return df