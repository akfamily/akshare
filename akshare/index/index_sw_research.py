import pandas as pd
import requests
import math
from tqdm import tqdm


def index_realtime_sw(symbol: str = "二级行业"):
    url = "https://www.swhyresearch.com/institute-sw/api/index_publish/current/"
    params = {
        'page': '1',
        'page_size': '50',
        'indextype': symbol
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    total_num = data_json['data']['count']
    total_page = math.ceil(total_num / 50)
    big_df = pd.DataFrame()
    for page in tqdm(range(1, total_page+1), leave=False):
        params.update({
            "page": page
        })
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json['data']['results'])
        big_df = pd.concat([big_df, temp_df], ignore_index=True)

    return big_df


if __name__ == '__main__':
    index_realtime_sw_df = index_realtime_sw(symbol="风格指数")
    print(index_realtime_sw_df)
