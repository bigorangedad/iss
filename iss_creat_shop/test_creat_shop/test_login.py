import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait



class Test_Main:
    def setup(self):
        self.driver = webdriver.Chrome()
        # self.driver.maximize_window()
        # self.driver.execute_script("document.body.style.zoom='0.8'")
        self.driver.get("http://csms-st.evcard.vip:180/evcard-sso/login.html?redirectUrl=http://csms-st.evcard.vip:180/evcard-iss/index.html#/")
        self.driver.implicitly_wait(3)

# class TestLogin:
#     def setup(self):
#         option = Options()
#         option.debugger_address = "localhost:9222"
#         self.driver = webdriver.Chrome(options=option)
#         self.driver.get("http://csms-st.evcard.vip:180/evcard-sso/login.html?redirectUrl=http://csms-st.evcard.vip:180/evcard-iss/index.html#/")
    def test_login(self):
        #输入手机号、密码、机构，点击登录
        self.driver.find_element(By.XPATH, '//*[@placeholder="手机号／工号（非客服工号）"]').\
            send_keys("18117150858")
        self.driver.find_element(By.XPATH, '//*[@placeholder="密码"]').\
            send_keys("lwJ1989010@")
        self.driver.find_element(By.XPATH, '//*[@placeholder="登录机构"]').\
            send_keys("hq")
        print("输入完成")
        self.driver.find_element(By.XPATH, '//*[@value="登录"]').click()
        print("点击登录")
        #显示等待,验证码出现后输入
        # time.sleep(0.5)
        def wait01(x):
            return len(self.driver.find_elements(By.XPATH, '//*[@value="获取验证码"]')) >= 1

        WebDriverWait(self.driver, 10).until(wait01)
        print("验证码出现了")

        self.driver.find_element(By.XPATH, '//*[@name="code"]').\
            send_keys("123456")
        # time.sleep(1)
        self.driver.find_element(By.XPATH, '//*[@value="登录"]').click()
    # def test_creat_shop(self):
        """
        创建网点
        :return:
        """
        self.driver.find_element(By.XPATH, '//*[@class="el-submenu"][1]').click()

        def wait02(x):
            """
            等待'网点建设'标签出现
            :param x:
            :return:
            """
            return len(self.driver.find_elements(By.XPATH, '//*[@class="el-menu-item is-active"]')) >= 1
        print("网点建设标签出现")
        WebDriverWait(self.driver, 10).until(wait02)
        print("等待结束")

        #点击网点建设
        self.driver.find_element(By.XPATH, '//*[@class="slider-wrap"]/ul[1]/li[1]/ul[1]/li[3]').click()
        print("点击网点建设")

        #点击新增网点按钮
        self.driver.find_element(By.XPATH, '//button[@class="el-button addStore el-button--primary"]').click()

        #新增实体网点数据录入
        #选取网点种类为实体
        self.driver.find_element(By.XPATH, '//*[@for="shopSpecies"]/../div//label[1]/span[2]').click()
        #输入网点名称
        self.driver.find_element(By.XPATH, '//*[@for="shopName"]/..//input')\
            .send_keys("自动化新建实体网点01")
        #运营单位选择
        # js_orgId = "$('label[for="'orgId'"]~div input').removeAttr('readonly','autocomplete')"
        # self.driver.execute_script(js_orgId)
        # orgId = self.driver.find_element(By.CSS_SELECTOR, 'label[for="orgId"]~div input')
        # orgId.send_keys("上海国际汽车城新能源汽车运营服务有限公司")
        # self.click_blank = self.driver.find_element(By.CSS_SELECTOR, 'label[for="orgId"]').click()
        self.driver.find_element(By.XPATH, '//*[@for="orgId"]/..//input').click()
        self.driver.find_element(By.CSS_SELECTOR, '[class="el-select-dropdown"]:nth-last-child(1) [class="el-select-dropdown__item"]:nth-child(2)').click()
        #选择省市区
        self.driver.find_element(By.CSS_SELECTOR, 'input[placeholder="省/市"]').click()
        def wait_shengshi(sx):
            return len(self.driver.find_elements(By.CSS_SELECTOR\
                                                 , '[class="el-select-dropdown"]:nth-last-child(1) [class="el-select-dropdown__item"]:nth-child(1)')) >= 1
        WebDriverWait(self.driver, 10).until(wait_shengshi)
        self.driver.find_element(By.CSS_SELECTOR\
                                 , '[class="el-select-dropdown"]:nth-last-child(1) [class="el-select-dropdown__item"]:nth-child(1)').click()

        self.driver.find_element(By.CSS_SELECTOR, 'input[placeholder="市"]').click()
        def wait_shi(s):
            return  len(self.driver.find_elements(By.CSS_SELECTOR\
                                                  , '[class="el-select-dropdown"]:nth-last-child(1) [class="el-select-dropdown__item"]:nth-last-child(1)')) >= 1
        WebDriverWait(self.driver, 10).until(wait_shi)
        self.driver.find_element(By.CSS_SELECTOR\
                                 , '[class="el-select-dropdown"]:nth-last-child(1) [class="el-select-dropdown__item"]:nth-last-child(1)').click()

        self.driver.find_element(By.CSS_SELECTOR, 'input[placeholder="区/县"]').click()
        def wait_quxian(qx):
            return len(self.driver.find_elements(By.CSS_SELECTOR\
                                                 , '[class="el-select-dropdown"]:nth-last-child(1) [class="el-select-dropdown__item"]:nth-last-child(14)')) >= 1
        WebDriverWait(self.driver, 10, ignored_exceptions="没找到区/县").until(wait_quxian)
        self.driver.find_element(By.CSS_SELECTOR\
                                 , '[class="el-select-dropdown"]:nth-last-child(1) [class="el-select-dropdown__item"]:nth-last-child(14)').click()

        #输入网点地址
        self.driver.find_element(By.XPATH, '//*[@for="address"]/..//input').send_keys("自动化新建实体网点01网点地址")

        #输入运营区域
        self.driver.find_element(By.CSS_SELECTOR\
                                , 'label[for=regionid]~[class=el-form-item__content] [class=el-select]').click()
        def wait_area(qy):
            return len(self.driver.find_elements(By.CSS_SELECTOR\
                                                 , '.el-select-dropdown:nth-last-child(1) .el-select-dropdown__item:nth-child(2)')) >= 1
        WebDriverWait(self.driver, 10).until(wait_area)
        self.driver.find_element(By.CSS_SELECTOR\
                                 , '.el-select-dropdown:nth-last-child(1) .el-select-dropdown__item:nth-child(2)').click()

        #输入网点总车位费，分段计费
        # self.driver.switch_to.frame('iframe')

        self.driver.find_element(By.CSS_SELECTOR\
                                 , '[for=chargeType]~[class=el-form-item__content]>label:nth-child(2)>span:nth-child(1)').click()
        js_01 = "$('input[placeholder="'选择日期'"]').eq(2).removeAttr('autocomplete')"
        self.driver.execute_script(js_01)
        time.sleep(1)
        self.driver.find_element(By.CSS_SELECTOR\
                                 , '[class="el-date-editor marLR; el-input el-date-editor--date"] input').send_keys("20190901")
        js = "$('input[placeholder="'选择日期'"]').eq(3).removeAttr('autocomplete')"
        self.driver.execute_script(js)
        self.driver.find_element(By.CSS_SELECTOR\
                                 , '[class="el-date-editor marLR el-input el-date-editor--date"] input').send_keys("2020-12-31")
        self.driver.find_element(By.CSS_SELECTOR\
                                 , 'input[placeholder="租金"]').send_keys(2000)





    def teardown(self):
        time.sleep(5)
        print("测试结束，退出浏览器")
        self.driver.quit()



