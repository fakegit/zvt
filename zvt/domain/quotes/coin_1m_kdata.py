# -*- coding: utf-8 -*-
from sqlalchemy.ext.declarative import declarative_base

from zvdata.contract import register_schema
from zvt.domain.quotes import TickCommon

Coin1mKdataBase = declarative_base()


class Coin1mKdata(Coin1mKdataBase, TickCommon):
    __tablename__ = 'coin_1m_kdata'


register_schema(providers=['ccxt'], db_name='coin_1m_kdata', schema_base=Coin1mKdataBase)
