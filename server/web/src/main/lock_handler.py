import os
import json
import configparser

from web3 import Web3
from web3.contract import ConciseContract
from web3.middleware import geth_poa_middleware


class ContractManager:
    def __init__(self):
        self.infura_url = 'http://geth:8545'
        self.abi_path = 'static/contract_info/abi.txt'
        self.tx_hash_path = 'static/contract_info/tx_hash.txt'

        self.abi = self.get_abi()
        self.tx_hash = self.get_tx_hash()

        self.web3_instance = self.get_web3_instance()
        self.get_contract_instance = self.get_contract_instance()

    def get_abi(self):
        try:
            with open(self.abi_path, 'r') as f:
                abi = json.load(f)
        except Exception:
            abi = ''

        return abi

    def get_tx_hash(self):
        try:
            with open(self.tx_hash_path, 'r') as f:
                tx_hash = json.load(f)
        except Exception:
            tx_hash = ''

        return tx_hash

    def get_web3_instance(self):
        try:
            w3 = Web3(Web3.HTTPProvider(self.infura_url))
            w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        except Exception:
            w3 = ''

            return w3

    def get_contract_instance(self):
        try:
            tx_receipt = self.web3_instance.eth.getTransactionReceipt(self.tx_hash)
            contract_address = tx_receipt['contractAddress']
            contract_instance = self.web3_instance.eth.contract(
                abi=self.abi,
                address=contract_address,
                ContractFactoryClass=ConciseContract
            )
        except Exception:
            contract_instance = ''

        return contract_instance

    def get_status(self):
        try:
            status = 'Locked' if self.contract_instance.status() else 'Unlocked'
        except Exception:
            status = 'Unknown'

        return status

    def unlock(self):
        try:
            self.contract_instance.unlock(transact={'from': self.w3.eth.accounts[0]})
        except Exception:
            pass

        return "unlocked"

    def lock(self):
        try:
            self.contract_instance.lock(transact={'from': self.w3.eth.accounts[0]})
        except Exception:
            pass

        return "locked"