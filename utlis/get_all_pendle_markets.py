from enum_type.chain_id import ChainId
from enum_type.endpoints import PendleAPI
import requests
import json


def get_all_assets_metadata(chain: str):
    url = f'{PendleAPI.ROOT.value}/v3/{ChainId[chain].value}/assets/all'
    res =  requests.get(url)
    return res.json()









