from web3 import Web3
import json
import os

# Load environment variables (never hardcode your private key!)
from dotenv import load_dotenv
load_dotenv()

# Connect to blockchain (Infura, Alchemy, or other RPC)
RPC_URL = os.getenv("RPC_URL")  # e.g. "https://polygon-mainnet.infura.io/v3/YOUR_PROJECT_ID"
PRIVATE_KEY = os.getenv("PRIVATE_KEY")  # your wallet private key (KEEP SAFE!)
PUBLIC_ADDRESS = os.getenv("PUBLIC_ADDRESS")  # your wallet public address

w3 = Web3(Web3.HTTPProvider(RPC_URL))

# USDC or USDT ERC20 contract address (Polygon example: USDC)
TOKEN_ADDRESS = Web3.to_checksum_address("0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174")  

# Minimal ERC20 ABI
ERC20_ABI = json.loads('[{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[{"name":"","type":"bool"}],"type":"function"}]')

token_contract = w3.eth.contract(address=TOKEN_ADDRESS, abi=ERC20_ABI)

# Example payout function
def send_payout(recipient, amount, decimals=6):
    """
    Sends payout to a recipient.
    amount: human-readable (e.g. 10 for 10 USDC)
    """
    nonce = w3.eth.get_transaction_count(PUBLIC_ADDRESS)
    txn = token_contract.functions.transfer(
        Web3.to_checksum_address(recipient),
        int(amount * (10**decimals))  # convert to smallest unit
    ).build_transaction({
        'from': PUBLIC_ADDRESS,
        'nonce': nonce,
        'gas': 100000,
        'gasPrice': w3.to_wei('50', 'gwei')
    })

    signed_txn = w3.eth.account.sign_transaction(txn, private_key=PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    return w3.to_hex(tx_hash)

# Example usage
if __name__ == "__main__":
    recipient_address = "0xRecipientWalletHere"
    tx_hash = send_payout(recipient_address, 5)  # send 5 USDC
    print(f"Payout sent! Transaction hash: {tx_hash}")
