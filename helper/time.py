import pandas as pd

def timeField_to_timeStamp(df: pd.DataFrame) -> pd.DataFrame:
    """Converts timeField column from DO data to a pd.timeStamp type in the first column

    Args:
        df (pd.DataFrame): DO json file to pandas DataFrame

    Returns:
        pd.DataFrame: DataFrame with pandas timeStamp type in the first column
    """
    
    # Create a new timeStamp column that is the '$date' entry in 'timeField'
    df['timeStamp'] = df['timeField'].apply(lambda x: x['$date'])

    # remove 'timeStamp' column and move it to the first column
    firstColumn = df.pop('timeStamp')
    df.insert(0, 'timeStamp', firstColumn)

    # convert 'timeStamp' column to pandas timestamp
    df['timeStamp'] = pd.to_datetime(df['timeStamp'])
    
    return df