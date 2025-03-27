import requests
from web3 import Web3
from dataclasses import dataclass
from typing import List, Dict
from web3_multicall import Multicall, multicall
from datetime import datetime


class PendleTokenTracker:
    def __init__(self, wallet_address: str, rpc_urls: Dict[str, str], chain_ids: Dict[str, int]):
        self.wallet = Web3.to_checksum_address(wallet_address)
        self.rpc_urls = rpc_urls  # 例如 {'ethereum': 'https://...', 'arbitrum': 'https://...'}
        self.chain_ids = chain_ids  # 例如 {'ethereum': 1, 'arbitrum': 42161}
        self.assets: Dict[str, List[Asset]] = {}  # 鍵為鏈名

    def load_tokens_from_api(self):
        for chain, chain_id in self.chain_ids.items():
            url = f"https://api-v2.pendle.finance/core/v1/{chain_id}/tokens"
            res = requests.get(url)
            data = res.json().get("assets", [])
            self.assets[chain] = [Asset.from_dict(a) for a in data if a.get("tags") and any(t in ["SY", "PT", "YT"] for t in a["tags"])]

    def get_balances(self) -> Dict[str, Dict[str, float]]:
        result = {}
        for chain, asset_list in self.assets.items():
            w3 = Web3(Web3.HTTPProvider(self.rpc_urls[chain]))
            calls = []
            for asset in asset_list:
                calls.append(
                    Call(
                        target=asset.address,
                        function=["balanceOf(address)(uint256)", self.wallet],
                        returns=[(asset.symbol, lambda v: v / (10 ** asset.decimals))]
                    )
                )

            multi = Multicall(calls, _w3=w3)
            balances = multi()  # 回傳 dict
            result[chain] = {k: v for k, v in balances.items() if v > 0}

        return result
