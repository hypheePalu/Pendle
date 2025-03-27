from enum_type.chain_id import ChainId
from enum_type.endpoints import PendleAPI
import requests
import json


def get_all_assets_metadata(chain: str):
    url = f'{PendleAPI.ROOT.value}/v3/{ChainId[chain].value}/assets/all'
    res =  requests.get(url)
    return res.json()

def get_all_active_markets(chain: str):
    url = f'{PendleAPI.ROOT.value}/v1/{ChainId[chain].value}/markets/active'
    res =  requests.get(url)
    return res.json()







