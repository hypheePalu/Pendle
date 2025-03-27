from dataclass.pendle_market import Asset, MarketPool, MultiKeyDict
from utlis.get_all_pendle_markets import get_all_active_markets
from dateutil import parser
from enum_type.chain_id import ChainId


def parse_all_active_markets(chain:str):
    multikey  = MultiKeyDict()
    raw = get_all_active_markets(chain)
    data = raw['markets']

    for entry in data:
        sy = Asset(tag='SY',
                   address=entry.get('sy').split('-')[1]
                   )
        yt = Asset(tag='YT',
                   address=entry.get('yt').split('-')[1]
                   )
        pt = Asset(tag='PT',
                   address=entry.get('pt').split('-')[1]
                   )

        market_pool = MarketPool(
            market_address=entry.get('address'),
            chain_id=ChainId[chain].value,
            name=entry.get('name'),
            underlying_asset = entry.get('underlyingAsset').split('-')[1],
            yield_range=entry.get('details').get('yieldRange'),
            expiry_date=parser.isoparse(entry.get('expiry')),
            SY=sy,
            PT=pt,
            YT=yt
        )
        multikey.add(market_pool, market_pool.name, market_pool.market_address)

    return multikey



