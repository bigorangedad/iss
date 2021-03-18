import json
import logging
import random
import re
import time

import pytest
import requests
logging.basicConfig(level=logging.INFO)

class TestUserCard:
    @pytest.fixture(scope="session")
    def token(self):
        url = "http://csms-st.evcard.vip:180/evcard-sso/api/loginAjax"
        params = {
            "username": "17301736764@hq",
            "password": "79409c046934219ce6394df684b06f85",
            "code": 123456
        }
        res = requests.get(url=url, params=params)
        print(res.headers['token'])
        print(res.json())
        print(res.text)
        # token = res.headers['token']
        try:
            yield res.headers['token']
        except Exception as e:
            raise ValueError("requests token error")

    def test_access_token(self):
        url = "http://csms-st.evcard.vip:180/evcard-sso/api/loginAjax"
        params = {
            "username": "17301736764@hq",
            "password": "79409c046934219ce6394df684b06f85",
            "code": 123456
        }
        res = requests.get(url=url, params=params)
        # print(res.headers['token'])
        print(res.json())
        print(res.text)
        # token = res.headers['token']
        try:
            return res.headers['token']
        except Exception as e:
            raise ValueError("requests token error")

    def test_add_data(self):
        data = [("自增vip卡0" + str(random.randint(1, 99)),
                 str(random.randint(1, 99)),
                 str(random.randint(1, 300))
                 ) for x in range(2)]
        return data

    # def test_update_data(self):
    #     data = [
    #
    #     ]
    #     return data

    # @pytest.mark.parametrize(["cardName", "discount", "maxValue"], [("自增vip卡0"+str(random.randint(1, 99)),
    #             str(random.randint(1, 99)),
    #             str(random.randint(1, 300))
    #              )for x in range(1)])
    # @pytest.mark.parametrize(["cardName", "discount", "maxValue"], [("自增vip卡073", "54", "231")])
    @pytest.mark.parametrize(["cardName", "discount", "maxValue"],
                             [("自增vip卡ce", "88", "288")])
    def test_creat_card(self, token, cardName, discount, maxValue):
        """
        创建卡片模板
        :return:
        """
        url = "http://csms-st.evcard.vip:180/evcard-mmp/api/vipcard/card/add"
        data = {
            "cardName": cardName,
            "orgId": "00",
            "cardType": 1,
            "discount": discount,
            "maxValue": maxValue,
            "durationLimit": 5,
            "cityIds": [310100, 331100, 330100, 330800],
            "vehicleModels": [188, 211],
            "rentMethods": [0, 2, 3],
            "startTime": "000000",
            "endTime": "240000",
            "availableDaysOfWeek": [],
            "personPurchasesLimit": 10,
            "rules": f"{cardName} 卡片使用规则说明"
        }
        cookies = {
            "token": token
        }
        res = requests.post(url=url, json=data, cookies=cookies)
        print(res.json())
        print(f"卡片名称:{cardName}, 折扣:{discount}, 可抵扣金额:{maxValue}")
        return res.json()

    @pytest.mark.parametrize("cardId", ["100044"])
    def test_card_list_by_id(self, token, cardId):
        """
        查询卡片-卡片id
        :param token:
        :param cardName:
        :return:
        """
        url = "http://csms-st.evcard.vip:180/evcard-mmp/api/vipcard/card/list"
        data = {
            "cardId": cardId
        }
        cookies = {
            "token": token
        }
        res = requests.post(url=url, cookies=cookies, json=data)
        # dic = res.json()['data']['list'][0]
        # print(dic)
        # dic2 = ["cardName", "cardId"]
        # dic3 = {}
        # for i in dic.keys():
        #     if i in dic2:
        #         dic3 = {dic2[i]: i}
        # print(dic3)
        # print(dic)
        print(res.json())
        return res.json()

    def test_card_list_by_cardName(self, token, cardName):
        """
        查询卡片-卡片名称
        :param token:
        :param cardName:
        :return:
        """
        url = "http://csms-st.evcard.vip:180/evcard-mmp/api/vipcard/card/list"
        data = {
            "cardName": cardName
        }
        cookies = {
            "token": token
        }
        res = requests.post(url=url, cookies=cookies, json=data)
        print(res.json())
        return res.json()

    # @pytest.mark.parametrize(["cardId", "cardName", "discount", "maxValue"],
    #                          [("100026",
    #                            "自增修改卡01",
    #                            str(random.randint(1, 99)),
    #                            str(random.randint(189, 300))
    #                            ) for x in range(1)])
    def test_update_card(self, token, cardId, cardName, discount, maxValue):
        """
        修改卡片
        :param token:
        :param cardName:
        :param discount:
        :param maxValue:
        :return:
        """
        url = "http://csms-st.evcard.vip:180/evcard-mmp/api/vipcard/card/update"
        cookies = {
            "token": token
        }
        data = {
            "cardId": cardId,
            "cardName": cardName,
            "orgId": "00",
            "cardType": 1,
            "discount": discount,
            "maxValue": maxValue,
            "durationLimit": 0,
            "cityIds": [],
            "vehicleModels": [188, 211],
            "rentMethods": [0, 2, 3],
            "startTime": "000000",
            "endTime": "240000",
            "availableDaysOfWeek": [],
            "personPurchasesLimit": 10,
            "rules": f"{cardName} 卡片使用规则说明updated"
        }
        res = requests.post(url=url, cookies=cookies, json=data)
        print(res.json())
        return res.json()

    # @pytest.mark.parametrize(["cardName", "discount", "maxValue"],
    #                          [("自增vip卡0" + str(random.randint(1, 199)),
    #                            75,
    #                            199
    #                            ) for x in range(1)])
    @pytest.mark.parametrize(["cardName", "discount", "maxValue"],
                             [("自增vip卡ce", "88", "288")])
    # @pytest.mark.parametrize(["cardName", "discount", "maxValue"],
    #                          [("自增vip卡0" + str(random.randint(1, 199)),
    #                            str(random.randint(5, 95)),
    #                            str(random.randint(10, 299))
    #                            ) for x in range(20)])
    def test_card_all(self, token, cardName, discount, maxValue):
        # 新增卡片
        try:
            assert '新增卡片成功' == self.test_creat_card(token, cardName, discount, maxValue)['message']
            logging.info("新增卡片成功" + str(time.time()))
        except AssertionError as e:
            if '已存在相同限制条件的卡片' in e.__str__():
                print("错误信息：" + e.__str__())
                change_cardId = re.findall(r"\d{6}", e.__str__())[0]
                print(f"需要更新的卡id:{change_cardId}")
                update_cardName = self.test_card_list_by_id(token, change_cardId)['data']['list'][0]['cardName']
                # change_discount = int(discount) + random.randint(0, 5)
                # change_maxValue = int(maxValue) + random.randint(1, 99)
                change_discount = int(discount) + 1
                change_maxValue = int(maxValue) + 1
                print("需要修改的卡片：update_cardName" + update_cardName)
                print("修改后的折扣：update_discount" + str(change_discount))
                print("修改后的可抵金额：update_maxValue" + str(change_maxValue))
                logging.info(f"存在相同限制条件卡片，id为:{change_cardId}" + str(time.time()))
                assert '修改卡片成功' == self.test_update_card(
                    token, change_cardId, update_cardName, change_discount, change_maxValue)['message']
                print("修改卡片成功")
            assert '新增卡片成功' == self.test_creat_card(token, cardName, discount, maxValue)['message']
        logging.info("新增卡片成功，卡片" + str(time.time()))
        # 更新卡片
        try:
            update_cardId = self.test_card_list_by_cardName(token, cardName)['data']['list'][0]['cardId']
            update_cardName = cardName + "Up"
            update_discount = int(discount) + 1
            update_maxValue = int(maxValue) + 1
            assert '修改卡片成功' == self.test_update_card(
                token, update_cardId, update_cardName, update_discount, update_maxValue)['message']
        except AssertionError as e:
            if '已存在相同限制条件的卡片' in e.__str__():
                change_update_cardId = re.findall(r"\d{6}", e.__str__())[0]
                print("需要更新的卡id:" + change_update_cardId)

                change_update_cardName = str(self.test_card_list_by_id(token, change_update_cardId
                                                                       )['data']['list'][0]['cardName']) + "up"
                change_update_discount = int(self.test_card_list_by_id(token, change_update_cardId
                                                                       )['data']['list'][0]['discount']) + 3
                change_update_maxValue = int(self.test_card_list_by_id(token, change_update_cardId
                                                                       )['data']['list'][0]['maxValue']) + 3
                change_update_info = {"change_update_cardName": change_update_cardName,
                                      "change_update_discount": change_update_discount,
                                      "change_update_maxValue": change_update_maxValue}
                print("info_list:" + str(change_update_info))
                self.test_update_card(token, change_update_cardId,
                                          change_update_cardName,change_update_discount,change_update_maxValue)
            assert '修改卡片成功' == self.test_update_card(
                token, update_cardId, update_cardName, update_discount, update_maxValue)['message']

    @pytest.mark.parametrize(["cardId", "activityName", "salesPrice", "underlinePrice",
                            "startTime", "endTime", "advanceNoticeTime"],
                             [("100044", "自增vip活动001", "60", "188", "20210118090000", "20210131240000",
                              "20210117160000")])
    def test_creat_activity(self, token, cardId, activityName, salesPrice, underlinePrice,
                            startTime, endTime, advanceNoticeTime):
        """
        新增活动
        :param token: token
        :param cardId: 卡片id
        :param activityName: 活动名称
        :param salesPrice: 售价
        :param underlinePrice: 划线价
        :param startTime: 活动开始时间
        :param endTime: 活动结束时间
        :param advanceNoticeTime: 预告时间
        :return: 新增结果
        """
        url = "http://csms-st.evcard.vip:180/evcard-mmp/api/vipcard/activity/add"
        cookies = {
            "token": token
        }
        data = {
            "cardId": cardId,
            "activityName": activityName,
            "orgId": "00",
            "salesPrice": salesPrice,
            "underlinePrice": underlinePrice,
            "personPurchasesLimit": 5,
            "startTime": startTime,
            "endTime": endTime,
            "advanceNoticeTime": advanceNoticeTime,
            "stock": 999,
            "rules": "活动规则说明 XX--00"
        }
        res = requests.post(url=url, json=data, cookies=cookies)
        print(res.headers)
        print(res.text)
        return res.json()

    @pytest.mark.parametrize(["activityName", "cardId"], [("自增vip活动001", "100044")])
    def test_activity_list(self, token, activityName, cardId):
        """
        活动查询
        :param token: token
        :param activityName: 活动名称
        :param cardId: 卡片id
        :return:
        """
        url = "http://csms-st.evcard.vip:180/evcard-mmp/api/vipcard/activity/list"
        cookies = {
            "token": token
        }
        data = {
            "activityName": activityName,
            "cardId": cardId
        }
        res = requests.post(url=url, cookies=cookies, json=data)
        print(res.json())
        return res.json()

    @pytest.mark.parametrize(["id", "activityName", "cardId", "salesPrice", "underlinePrice",
                              "startTime", "endTime", "advanceNoticeTime"],
                             [("100044", "自增vip活动001", "100044", "60", "188", "20210118090000", "20210131240000",
                               "20210117200000")])
    def test_activity_update(self, token, id, activityName, cardId, salesPrice, underlinePrice,
                             startTime, endTime, advanceNoticeTime):
        """
        修改活动
        :param token:
        :param id: 活动id
        :param activityName: 活动名称
        :param cardId: 卡片id
        :param salesPrice: 售价
        :param underlinePrice: 划线价
        :param startTime: 活动开始时间
        :param endTime: 活动结束时间
        :param advanceNoticeTime: 预告时间
        :return:
        """
        url = "http://csms-st.evcard.vip:180/evcard-mmp/api/vipcard/activity/update"
        cookies = {
            "token": token
        }
        data = {
            "id": id,
            "activityName": activityName,
            "orgId": "00",
            "cardId": cardId,
            "salesPrice": salesPrice,
            "underlinePrice": underlinePrice,
            "personPurchasesLimit": 5,
            "startTime": startTime,
            "endTime": endTime,
            "advanceNoticeTime": advanceNoticeTime,
            "stock": 888,
            "rules": "活动规则说明update"
        }
        res = requests.post(url=url, cookies=cookies, json=data)
        return res.json()

    # @pytest.mark.parametrize("id", [100034])
    def test_delete_activity(self, token, id):
        """
        删除活动
        :param token:
        :param id:
        :return:
        """
        url = "http://csms-st.evcard.vip:180/evcard-mmp/api/vipcard/activity/delete/"
        cookies = {
            "token": token
        }
        params = {
            "id": id
        }
        res = requests.put(url=url + f"{id}", cookies=cookies)
        return res.text

    @pytest.mark.parametrize("id", ["100043"])
    def test_publish_activity(self, token, id):
        """
        活动审核通过（发布）
        :param token:
        :param id:
        :return:
        """
        url = "http://csms-st.evcard.vip:180/evcard-mmp/api/vipcard/activity/publish/"
        cookies = {
            "token": token
        }
        res = requests.put(url=url + f"{id}", cookies=cookies)
        print(res.text)
        return res.text


    @pytest.mark.parametrize("id", [100045])
    def test_start_activity(self, token, id):
        """
        活动开始（上架）
        :param token:
        :param id:
        :return:
        """
        url = "http://csms-st.evcard.vip:180/evcard-mmp/api/vipcard/activity/start/"
        cookies = {
            "token": token
        }
        res = requests.put(url=url + f"{id}", cookies=cookies)
        print(res.text)
        return res.text

    @pytest.mark.parametrize("id", [100045])
    def test_stop_activity(self, token, id):
        """
        活动停止（下架）
        :param token:
        :param id:
        :return:
        """
        url = "http://csms-st.evcard.vip:180/evcard-mmp/api/vipcard/activity/stop/"
        cookies = {
            "token": token
        }
        res = requests.put(url=url + f"{id}", cookies=cookies)
        print(res.text)
        return res.text


    @pytest.mark.parametrize(["cardId", "activityName", "salesPrice", "underlinePrice",
                              "startTime", "endTime", "advanceNoticeTime"],
                             [("100044",
                               "自增vip活动001",
                               "60",
                               "188",
                               "20210118090000",
                               "20210131240000",
                               "20210117200000")])
    def test_activity_all(self, token,
                          cardId, activityName, salesPrice, underlinePrice, startTime, endTime, advanceNoticeTime):
        #新增活动：
        assert "新增活动成功" == self.test_creat_activity(
            token, cardId, activityName, salesPrice, underlinePrice, startTime, endTime, advanceNoticeTime)["message"]
        #修改活动：
        id = self.test_activity_list(token, activityName, cardId)['data']['list'][0]['id']
        print(id)
        assert "修改活动成功" == self.test_activity_update(token, id, activityName, cardId, salesPrice, underlinePrice,
                                                     startTime, endTime, advanceNoticeTime)["message"]
        #审核活动：
        assert "审核成功" == self.test_publish_activity(token, id)["message"]

        #上架活动：
        assert "上架成功" == self.test_start_activity(token, id)["message"]

        #下架活动：
        assert "下架成功" == self.test_stop_activity(token, id)["message"]



if __name__ == '__main__':
    TestUserCard.test_access_token()
