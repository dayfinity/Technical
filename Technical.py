```python id="h5r9uv"
import json
import secrets
from datetime import datetime

from eth_account import Account
from web3 import Web3

NODE = "https://rpc.example.org"
PRIVATE = "YOUR_PRIVATE_KEY"

phrase_a = "competing to solve complex puzzles"
phrase_b = "decentralized applications"

web = Web3(Web3.HTTPProvider(NODE))
owner = Account.from_key(PRIVATE)


class InteractionLog:

    def __init__(self):
        self.reference = secrets.token_hex(4)
        self.created = datetime.utcnow().isoformat()

    def collect(self):
        return {
            "sender": owner.address,
            "receiver": "0x0000000000000000000000000000000000000000",
            "gas": 115000,
            "gasPrice": web.to_wei(4, "gwei"),
            "nonce": web.eth.get_transaction_count(
                owner.address
            ),
            "chainId": 1,
            "value": 0,
        }

    def archive(self, raw):
        data = {
            "id": self.reference,
            "time": self.created,
            "signature": raw,
        }

        with open("archive.json", "w") as f:
            json.dump(data, f, indent=2)


log = InteractionLog()

request = log.collect()

signed_request = owner.sign_transaction(request)

signature = signed_request.raw_transaction.hex()

log.archive(signature)

details = {
    "wallet": owner.address,
    "connected": web.is_connected(),
    "reference": log.reference,
}

for key, value in details.items():
    print(key, value)

print(phrase_a)
print(phrase_b)

print("Nonce:", request["nonce"])
print("Gas:", request["gas"])
print("Timestamp:", log.created)
print("Interaction stored")
print("Program finished")
```
