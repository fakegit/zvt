# -*- coding: utf-8 -*-
from sqlalchemy import String, Column, Float

from zvdata import Mixin


class KdataCommon(Mixin):
    provider = Column(String(length=32))
    code = Column(String(length=32))
    name = Column(String(length=32))
    # Enum constraint is not extendable
    # level = Column(Enum(IntervalLevel, values_callable=enum_value))
    level = Column(String(length=32))

    # 如果是股票，代表前复权数据
    # 开盘价
    open = Column(Float)
    # 收盘价
    close = Column(Float)
    # 最高价
    high = Column(Float)
    # 最低价
    low = Column(Float)
    # 成交量
    volume = Column(Float)
    # 成交金额
    turnover = Column(Float)


class StockKdataCommon(KdataCommon):
    # 涨跌幅
    change_pct = Column(Float)
    # 换手率
    turnover_rate = Column(Float)


class TickCommon(Mixin):
    provider = Column(String(length=32))
    code = Column(String(length=32))
    name = Column(String(length=32))
    level = Column(String(length=32))

    order = Column(String(length=32))
    price = Column(Float)
    volume = Column(Float)
    turnover = Column(Float)
    direction = Column(String(length=32))
    order_type = Column(String(length=32))


from .coin_tick_kdata import *
from .coin_1m_kdata import *
from .coin_1h_kdata import *
from .coin_1d_kdata import *
from .coin_1wk_kdata import *
from .coin_1mon_kdata import *

from .index_1d_kdata import *
from .index_1wk_kdata import *
from .index_1mon_kdata import *

from .stock_1m_kdata import *
from .stock_5m_kdata import *
from .stock_15m_kdata import *
from .stock_30m_kdata import *
from .stock_1h_kdata import *
from .stock_1d_kdata import *
from .stock_1wk_kdata import *
from .stock_1mon_kdata import *
