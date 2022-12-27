import requests
import pprint

# asset: BTC, gemini_price: 16852.54, ascendex_price: 16856.29, difference: 0.02225
price_list = []

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
    if price:
        return float(price)
    return price

# calculate difference in %
def get_difference(price_asset_one, price_asset_two):
    # initial value bigger one
    # difference / initial value * 100  
    if price_asset_one > price_asset_two:
        greater_value = price_asset_one
    else:
        greater_value = price_asset_two

    # return absolute value i.e. positive value
    difference = abs(price_asset_one - price_asset_two)
    percent_difference = (difference / greater_value) * 100

    return percent_difference

def get_price_list():
    for item in non_stablecoins:
        gemini_price = get_price(item, "gemini")
        ascendex_price = get_price(item, "ascendex")
        
        if gemini_price and ascendex_price:
            temp_dict = {
                "asset": item,
                "price_gemini": gemini_price,
                "price_ascendex": ascendex_price,
                "difference": get_difference(gemini_price, ascendex_price)
            }
            price_list.append(temp_dict)
        pass

    return price_list

print(get_price_list())

#print(f"btc_gemini: {btc_gemini}, btc_ascendex: {btc_ascendex}, difference %: {get_difference(btc_ascendex, btc_gemini)}")

#sample output: btc_gemini: 16852.54, btc_ascendex: 16856.29, difference %: 0.022246888253583674

#print(get_difference(100,6))

#for nsc in non_stablecoins:
#    print(get_price(nsc, "ascendex"))

# print(get_price("BTC", "gemini"))
# print(get_price("BTC", "ascendex"))

