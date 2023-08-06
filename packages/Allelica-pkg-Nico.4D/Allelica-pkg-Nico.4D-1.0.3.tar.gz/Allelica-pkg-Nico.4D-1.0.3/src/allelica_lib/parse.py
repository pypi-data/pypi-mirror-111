import pandas as pd
import dask.dataframe as dd

def process(path, outpath):

    """
    Read the csv From "path" and 
    Process it and Save it Into $outpath
    Without Dask.

    """

    df = pd.read_excel(path)
    gb = df.groupby(['Run #','Sample ID'])['Array Position'].agg([lambda x: ','.join(map(str, x))])
    res = gb.reset_index()

    res.columns = ['Run #','Sample ID', 'Array Position']
    res.to_csv(outpath,sep='\t', index=False)

def process_dask(path, outpath, partitions):

    """
    Read the csv From "path" and 
    Process it and Save it Into $outpath
    Using Dask.

    Must Add the Numbers of Partitions.

    """

    df = pd.read_excel(path)
    ddf = dd.from_pandas(df, npartitions=partitions)
    out = ddf.groupby(['Run #','Sample ID'])['Array Position'].apply(lambda x: ','.join(map(str, x)), meta=pd.Series(dtype='str', name='Array Position'))
    out = out.compute()
    
    out = out.to_frame().reset_index()
    out.to_csv(outpath,sep='\t', index=False)