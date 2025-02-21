# -*- coding: utf-8 -*-
import sys
from locust import task, tag
from common.apiCommon import commonTask
from utilTools.getConfig import CommonConfig


class checkOrderDetail(commonTask):

    @tag("pageList")
    @task(1)
    def orderPageList(self):
        # 获取请求信息
        url = CommonConfig.get_cf("config", "url", sys._getframe().f_code.co_name)
        header = commonTask.getHeader(self.user.token)
        json_data = self.getApiJson(sys._getframe().f_code.co_name)

        res = self.pypost(url=url, headers=header, json=json_data)

        self.orderid = res.json()['data']['page']['rows'][0]['id']
        print(self.orderid)


    @task
    def fun_interrupt(self):
        self.interrupt()
