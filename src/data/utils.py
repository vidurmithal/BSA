def baseline(df, agg='count', date_col='ACQ_DATE', year=2020):
    '''Separate baseline and current year based from DataFrame.
    '''
    import pandas as pd
    import numpy as np

    current = df[df[date_col].dt.year == year]
    baseline= df[df[date_col].dt.year <  year]
    
    if agg=='count':    
        current = current.groupby(current[date_col].dt.dayofyear).count()
        baseline= baseline.groupby(baseline[date_col].dt.dayofyear).count() / len(set(baseline[date_col].dt.year))
    
    elif agg=='mean':
        current = current.groupby(current[date_col].dt.dayofyear).agg(np.nanmean)
        baseline= baseline.groupby(baseline[date_col].dt.dayofyear).agg(np.nanmean)
            
    current.index = pd.to_datetime('%s-01-01'%year) + pd.to_timedelta(current.index, 'D')
    baseline.index = pd.to_datetime('%s-01-01'%year) + pd.to_timedelta(baseline.index, 'D')
    
    current.columns = pd.MultiIndex.from_product([['current'], current.columns.tolist()])
    baseline.columns = pd.MultiIndex.from_product([['baseline'], baseline.columns.tolist()])
    
    df = pd.DataFrame(index=pd.date_range('%s-01-01'%year, '%s-12-31'%year, ))
    
    df = df.join(current.iloc[:,:]).join(baseline.iloc[:,:])
    df.columns = pd.MultiIndex.from_tuples(df.columns.tolist())
    
    return df