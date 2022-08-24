import json
import requests

def stacks_balance(node_address):
    try:
        response = requests.get(f"https://stacks-node-api.mainnet.stacks.co/extended/v1/address/{node_address}/stx")
        data = json.loads(response.text)
        stacks_balance = float(data['balance']) * 0.000001  #Returns total number of STX tokens in wallet
        return stacks_balance
    except:
        return "None"
