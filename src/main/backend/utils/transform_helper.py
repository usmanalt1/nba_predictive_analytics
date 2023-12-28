import pandas as pd
import time as t

class TransformHelper:
    def transfrom_data(self, api, *args, **kwargs) -> pd.DataFrame:
        ids = args[0]
        tran_empty_array = []
        for id in ids:
            t.sleep(1)
            df = api(id, **kwargs).get_data_frames()[0]  
            print(df)
            tran_empty_array.append(df)

        return pd.concat(tran_empty_array)
    