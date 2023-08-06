import pandas as pd
import numpy as np

def RollingGroupCorrelation(df, window):
    """
    This function calculates the mean rolling window multi correlation
    between all columns of a Pandas DataFrame.
    
    Inputs:
    * A DataFrame (pd.Dataframe)
    * A window length (int)
    
    Outputs:
    * A Series (pd.Series)
    
    """

    # declare lists
    done = []
    correlations = []

    # loop thru all column pairs
    for column1 in df.columns:
        done.append(column1)
        for column2 in df.columns:
            
            # make sure that we only calculate the correlation
            # between unique columns pairs
            if column2 in done:
                continue
                
            # calculate the rolling correlation between two columns
            rolling_corr = df[column1].rolling(window).corr(df[column2].rolling(window))
            
            # save the result
            correlations.append(rolling_corr)

    # calculate the rolling mean of multiple correlations
    mean_multi_correlation = pd.DataFrame(correlations).mean()

    # drop non-finite values
    mean_multi_correlation = mean_multi_correlation[np.isfinite(mean_multi_correlation)]
    
    return mean_multi_correlation

