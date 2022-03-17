import json
from multiprocessing import Pool
import requests
import json
import pandas as pd
from datetime import datetime, timedelta

from db.crud import create_posts


def get_details_from_data(token):
    ss = (datetime.now() - timedelta(minutes=5)).timestamp()*1000000
    timee = str(int(ss))
    token = token["data"].get("token")
#     print(token)
    url = "https://api.divar.ir/v5/posts/"+token

    # payload="""{\"json_schema\":{\"category\":{\"value\":\"ROOT\"}},\"last-post-date\":{}}""".format(timee)
    # payload=json.dumps({"json_schema":{"category":{"value":"ROOT"}},"last-post-date":1644677364155524})
    headers = {
        'Content-Type': 'text/plain',
        'Cookie': 'did=ec3de232-193d-4d29-8d19-5c210cd0e20d; ga=GA1.2.958343835.1628941508; _gcl_au=1.1.1710749390.1637677108; multi-city=isfahan|; city=isfahan; _gid=GA1.2.958373558.1644561048; _gat_UA-32884252-2=1'
    }

    response = requests.request("GET", url, headers=headers)

    data_get = response.json()
    data = data_get.get('data')
    widgets = data_get.get('widgets')
    ss = []
    pure_data = {
        # "description":data.get("description"),
        # "business_type":data.get("business_data")["business_type"],
        # "price":data.get("webengage")["price"],
        # "brand_model":data.get("webengage")["brand_model"],
        # "city":data.get("webengage")["city"],
        # "token":data.get("webengage")["token"],
        # "title":widgets.get("header")["title"],
        #   "date":widgets.get("header")["date"],
        # "list_data":widgets.get("list_data"),
        # "web_images":widgets.get("web_images"),
        "category": data.get("category")['title'],
        "title": data.get("share"),
        "url": data.get("url"),
        "district": data.get("district"),
        "description": data.get("description"),
        "business_type": data.get("business_data")["business_type"],
        "price": data.get("webengage")["price"],
        "brand_model": data.get("webengage")["brand_model"],
        "token": data.get("webengage")["token"],
        "title": widgets.get("header")["title"],
        "date": widgets.get("header")["date"],
        "list_data": widgets.get("list_data"),
        "web_images": widgets.get("web_images"),
        

    }
    ss.append(pure_data)
    return pure_data


def get_data_from_divar():
    ss = (datetime.now() - timedelta(minutes=5)).timestamp()*1000000
    timee = int(ss)
    print(timee)
    url = "https://api.divar.ir/v8/search/4/ROOT"
    # url = "https://api.divar.ir/v8/search/4/Root"
    lst_token = []
    results = []
    for item in range(5):
        payload = json.dumps(
            {"json_schema": {"category": {"value": "ROOT"}}, "last-post-date": timee})
        headers = {
            'Content-Type': 'text/plain',
            'Cookie': 'did=ec3de232-193d-4d29-8d19-5c210cd0e20d; ga=GA1.2.958343835.1628941508; _gcl_au=1.1.1710749390.1637677108; multi-city=isfahan|; city=isfahan; _gid=GA1.2.958373558.1644561048; _gat_UA-32884252-2=1'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        res = response.json()
        # print(response.json().get('widget_list')[0])
        lst_data = res.get('widget_list')
        # print(response.json().get('widget_list')[0]['data'].get('token'))

        print(timee)
        timee = res['last_post_date']

        pool = Pool(processes=1)
        results = results+pool.map(get_details_from_data, lst_data)
        pool.close()
        pool.join()
        lst_token.append(results)

    df = pd.DataFrame(results)
    filter_response = df[df['description'].str.contains('مالی | مهاجر')]
    ss = []
    for index, item in filter_response.iterrows():
        # print('system',item)
        ss.append(item)

    return ss
