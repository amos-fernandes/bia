import requests

from binance.client import Client


api_key="At0R6ebAME5rvFAFv2vfdniyamxdjIN3ouw9NcVU0jBuejrMRlpt2070wKwNGOil"
api_secret="KwXApzKS3L0pbmrjT93CuDPgQ63pOrKi49TfSnU9eCBrrFkfi07362PF8Ryx7rF3"

client = Client(api_key, api_secret)

# Get user account information
info = client.get_account()
print(info)

# Get user ID
user_id = info['uid']
print(f"User ID: {user_id}")

# Get account balance
balances = client.get_asset_balance(asset='USDT')
print("Saldo USDT:", balances)



