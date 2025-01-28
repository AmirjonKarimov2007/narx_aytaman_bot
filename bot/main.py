import json
import requests
from requests.auth import HTTPBasicAuth
def get_info_for_product():
    url = "https://smartup.online/b/anor/mxsx/mr/inventory$export"

    auth = HTTPBasicAuth('jamshidbek@falcon', '571++632')

    headers = {
        'filial_id': '5012602',
        'project_id': 'trade',
        'Content-Type': 'application/json'
    }

    data = {
        "code": "",
        "begin_created_on": "",
        "end_created_on": "",
        "begin_modified_on": "",
        "end_modified_on": ""
    }

    response = requests.get(url, json=data, auth=auth, headers=headers)

    if response.status_code == 200:
        print("So'rov muvaffaqiyatli amalga oshirildi.")
        
        # JSON ma'lumotlarini dekodlash
        response_dict = response.json()

        # Ma'lumotlarni tartibli JSON faylga yozish va Unicode belgilarni to'g'ri ko'rsatish
        with open('data.json', 'w', encoding='utf-8') as file:
            json.dump(response_dict, file, indent=4, ensure_ascii=False)
        return True
    else:
        print(f"So'rovda xatolik: {response.status_code}")
        return False
def get_price_for_product():
    url = "https://smartup.online/b/anor/mxs/mkf/product_price$export"

    auth = HTTPBasicAuth('jamshidbek@falcon', '571++632')

    headers = {
        'filial_id': '5012602',
        'project_code': 'trade',
    }

    data = {
        
    }

    response = requests.get(url, json=data, auth=auth, headers=headers)

    if response.status_code == 200:
        print("So'rov muvaffaqiyatli amalga oshirildi.")
        response_dict = response.json()
        with open('prices.json', 'w', encoding='utf-8') as file:
            json.dump(response_dict, file, indent=4, ensure_ascii=False)
        return True
    else:
        print(f"So'rovda xatolik: {response.status_code}")
        return False

def do_all():
    info = get_info_for_product()
    price = get_price_for_product()
    if price and info:
        with open('data.json', 'r', encoding='utf-8') as data_file:
            data = json.load(data_file)

        with open('prices.json', 'r', encoding='utf-8') as prices_file:
            prices = json.load(prices_file)

        price_dict = {}
        for item in prices["inventory"]:
            price_uzs = item["price_type"][0]["price"] if len(item["price_type"]) > 0 else None
            price_usd = item["price_type"][1]["price"] if len(item["price_type"]) > 1 else None
            price_dict[item["inventory_code"]] = {
                "price_uzs": price_uzs,
                "price_usd": price_usd
            }

        for product in data["inventory"]:
            code = product["code"]  
            if code in price_dict:  
                product["price_uzs"] = price_dict[code]["price_uzs"]
                product["price_usd"] = price_dict[code]["price_usd"]
            else:
                product["price_uzs"] = None
                product["price_usd"] = None

        with open('updated_data.json', 'w', encoding='utf-8') as updated_file:
            json.dump(data, updated_file, ensure_ascii=False, indent=4)
        return True
    else:
        print("Xatolik bor.")
        return False

# do_all()