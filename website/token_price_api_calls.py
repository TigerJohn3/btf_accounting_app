import json
import requests

def asset_usd_price(token_type, token_amount):
    token_amount = float(token_amount)
    price = token_call(token_type)
    usd_asset_price = '{:.2f}'.format(price*token_amount)
    return usd_asset_price


def token_call(token_name):
    print(token_name)
    response = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={token_name}&vs_currencies=usd")
    print(response)
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
