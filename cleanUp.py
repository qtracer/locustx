# -*- coding: utf-8 -*-
from utilTools.getConfig import CommonConfig
from utilTools.redisUtil import redisDB

# 连接Redis
redis_host = CommonConfig.get_cf("config", "env", "redis_host")
redis_pwd = CommonConfig.get_cf("config", "env", "redis_pwd")
redis_db = CommonConfig.get_cf("config", "env", "redis_db")
db = redisDB(redis_host=redis_host, redis_pwd=redis_pwd, redis_db=redis_db)

db.flush_key("worker")