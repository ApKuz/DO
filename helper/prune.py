import pandas as pd


def pruneCols(dict: dict, colsTBD: list) -> dict:
    """Prunes the column names in a provided list, iff it exists in any dictionary entry.
       Note, the first df will only delete the topic and size column

    Args:
        dict (dict): Dictioinary of pd.Dataframes of drive ohio data split by topic
        colsTBD (list): list of column names to be deleted

    Returns:
        dict: returns the dictionary of dataframes with provided columns removed, if they were there
    """
    
    
    # remove these columns as the
    for value in dict:
        dict.update({value: dict[value].reset_index()})
        
        # only these columns will be deleted in 'df0' of the dict
        delete = ['topic', 'size']
        
        if value != 'df0':
            delete = colsTBD
        
        for field in delete:
            
            try:
                tempDF = dict[value].drop(columns=[field])
            except KeyError:
                continue
            else:
                dict.update({value: tempDF})
        

        dict.update({value: dict[value].sort_values(by=['timeStamp'])})
        
    return dict