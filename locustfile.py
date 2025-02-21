# -*- coding: utf-8 -*-
import concurrent.futures
import os
import sys
import time

from locust.runners import WorkerRunner

sys.path[0] = os.path.dirname(__file__)

from common import dataHandle
from utilTools.redisUtil import redisDB
from locustService import order_checkOrderDetail, order_mainflow
from utilTools.getConfig import CommonConfig
from locust import HttpUser, events

# 被施压域名
host = CommonConfig.get_cf("config", "env", "host")

# 连接Redis
redis_host = CommonConfig.get_cf("config", "env", "redis_host")
redis_pwd = CommonConfig.get_cf("config", "env", "redis_pwd")
redis_db = CommonConfig.get_cf("config", "env", "redis_db")
db = redisDB(redis_host=redis_host, redis_pwd=redis_pwd, redis_db=redis_db)

# 初始化用户计数器
lenForAccount = 0
cForAccount = 0
listForAccount = []
worker_id = 0
cWorker = 0


"""
性能测试统一执行类
"""
class User(HttpUser):
    host = host
    tasks = {
        order_checkOrderDetail.checkOrderDetail: 1,
        order_mainflow.orderMainflow: 1
    }

    ''' 每启动一个用户，就会执行一次 '''
    def on_start(self):
        print("+++++++++++++on_start++++++++++++")
        global cForAccount, lenForAccount, listForAccount
        account = listForAccount[cForAccount if cForAccount < lenForAccount else cForAccount % lenForAccount]
        cForAccount += 1
        self.token = db.get(service="account", key=account)


@events.init.add_listener
def on_locust_init(environment, **_kwargs):
    print("+++++++++++++on_locust_init++++++++++++")
    if not isinstance(environment.runner, WorkerRunner):
        '''
            locust-master启动时&服务还没准备好进行初始化
        '''
        # db.flush_key("worker*")  # 压测前清理。可以在压测结束后自动清理

        global listForAccount
        listForAccount = []

        reader = dataHandle.getCSVObject('account_pwd')
        threadMaxWorkers = int(CommonConfig.get_cf("config", "setting", "threadMaxWorkers"))

        with concurrent.futures.ThreadPoolExecutor \
                    (max_workers=threadMaxWorkers) as executor:
            executor.map(accountToList, [row[0] for row in reader])
        initCounter()
    else:
        time.sleep(5)
        global worker_id

        db.set(service="worker", key=str(environment.runner), value=str(environment.runner))
        worker_id = db.get_key_account("worker*")
        db.close()


@events.init.add_listener
def on_test_start(environment, **_kwargs):
    print("+++++++++++++on_test_start++++++++++++")
    time.sleep(2)
    if isinstance(environment.runner, WorkerRunner):
        global listForAccount, lenForAccount
        worker_count = db.get_key_account("worker*")
        account_reader = dataHandle.getCSVObject('account_pwd')
        print("worker_id is: ", worker_id)
        print("worker_count is: ", worker_count)
        listForAccount = [i[0] for i in account_reader][worker_id-1::worker_count]
        lenForAccount = len(listForAccount)


def initCounter():
    global lenForAccount, cForAccount
    lenForAccount = db.get_key_account("account")
    cForAccount = 0


def accountToList(i):
    listForAccount.append(i)


if __name__ == '__main__':
    print(CommonConfig.get_cf("config", "env", "host"))