import pandas as pd

class TransformHelper:
    def transfrom_data(self, api, *args, **kwargs) -> pd.DataFrame:
        ids = args
        api_data = [api(**kwargs, id).get_data_frames()[0] for id in ids]
        return pd.concat(api_data)
    