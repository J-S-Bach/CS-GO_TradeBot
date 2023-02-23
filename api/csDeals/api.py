import requests


def getLowestPrice(appid):
    payload = {"appid": appid}
    headers = {
        "content-type": "application/json"
    }
    t = requests.get("https://cs.deals/API/IPricing/GetLowestPrices/v1", headers=headers, json=payload).json()
    return t
