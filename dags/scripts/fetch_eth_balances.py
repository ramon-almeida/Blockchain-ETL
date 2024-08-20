import requests
from airflow.models import Variable

# Retrieve the Etherscan API key from Airflow variables
etherscan_api_key = Variable.get("ETHERSCAN_API_KEY")

if not etherscan_api_key:
    raise ValueError("Please set the ETHERSCAN_API_KEY Airflow variable.")

# List of Ethereum addresses to check
addresses = [
    "0x28c6c06298d514db089934071355e5743bf21d60",
    "0x742d35Cc6634C0532925a3b844Bc454e4438f44e",
    "0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae",
    "0x0000000000000000000000000000000000000000",
    "0x0a869d79a7052c7f1b55a8ebabbea3420f0d1e13"
    # Add more addresses here
]

# Function to get balance of a single address using Etherscan


def get_balance(eth_address):
    url = f'https://api.etherscan.io/api?module=account&action=balance&address={eth_address}&tag=latest&apikey={etherscan_api_key}'
    response = requests.get(url).json()

    if response['status'] != '1':
        print(f"Full Etherscan API response: {response}")
        raise Exception(f"Etherscan API error: {response['message']}")

    balance_in_wei = int(response['result'])
    balance_in_eth = balance_in_wei / 10**18

    return balance_in_eth


# Loop through the addresses and get their balances
def fetch_balances():
    balances = {}
    for eth_address in addresses:
        balance_in_eth = get_balance(eth_address)
        balances[eth_address] = balance_in_eth
    return balances
