import json
import threading
from secrets import token_bytes

from eth_account import Account
from sha3 import keccak_256
from web3 import Web3

with open("config.json") as json_config:
    config = json.load(json_config)
    infura_api = config["infura_api"]

infura_web = f"https://mainnet.infura.io/v3/{infura_api.replace('https://mainnet.infura.io/v3/', '')}"
web3 = Web3(Web3.HTTPProvider(infura_web))


def ethereum_generate():
    while True:
        private_key = keccak_256(token_bytes(32)).digest().hex()
        address = Account.from_key(private_key).address
        balance = web3.eth.get_balance(address)

        print(f"Private key: {private_key}\n"
              f"Address: {address}\n"
              f"Balance: {balance}\n"
              "--------------------------------------------------------------------------------\n")

        if balance > 0:
            with open("eth.txt", "a+") as file:
                file.write(f"Private key: {private_key}\n"
                           f"Address: {address}\n"
                           f"Balance: {balance}\n"
                           "--------------------------------------------------------------------------------\n")
                file.close()


if __name__ == '__main__':
    for _ in range(1000):
        threading.Thread(target=ethereum_generate).start()
