import time
from sys import argv
import hashlib
import pytest
import requests


class TestCoupon:

    @pytest.fixture(scope="session")
    def token(self):
        """
                获取单点系统token
                :return:
                """
        url = "http://csms-st.evcard.vip:180/evcard-sso/api/loginAjax"
        params = {
            "username": "17301736764@hq",
            "password": "79409c046934219ce6394df684b06f85",
            "code": 123456
        }
        res = requests.get(url, params=params)
        # print(f"token: {res.headers['token']}")
        # print(f"获取token结果 : {res.json()}")
        # cookies = res.headers['token']
        try:
            yield res.headers['token']
        except Exception as e:
            raise ValueError("requests token error")

    def encrypt_md5(self, key):
        """
        md5加密
        :param key:
        :return:
        """
        input_name = hashlib.md5()
        input_name.update(key.encode(encoding='utf-8'))
        return input_name.hexdigest()

    @pytest.mark.parametrize("mobilephone", [(18601615258), (18605558888)])
    def test_offer_third_coupon(self, token, mobilephone, ):
        """
        :param timestamp: 调用时的时间轴（毫秒）
        :param token:
        :param mobilephone:
        :param sn: md5加密后的值，加密顺序（appKey+ timeStamp +secret）,appKey渠道key ，secret为渠道key生成后的secret
        :param couponVals: 优惠券模板发放组合，json字符串；传入json数组对象类型如：
                           “[{‘couponSeq’:1001,’offerNum’:1},{‘couponSeq’:1002,’offerNum’:2}]”
        :param couponSeq: 优惠券模板记录id
        :param offerNum: 发放券数量
        :param activityId: 加密后的活动id(详见活动详情界面)
        :return:
        """
        url = "http://csms-st.evcard.vip:180/evcard-mmp/api/thirdCoupon/offerThirdCoupon"
        timestamp = str(round(time.time() * 1000))
        sn = f"saic_ios{timestamp}c68dc2e2-26b5-4112-aad0-437ad29dae6f"
        sn_md5 = self.encrypt_md5(sn)
        print(sn)
        print(sn_md5)
        headers = {
            "timestamp": timestamp,
            "sn": sn_md5
        }
        cookies = {
            "token": token
        }
        data = {
            "activityId": "h3m49ya9",
            "mobilePhone": f"{mobilephone}",
            "couponVals": "[{'couponSeq': 75266, 'offerNum': 5}]",
        }
        res = requests.post(url=url, json=data, headers=headers, cookies=cookies)
        print(res.json())
