import numpy as np  
from datetime import datetime

# split df by no volume value (volume == 0)
def zsplit_by_nv(df, drop_under=300):
    
    dfv0 = df[df['volume'] == 0]
    v0days = []
    prev_d = datetime(1900,12,1)
    start_dt = None
    start_idx = None
    for index, row in dfv0.iterrows():
        d = datetime.strptime(row['date'], '%Y%m%d')
        if start_dt == None:
            start_dt = d
            start_idx = index
            end_dt = d
            end_idx = index
            prev_d = d
            prev_idx = index
        else:
            if (d - prev_d).days > 10:
                end_dt = prev_d
                end_idx = prev_idx
                v0days.append([start_dt, end_dt, start_idx, end_idx])
                start_dt = d
                start_idx = index
            end_dt = d
            prev_d = d
            prev_idx = index
        
                
    if start_dt is not None:
        v0days.append([start_dt, end_dt, start_idx, prev_idx])

    from_idx = None
    to_idx = None
    nv0_ranges = []
    for didx in v0days:
        if from_idx is None:
            nv0_ranges.append([-np.inf, didx[2]])
            from_idx = didx[3]
        else:
            to_idx = didx[2]
            nv0_ranges.append([from_idx, to_idx])
            from_idx = didx[3]
            to_idx = np.inf
    nv0_ranges.append([from_idx, to_idx])

    result = []
    for vrange in nv0_ranges:
        if abs(vrange[0] - vrange[1]) > drop_under:
            result.append(vrange)

    return result

def split_by_nv(df, drop_under=300):
    v0_days = []
    start_dt = None
    start_idx = None
    prev_d = datetime(1900, 12, 1)
    
    for index, row in df[df['volume'] == 0].iterrows():
        d = datetime.strptime(row['date'], '%Y%m%d')
        if start_dt is None:
            start_dt = d
            start_idx = index
        elif (d - prev_d).days > 10:
            v0_days.append([start_dt, prev_d, start_idx, index - 1])
            start_dt = d
            start_idx = index
        prev_d = d
    
    if start_dt is not None:
        v0_days.append([start_dt, prev_d, start_idx, df.index[-1]])
    
    nv0_ranges = [[-np.inf, v0_days[0][2]]]
    for i in range(len(v0_days) - 1):
        nv0_ranges.append([v0_days[i][3], v0_days[i + 1][2]])
    nv0_ranges.append([v0_days[-1][3], np.inf])
    
    result = [vrange for vrange in nv0_ranges if abs(vrange[0] - vrange[1]) > drop_under]
    
    return result

def test():
    print('test')