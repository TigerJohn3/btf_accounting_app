import json
import requests

def asset_usd_price(token_type, token_amount):
    token_amount = float(token_amount)
    price = token_call(token_type)
    usd_asset_price = '{:.2f}'.format(price*token_amount)
    return usd_asset_price


def token_call(token_name):
    response = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={token_name}&vs_currencies=usd")
    data = json.loads(response.text)
    price = float(data[token_name]['usd'])
    return price


def token_call_date(token_name, date):
    response = requests.get(f"https://api.coingecko.com/api/v3/coins/{token_name}/history?date={date}")
    data = json.loads(response.text)
    price_from_date = float(data['market_data']['current_price']['usd'])
    return price_from_date


def token_display_switch(token_name):
    tokens_displayed = {
        'Bitcoin':'bitcoin',
        'Ether':'ethereum',
        'Matic': 'matic-network',
        'PYR':'vulcan-forged',
        'USDC':'usd-coin',
    }
    for token in tokens_displayed.items():
        if token_name == token[0]:
            return token[1]
        elif token_name == token[1]:
            return token[0]
    return "This token is not added to the list, contact support"




"""
# Pull bitcoin price from coingecko api
def bitcoin_usd_price():
    bitcoin_price = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd")
    bitcoin_price = json.loads(bitcoin_price.text)
    bitcoin_price = float(bitcoin_price['bitcoin']['usd'])
    return bitcoin_price

# Pull ether price from coingecko api
def eth_usd_price():
    eth_price = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd")
    eth_price = json.loads(eth_price.text)
    eth_price = float(eth_price['ethereum']['usd'])
    return eth_price

# Pull matic price from coingecko api
def matic_usd_price():
    matic_price = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=matic-network&vs_currencies=usd")
    matic_price = json.loads(matic_price.text)
    matic_price = float(matic_price['matic-network']['usd'])
    return matic_price

# Pull pyr price from coingecko api
def pyr_usd_price():
    pyr_price = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=vulcan-forged&vs_currencies=usd")
    pyr_price = json.loads(pyr_price.text)
    pyr_price = float(pyr_price['vulcan-forged']['usd'])
    return pyr_price

"""