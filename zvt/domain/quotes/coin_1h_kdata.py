# -*- coding: utf-8 -*-
from sqlalchemy.ext.declarative import declarative_base

from zvdata.contract import register_schema
from zvt.domain.quotes import KdataCommon

Coin1hKdataBase = declarative_base()


class Coin1hKdata(Coin1hKdataBase, KdataCommon):
    __tablename__ = 'coin_1h_kdata'


register_schema(providers=['ccxt'], db_name='coin_1h_kdata', schema_base=Coin1hKdataBase)
