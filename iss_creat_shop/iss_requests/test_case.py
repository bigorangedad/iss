from time import ctime
import pytest
import requests
import random
import logging

from iss_creat_shop.iss_requests.test_add_shop import TestLogin

logging.basicConfig(level=logging.INFO)

class TestCase(TestLogin):

    def creat_data(self):
        data = [("自增vip网点" + str(random.randint(10, 1000)),
                 "31." + str(random.randint(282000, 285000)),
                 "121." + str(random.randint(160000, 165000))
                 ) for x in range(2)]
        return data

    def mult_data(self):
        data = [(("新增测试网点" + "1%03d" % x),
                 "21." + "1%05d" % x,
                 "112.1%05d" % x
                 ) for x in range(53, 55)]
        return data

    @pytest.mark.parametrize(['shopname', 'latitude', 'longitude'], mult_data("x"))
    def test_all(self, token, shopname, latitude, longitude):
        # 新增网点建设任务
        try:
            assert '0' == self.test_add_shop_build_task(token, shopname)["code"]
        except AssertionError as e:
            if "10020002" in e.__str__():
                assert '0' == self.test_add_shop_build_task(token, shopname)["code"]
        print(f"新增网点名称:{shopname}")
        logging.info(f"本次新增网点名称:{shopname}" + ctime())

        # 查询新增的网点建设任务
        assert shopname == self.test_query_shop_build_task(token, shopname)["data"]["list"][0]["shopName"]
        logging.info(f"校验新增网点成功:{shopname}" + ctime())

        # 审核建设任务
        assert '0' == self.test_complete_shop_build_task(token, shopname)["code"]
        logging.info(f"网点建设任务审核通过" + ctime())

        # 提交施工
        assert '0' == self.test_shop_build_task_construction(token, shopname)["code"]
        logging.info(f"提交网点施工成功" + ctime())

        # 验收任务
        try:
            assert '0' == self.test_check_shop_build_task(token, shopname, latitude, longitude)["code"]
        except AssertionError as e:
            if '10020009' in e.__str__():
                assert '0' == self.test_check_shop_build_task(token, shopname, latitude, longitude)["code"]
        print(f"经纬度: {latitude} ; {longitude}")
        logging.info(f"网点验收通过，经纬度为:{latitude}, {longitude}" + ctime())

        # 审核上线
        assert '0' == self.test_shop_build_task_build_online(token, shopname)["code"]
        logging.info(f"网点上线审核通过" + ctime())

        # 修改网点基础信息
        shopseq = self.test_query_shop_build_task(token, shopname)["data"]["list"][0]["shopSeq"]
        assert '0' == self.test_update_shop_base_info(token, shopname, shopseq)["code"]

if __name__ == '__main__':
    pytest.main()