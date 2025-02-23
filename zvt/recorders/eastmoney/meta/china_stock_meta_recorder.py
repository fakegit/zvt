# -*- coding: utf-8 -*-

import requests

from zvdata.recorder import Recorder
from zvt.api.quote import get_entities
from zvt.domain.stock_meta import Stock
from zvdata.utils.time_utils import to_pd_timestamp
from zvdata.utils.utils import to_float, pct_to_float


class ChinaStockMetaRecorder(Recorder):
    provider = 'eastmoney'
    data_schema = Stock

    def __init__(self, batch_size=10, force_update=False, sleeping_time=10, codes=None) -> None:
        super().__init__(batch_size, force_update, sleeping_time)

        self.codes = codes
        if not self.force_update:
            self.entities = get_entities(session=self.session,
                                         entity_type='stock',
                                         exchanges=['sh', 'sz'],
                                         codes=self.codes,
                                         filters=[Stock.profile.is_(None)],
                                         return_type='domain',
                                         provider=self.provider)

    def run(self):
        for security_item in self.entities:
            assert isinstance(security_item, Stock)

            if security_item.exchange == 'sh':
                fc = "{}01".format(security_item.code)
            if security_item.exchange == 'sz':
                fc = "{}02".format(security_item.code)

            # 基本资料
            param = {"color": "w", "fc": fc, "SecurityCode": "SZ300059"}
            resp = requests.post('https://emh5.eastmoney.com/api/GongSiGaiKuang/GetJiBenZiLiao', json=param)
            resp.encoding = 'utf8'

            resp_json = resp.json()['Result']['JiBenZiLiao']

            security_item.profile = resp_json['CompRofile']
            security_item.main_business = resp_json['MainBusiness']
            security_item.date_of_establishment = to_pd_timestamp(resp_json['FoundDate'])

            # 关联行业
            industries = ','.join(resp_json['Industry'].split('-'))
            security_item.industries = industries

            # 关联概念
            security_item.concept_indices = resp_json['Block']

            # 关联地区
            security_item.area_indices = resp_json['Provice']

            self.sleep()

            # 发行相关
            param = {"color": "w", "fc": fc}
            resp = requests.post('https://emh5.eastmoney.com/api/GongSiGaiKuang/GetFaXingXiangGuan', json=param)
            resp.encoding = 'utf8'

            resp_json = resp.json()['Result']['FaXingXiangGuan']

            security_item.issue_pe = to_float(resp_json['PEIssued'])
            security_item.price = to_float(resp_json['IssuePrice'])
            security_item.issues = to_float(resp_json['ShareIssued'])
            security_item.raising_fund = to_float((resp_json['NetCollection']))
            security_item.net_winning_rate = pct_to_float(resp_json['LotRateOn'])

            self.session.commit()

            self.logger.info('finish recording stock meta for:{}'.format(security_item.code))

            self.sleep()


if __name__ == '__main__':
    # init_log('china_stock_meta.log')

    recorder = ChinaStockMetaRecorder()
    recorder.run()
