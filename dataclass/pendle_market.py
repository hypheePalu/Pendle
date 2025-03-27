from dataclasses import dataclass
from typing import Optional, Dict, Any
from datetime import datetime

# @dataclass
# class PendleMarket:
#     Chain_Id:
#     SY:

@dataclass
class Asset:
    address: str
    tag: str

@dataclass
class MarketPool:
    market_address: str
    chain_id:int
    name: str
    SY: Asset
    PT: Asset
    YT: Asset
    underlying_asset: str
    yield_range: dict
    expiry_date: Optional[datetime] = None
    decimal: int = 18


class MultiKeyDict:
    def __init__(self):
        self._data: Dict[str, Any] = {}

    def add(self, value: Any, *keys: str):
        for k in keys:
            self._data[k.lower()] = value

    def get(self, key: str, default=None) -> Any:
        return self._data.get(key.lower(), default)

    def __getitem__(self, key: str) -> Any:
        return self.get(key)

    def __contains__(self, key: str) -> bool:
        return key.lower() in self._data

    def __repr__(self):
        # 類似 dict 的格式：{'key': value_repr, ...}
        preview = {k: repr(v) for k, v in self._data.items()}
        return repr(preview)