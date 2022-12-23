import requests
import pprint

# Whitelisted non-stablecoins
non_stablecoins = [
    "BTC", "ETH", "FTM", "AVAX", "MATIC",
    "BNB", "ATOM", "XRP", "DOGE", "ADA",
    "DOT", "TRX", "SOL", "LINK", "UNI"
]

# exchange: ascendex
def get_price_ascendex(asset):

    url = "https://ascendex.com/api/pro/v1/spot/ticker"
    params = {
        "symbol": f"{asset}/USDT"
    } 
    headers = {
        "Accepts": "application/json"
    }

    response = requests.get(url, params=params, headers=headers)

    return (response.json().get("data", {}).get("bid", {})[0])

# exchange gemini
def get_price_gemini(asset):

    url = f"https://api.gemini.com/v1/pubticker/{asset.lower()}usd"
    headers = {
        "Accepts": "application/json"
    } 

    response = requests.get(url, headers) 

    return (response.json().get("ask", {}))

# exhange to function mappings
cexs = {
    "ascendex": get_price_ascendex,
    "gemini": get_price_gemini
}

# return prices for given asset in given exchange
def get_price(asset, exchange):     
    price = cexs[exchange](asset)
    return float(price)

# calculate difference in %
def get_difference(price_asset_one, price_asset_two):
    # initial value bigger one
    # difference / initial value * 100  
    pass

#for nsc in non_stablecoins:
#    print(get_price(nsc, "ascendex"))

print(get_price("BTC", "gemini"))
print(get_price("BTC", "ascendex"))

