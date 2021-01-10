import json
import logging
import random
import re
import time
from logging import log
import pytest
import requests

logging.basicConfig(level=logging.INFO)


class TestLogin:
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
        print(f"token: {res.headers['token']}")
        print(f"获取token结果 : {res.json()}")
        cookies = res.headers['token']
        try:
            yield res.headers['token']
        except Exception as e:
            raise ValueError("requests token error")

    def test_access_token(self):
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
        print(f"token: {res.headers['token']}")
        print(f"获取token结果 : {res.json()}")
        cookies = res.headers['token']
        try:
            return res.headers['token']
        except Exception as e:
            raise ValueError("requests token error")

    @pytest.mark.parametrize('shopname', ["新增测试网点999"])
    def test_add_shop_build_task(self, shopname, token):
        """
        新增网点建设任务
        :return:
        """

        url = "http://csms-st.evcard.vip:180/evcard-iss/api/addShopBuildTask"
        cookies = {
            "token": f"{token}"
        }
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json;charset=UTF-8"
        }
        payload = {
            "address": f"{shopname}网点地址",
            "addressDesc": "",
            "agencyAmount": 1200,
            "agencyAmountUnit": 3,
            "agencyId": "",
            "appRemark": "",
            "areaCode": 310114,
            "autoOfflineDuration": 0,
            "baiduLatitude": "",
            "baiduLongitude": "",
            "bankName": "",
            "bankNo": "",
            "bankUser": "",
            "billPeriod": [{"startTime": "2020-01-01", "endTime": "2020-01-31"}],
            "billPeriodRule": 1,
            "businessTag": "",
            "chargeType": 1,
            "contractBeginTime": "2020-01-01",
            "contractEndTime": "2020-01-31",
            "contractScanning": "/shopInfo/contract_scanning/0abb39e4-22cd-4a12-bfdb-c69855d07619/01.pdf,",
            "couponAddAmount": 0,
            "couponAddType": 1,
            "couponMinAmount": 0,
            "couponTotalAmount": 0,
            "dotType": "",
            "electricAmount": 1.3,
            "expandMode": 2,
            "freeDuration": 0,
            "isRestrict": 0,
            "isRestrictVehicleNo": 0,
            "isTakePhotoReturn": 0,
            "latitude": "",
            "longitude": "",
            "maxUsableCarport": 200,
            "navigateAddress": "",
            "operateType": 1,
            "orgId": "000T",
            "parkFloorDown": "",
            "parkFloorUp": "",
            "parkLocation": "",
            "parkNum": 2,
            "publicCarportNumber": 1,
            "regionid": 320586,
            "remark": "",
            "rentStakeAmount": 500,
            "rentStakeNum": 0,
            "restrictVehicleNo": "",
            "serverType": 1,
            "shopActiveDTO": {},
            "shopCloseTimeNormal": 235900,
            "shopExplorePicture": "",
            "shopKind": 0,
            "shopName": f"{shopname}",
            "shopOpenTimeNormal": "000000",
            "shopPicUrl": "",
            "shopProperty": 1,
            "shopSiteList": [],
            "shopSpecies": 1,
            "shopSystemType": 1,
            "shopType": "",
            "stackNum": 0,
            "storeNTag": [],
            "supplierId": 2,
            "tenementCompany": "物业所属公司",
            "tenementContact": "物业联系人",
            "tenementName": "签约方抬头",
            "tenementPosition": "物业联系人职位",
            "tenementTelephone": 13898998899,
            "totalParkCost": 1200,
            "totalParkCostStage": [],
            "unifiedSocialCreditCode": "F00A012223B"
        }
        res = requests.post(url=url, json=payload, headers=headers, cookies=cookies)
        print(f"result : {res.json()}")
        print(res.json())
        return res.json()

    def test_query_shop_build_task_list(self, shopname, token):
        """
        网点建设任务查询
        :return:
        """
        url = "http://csms-st.evcard.vip:180/evcard-iss/api/queryShopBuildTaskList"
        cookies = {
            "token": f"{token}"
        }
        headers = {
            "Accept": "application/json,text/plain,*/*",
            "Content-Type": "application/json;charset=UTF-8"
        }
        payload = {
            "buildSeq": "",
            "endUpdateTime": "",
            "isAll": 0,
            "orgId": "000T",
            "pageNum": 1,
            "pageSize": 50,
            "regionId": "",
            "serverType": "",
            "shopName": f"{shopname}",
            "shopSpecies": "",
            "startUpdateTime": "",
            "taskStatus": ""
        }

        res = requests.post(url=url, data=json.dumps(payload), headers=headers, cookies=cookies)
        shop_list = res.json()
        print(shop_list)
        shop_info = {}
        shop_name = shop_list["data"]["list"][0]["shopName"]
        shop_build_id = shop_list["data"]["list"][0]["shopBuildId"]
        shop_seq = shop_list["data"]["list"][0]["shopSeq"]
        shop_info = {"shop_build_id": shop_build_id, "shop_seq": shop_seq, "shop_name": shop_name}
        print(shop_info)
        return shop_info

    def test_query_shop_build_task(self, shopname, token):
        """
        网点列表查询，断言用
        :param shopname:
        :return:
        """
        url = "http://csms-st.evcard.vip:180/evcard-iss/api/queryShopBuildTaskList"
        cookies = {
            "token": f"{token}"
        }
        headers = {
            "Accept": "application/json,text/plain,*/*",
            # "Accept-Encoding": "gzip, deflate",
            # "Accept-Language": "zh-CN,zh;q=0.9",
            # "Cache-Control": "no-cache",
            # "Connection": "keep-alive",
            # "Content-Length": "179",
            "Content-Type": "application/json;charset=UTF-8"
        }
        payload = {
            "buildSeq": "",
            "endUpdateTime": "",
            "isAll": 0,
            "orgId": "000T",
            "pageNum": 1,
            "pageSize": 50,
            "regionId": "",
            "serverType": "",
            "shopName": f"{shopname}",
            "shopSpecies": "",
            "startUpdateTime": "",
            "taskStatus": ""
        }

        res = requests.post(url=url, data=json.dumps(payload), headers=headers, cookies=cookies)
        shop_list = res.json()
        print(shop_list)
        return shop_list

    @pytest.mark.parametrize("shopname", ["新增测试网点003"])
    def test_complete_shop_build_task(self, shopname, token):
        """
        审核建设任务通过
        :return:
        """
        url = "http://csms-st.evcard.vip:180/evcard-iss/api/completeShopBuildTask"
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json;charset=UTF-8",
        }
        cookies = {
            "token": f"{token}",
            # "bvmToken": "9ef30f42-c84b-4631-8c60-c855b2afd120",
            # "ssomac": "bqW0N05_SGaAmm1RXEiEug",
            # "SERVERID": "7afe8ce295581c36b8c229d846f05046|1608791449|1608791410"
        }
        payload = {
            "pastFlag": 1,
            "rentStakeAmount": 500,
            "rentStakeNum": 0,
            "stackNum": 0
        }
        res = requests.put(url=url + f"/{self.test_query_shop_build_task_list(shopname, token)['shop_build_id']}",
                           cookies=cookies,
                           headers=headers, data=json.dumps(payload))
        return res.json()

    def test_shop_build_task_construction(self, shopname, token):
        """
        提交施工
        :param test_query_shop_build_task_list:
        :return:
        """
        url = "http://csms-st.evcard.vip:180/evcard-iss/api/shopBuildTaskConstruction/"
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json;charset=UTF-8"
        }
        cookies = {
            "token": f"{token}",
            # "bvmToken": "9ef30f42-c84b-4631-8c60-c855b2afd120",
            # "ssomac": "rC988IJ6SxC92o5m0cNhUA",
            # "SERVERID": "7afe8ce295581c36b8c229d846f05046|1609139512|1609139339"
        }
        payload = {
            "applyCheck": 1,
            "completionDate": "2020-12-28",
            "constructionPicture": "",
            "constructionStatus": 2,
            "scopeDate": "2020-12-29",
            "shopConstructionId": 37
        }
        res = requests.put(url=url + f"{self.test_query_shop_build_task_list(shopname, token)['shop_build_id']}",
                           json=payload,
                           headers=headers, cookies=cookies)
        print(f"提交施工: {res.json()}")
        return res.json()

    def test_check_shop_build_task(self, shopname, latitude, longitude, token):
        """
        验收
        :param test_query_shop_build_task_list: shop_build_id
        :return:
        """
        url = "http://csms-st.evcard.vip:180/evcard-iss/api/checkShopBuildTask/"
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json;charset=UTF-8",
        }
        cookies = {
            "token": f"{token}",
            # "bvmToke": "9ef30f42-c84b-4631-8c60-c855b2afd120",
            # "ssomac": "7c-L1ZSBRRGud0w7_Z1cLg",
            # "SERVERID": "7afe8ce295581c36b8c229d846f05046|1609148050|1609147887"
        }
        payload = {
            "address": f"{shopname}网点地址",
            "addressDesc": f"{shopname}位置描述",
            "agencyAmount": 1200,
            "agencyAmountUnit": 3,
            "agencyId": 00,
            "agencyName": "普通",
            "ammeterNo": "",
            "appRemark": "",
            "areaCode": 310114,
            "areaCodeName": "嘉定区",
            "areaid": "",
            "autoOfflineDuration": 0,
            "baiduLatitude": "null",
            "baiduLongitude": "null",
            "balanceWay": 1,
            "bankName": "",
            "bankNo": "",
            "bankUser": "",
            "billPeriod": [{"startTime": "2020-01-01", "endTime": "2020-01-31"},
                           {"startTime": "2020-02-01", "endTime": "2020-02-29"}],
            "billPeriodRule": 1,
            "bluetoothFlag": "0",
            "businessTag": 1,
            "cancleFlag": "null",
            "carportAmount": "null",
            "carportQuantity": 0,
            "chargeAmount": "",
            "chargeReturnFlag": 2,
            "chargeType": 1,
            'checkCode': "",
            "city": 310100,
            "cityName": "上海市",
            "completionDate": "2020-12-28",
            "constructionPicture": "",
            "constructionStatus": 2,
            "contractBeginTime": "2020-01-01",
            "contractEndTime": "2020-07-31",
            "contractNo": "",
            "contractScanning": "/shopInfo/contract_scanning/0abb39e4-22cd-4a12-bfdb-c69855d07619/01.pdf",
            "coordinateList": [],
            "coordinates": "120.11233",
            "couponAddAmount": "null",
            "couponAddType": "null",
            "couponMinAmount": "null",
            "couponTotalAmount": "null",
            "deputyCoordinates": [],
            "derateAmount": "null",
            "dismissReason": "",
            "dotParkId": "null",
            "dotType": 0,
            "downloadSpeed": "",
            "electricAmount": "1.30",
            "electricityBoxPicture": "null",
            "expandMode": 2,
            "forPublic": "",
            "freeDuration": "null",
            "grade": [],
            "invoiceTitle": "null",
            "isCarwash": 0,
            "isCharge": 0,
            "isQuickRepair": 0,
            "isRestrict": 0,
            "isRestrictVehicleNo": 0,
            "isScanCharge": "null",
            "isTakePhotoReturn": 0,
            "isWatch": 0,
            "lamphouseType": "null",
            "lamphouseVerticalNum": 0,
            "lamphouseWallNum": 0,
            "latitude": f"{latitude}",
            "longitude": f"{longitude}",
            "maxUsableCarport": 20,
            "navigateAddress": f"{shopname}导航地址",
            "networkDelay": "",
            "networkSpeedPicture": "null",
            "openTime": "",
            "orgId": "000T",
            "orgName": "上海国际汽车城新能源汽车运营服务有限公司",
            "parkAmount": 0,
            "parkFloorDown": 0,
            "parkFloorUp": 0,
            "parkLocation": 0,
            "parkNum": "2",
            "parkWayId": 0,
            "parkingLockNumber": 0,
            "passFlag": 1,
            "pickvehAmount": "null",
            "province": 310000,
            "provinceName": "上海市",
            "publicCarportNumber": 1,
            "reason": "",
            "regionName": "车城区域",
            "regionid": 320586,
            "remark": "",
            "rentStakeAmount": 500,
            "rentStakeNum": 0,
            "restrictVehicleNo": "",
            "returnvehAmount": "null",
            "scopeDate": "2020-12-29",
            "serverType": 1,
            "shopActiveDTO": "{startTime1: null, endTime1: null, startTime2: null, endTime2: null,\
             startTime3: null,endTime3: null}",
            "shopCloseTimeNormal": "235900",
            "shopConstructionId": 37,
            "shopExplorePicture": "",
            "shopKind": 0,
            "shopLocalPicture": "null",
            "shopName": f"{shopname}",
            "shopOpenTimeNormal": "000000",
            "shopPicUrl": "/shopImg/a4bed7f3-818a-4fd0-82d4-f576259915ca/202012281734108800.jpg",
            "shopPriceAddList": "null",
            "shopPriceIds": "null",
            "shopProperty": "1",
            "shopRank": "null",
            "shopReplenishList": "null",
            "shopReplenishListForDouble": [],
            "shopSeq": 17781,
            "shopSiteList": [],
            "shopSiteType": "",
            "shopSpecies": 1,
            "shopSystemType": 1,
            "shopSystemTypeList": [0, 1],
            "shopType": 3,
            "shortRentCloseTime": "null",
            "shortRentOpenTime": "null",
            "showImgTitle": "http://evcard.oss-cn-shanghai.aliyuncs.com/test",
            "simCode": "null",
            "specialCarportAmount": 0,
            "specialCarportQuantity": 0,
            "stackNum": "0",
            "storeNTag": [],
            "supplierId": 2,
            "supplierName": "上海外包公司1",
            "taskStatus": 4,
            "tenementCompany": "物业所属公司",
            "tenementContact": "物业联系人",
            "tenementName": "签约方抬头",
            "tenementPosition": "物业联系人职位",
            "tenementTelephone": "13898998899",
            "totalParkCost": 1200,
            "totalParkCostStage": [],
            "unifiedSocialCreditCode": "F00A012223B",
            "uploadSpeed": "",
            "walkingTrack": "",
            "warningSignVerticalNum": 0,
            "warningSignWallNum": 0
        }
        res = requests.put(url=url + f"{self.test_query_shop_build_task_list(shopname, token)['shop_build_id']}",
                           cookies=cookies, headers=headers,
                           json=payload)
        print(f"网点验收：{res.json()}")
        return res.json()

    def test_shop_build_task_build_online(self, shopname, token):
        """
        网点建设任务审核上线
        :param :
        :return:
        """

        url = "http://csms-st.evcard.vip:180/evcard-iss/api/shopBuildTask/buildOnline"
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json;charset=UTF-8",
        }
        cookies = {
            "token": f"{token}",
            # "bvmToken": "9ef30f42-c84b-4631-8c60-c855b2afd120",
            # "ssomac": "TVKRulwgRFiTq_v0RqFa2g",
            # "SERVERID": "7afe8ce295581c36b8c229d846f05046|1609293747|1609293672"
        }
        payload = {
            "appImages": "",
            "checkResult": 1,
            "isNowTime": 1,
            "onOffTime": "2020-12-30 10:02:48",
            "shopBuildId": f"{self.test_query_shop_build_task_list(shopname, token)['shop_build_id']}",
            "shopSeq": f"{self.test_query_shop_build_task_list(shopname, token)['shop_seq']}"
        }
        res = requests.post(url=url, headers=headers, cookies=cookies, json=payload)
        print(res.json())
        return res.json()

    def test_creat_data(self):
        data = [("新增测试网点" + str(random.randint(10, 1000)),
                 str(random.randint(20, 39)) + "." + str(random.randint(100000, 999999)),
                 str(random.randint(115, 139)) + "." + str(random.randint(100000, 999999))
                 ) for x in range(1)]
        return data

    def test_mult_data(self):
        data = [(("新增测试网点" + "1%02d" % x),
                 "30." + "1%05d" % x,
                 "120.1%05d" % x
                 ) for x in range(2)]
        return data

    @pytest.mark.parametrize(['shopname', 'latitude', 'longitude'], test_mult_data("x"))
    def test_all(self, shopname, latitude, longitude, token):
        # 新增网点建设任务
        # assert '0' == self.test_add_shop_build_task(shopname, token)["code"]
        try:
            assert '0' == self.test_add_shop_build_task(shopname, token)["code"]
        except AssertionError as e:
            if "10020002" in e.__str__():
                assert '0' == self.test_add_shop_build_task(shopname, token)["code"]
        print(f"新增网点:{shopname}")
        # 审核建设任务
        assert '0' == self.test_complete_shop_build_task(shopname, token)["code"]
        print("网点审核建设任务通过")

        # 提交施工
        assert '0' == self.test_shop_build_task_construction(shopname, token)["code"]
        print("网点提交施工成功")

        # 验收任务
        try:
            assert '0' == self.test_check_shop_build_task(shopname, latitude, longitude, token)["code"]
        except AssertionError as e:
            if '10020009' in e.__str__():
                assert '0' == self.test_check_shop_build_task(shopname, latitude, longitude, token)["code"]
        print(f"经纬度为：{latitude}", f"{longitude}")
        print("网点验收通过")

        # 审核上线
        assert '0' == self.test_shop_build_task_build_online(shopname, token)["code"]
        print("网点上线审核通过")


if __name__ == "__main__":
    # Test_login()
    TestLogin.test_all()
