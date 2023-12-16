#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author  : 
# @Time    : 2023/12/16 09:29
# @File    : minter.py
# @annotation    :
import getopt
import logging
import sys
from datetime import datetime

from eth_account import Account
from web3 import Web3

logging.getLogger().setLevel(logging.INFO)
logging.basicConfig(format='%(message)s')


class InscriptionMinter:
    def __init__(self, mint_hex, rpc_url, private_key):
        self.private_key = private_key
        self.rpc_url = rpc_url
        self.mint_hex = mint_hex
        self.w3 = Web3(Web3.HTTPProvider(self.rpc_url))
        self.account = Account.from_key(self.private_key)
        logging.info("{:-^50s}".format("Minter initializing"))
        try:
            mint_text = self.w3.to_text(self.mint_hex)
            logging.info(f"Account Address: {self.account.address}\n"
                         f"Mint Hex: {self.mint_hex}\n"
                         f"Mint Plain Text: {mint_text}\n"
                         f"RPC URL: {self.rpc_url}")
        except Exception:
            logging.error("Failed to decode mint hex, please make sure input right")
            sys.exit()

    def batch_mint(self, times):
        count = 0
        nonce = self.w3.eth.get_transaction_count(self.account.address)
        while count < times:
            chainNonce = self.w3.eth.get_transaction_count(self.account.address)
            tx = {
                'nonce': nonce if nonce >= chainNonce else chainNonce,
                'to': self.account.address,
                'gas': 0,
                'gasPrice': self.w3.eth.gas_price,
                'value': 0,
                'data': self.mint_hex,
                'chainId': self.w3.eth.chain_id
            }
            tx.update({'gas': self.w3.eth.estimate_gas(tx)})
            signed_tx = self.w3.eth.account.sign_transaction(tx, self.private_key)
            try:
                tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
                logging.info(f"Mint {str(count)} Complete at {datetime.now()} : tx hash: {self.w3.to_hex(tx_hash)}")
            except Exception as reason:
                logging.error(f"Mint {str(count)} Failed at {datetime.now()} Reason: {reason}")
            nonce += 1
            count += 1


if __name__ == "__main__":
    usage_Msg = "python3 minter.py --mint-hex YOUR_MINT_HEX(starts with 0x) --rpc-url YOUR_RPC_URL --private-key " \
                "YOUR_PRIVATE_KEY --times YOUR_MINT_TIMES\n" \
                "For example: python3 minter.py --mint-hex 0x68656c6c6f5f776f726c64 --rpc-url " \
                "https://binance.llamarpc.com --private-key " \
                "ac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80 --times 2"
    argv = sys.argv[1:]
    mint_hex = None
    rpc_url = None
    private_key = None
    times = None
    try:
        opts, args = getopt.getopt(argv, "",
                                   ["mint-hex=", "rpc-url=", "private-key=", "times="])
        for opt, arg in opts:
            if opt == '--mint-hex':
                mint_hex = arg
            elif opt == '--rpc-url':
                rpc_url = arg
            elif opt == '--private-key':
                private_key = arg
            elif opt == '--times':
                times = int(arg)
        if not any([mint_hex, rpc_url, private_key, times]):
            logging.error(f"Missing some parameters! Please check input. Usage: \n{usage_Msg}")
            sys.exit()
        minter = InscriptionMinter(mint_hex, rpc_url, private_key)
        logging.info(f"Mint Times: {str(times)}")
        answer = input(
            "Please carefully confirm the information above and input y/yes to continue, n/no to abort[y/n]:")
        if answer.lower() in ["y", "yes"]:
            minter.batch_mint(times)
        elif answer.lower() in ["n", "no"]:
            sys.exit()
        else:
            logging.error("Input Error, Exit")
            sys.exit()
    except Exception as e:
        logging.error(e)
