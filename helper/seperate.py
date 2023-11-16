import pandas as pd

def dfByTopic(df : pd.DataFrame) -> dict:
    """Splits a drive route dataframe by topic, deleting all columns that are nan for each topic

    Args:
        df (pd.DataFrame): DriveOhio json converted to a dataframe

    Returns:
        dict: dict of all topic dataframes accessed via the following keys:\n
            df0 : "/tf"\n
            df1 : "/apollo/localization/pose"\n
            df2 : "/apollo/sensor/gnss/corrected_imu"\n
            df3 : "/apollo/localization/msf_status"\n
            df4 : "/apollo/sensor/gnss/raw_data"\n
            df5 : "/apollo/sensor/gnss/odometry"\n
            df6 : "/apollo/perception/traffic_light"\n
            df7 : "/apollo/control"\n
            df8 : "/apollo/sensor/gnss/ins_stat"\n
            df9 : "/apollo/routing_response"\n
            df10 : "/apollo/routing_response_history"\n
            df11 : "/tf_static"\n
            df12 : "/apollo/sensor/gnss/best_pose"\n
            df13 : "/apollo/sensor/gnss/gnss_status"\n
            df14 : "/apollo/sensor/gnss/ins_status"\n
            df15 : "/apollo/canbus/chassis"\n
            df16 : "/apollo/canbus/chassis_detail"\n
            df17 : "/apollo/monitor"\n
            df18 : "/apollo/common/latency_records"\n
            df19 : "/apollo/routing_request"\n
            df20 : "/apollo/monitor/system_status"\n
            df21 : "/apollo/hmi/status"\n
            df22 : "/apollo/common/latency_reports"\n
            df23 : "/apollo/control/pad"\n
    """
    
    topicDF = {}
    
    for x in zip(df['topic'].unique(),[i for i in range(df['topic'].unique().size)]):
        # key names and related subsetted dataframe
        # print(f'df{x[1]} : "{x[0]}"')
        
        # updating dictionary to include key and subset
        
        key = 'df' + str(x[1])
        value = df[df['topic'] == x[0]]
        
        # drop all np.nan columns
        value.dropna(how='all', axis=1, inplace=True)
        
        # add unique topic df into topicDF
        topicDF.update({key: value})
        
    return topicDF
        