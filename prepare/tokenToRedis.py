# -*- coding: utf-8 -*-

import concurrent.futures
import csv
import os, platform
import sys
import threading

import requests

if platform.system() == "Windows":
    sys.path[0] = os.path.dirname(os.path.dirname(__file__))
else:
    sys.path[0] = os.path.dirname(os.getcwd())
print("sys.path[0] is", sys.path[0])
from utilTools.getConfig import CommonConfig
from utilTools.redisUtil import redisDB
from common import dataHandle

'''
连接redis
'''
redis_host = CommonConfig.get_cf("config", "env", "redis_host")
redis_pwd = CommonConfig.get_cf("config", "env", "redis_pwd")
redis_db = CommonConfig.get_cf("config", "env", "redis_db")
db = redisDB(redis_host=redis_host, redis_pwd=redis_pwd, redis_db=redis_db)

# 生成token并set到Redis里面去
def pushToRedis(row):
    _Account = row[0]
    _Password = row[1]
    setTokenToRedis(_Account, _Password)


# 生成token
def setTokenToRedis(account, password):
    host = CommonConfig.get_cf("config", "env", "host")
    uri = CommonConfig.get_cf('config', 'order_url', 'bslogin')
    params = {
        'email': account,
        'password': password,
        'verifyCode': 'skip',
        'accessCode': 'autologin'
    }
    # 请求登录接口
    res = requests.post(url=host + uri,  params=params, verify=False)
    print(res.cookies)
    # 设置accesstoken到Redis
    db.set(service="account", key=account, value=res.json()['data']['accessToken'])


if __name__ == '__main__':
    dir = sys.path[0]
    reader = dataHandle.getCSVObject('account_pwd')
    threadMaxWorkers = int(CommonConfig.get_cf("config", "setting", "threadMaxWorkers"))

    with concurrent.futures.ThreadPoolExecutor \
                        (max_workers=threadMaxWorkers) as executor:
        executor.map(pushToRedis, [row for row in reader])


