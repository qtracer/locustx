# -*- coding: utf-8 -*-

import redis
from utilTools.getConfig import CommonConfig

class redisDB(object):
    def __init__(self, is_master=False, redis_host="127.0.0.1", redis_port="6379", redis_pwd=None, redis_db = 0):
        self.pool = redis.ConnectionPool(host=redis_host,
                                        port=redis_port,
                                        db=redis_db,
                                        password=redis_pwd)
        self.conn = redis.StrictRedis(connection_pool=self.pool)

    def set(self, service, key, value=None):
        self.conn.set(name=service + ":" + key, value=value)

    def get(self, service, key):
        data = str(self.conn.get(service + ":" + key), encoding="utf-8")
        return data

    def getD(self, service, key):
        data = eval(str(self.conn.get(service + ":" + key), encoding="utf-8"))
        return data

    def get_key_account(self, service=None):
        # return len(self.conn.scan(match=service+'*'))
        count = 0
        cursor = 0
        while True:
            cursor, keys = self.conn.scan(cursor=cursor, match=service+'*')
            count += len(keys)
            if cursor == 0:
                break
        return count


    def flush_key(self, service):
        for key in self.conn.scan_iter(match=service+'*'):
            self.conn.delete(key)

    def close(self):
        self.conn.close()

if __name__ == '__main__':
    redis_host = CommonConfig.get_cf("config", "env", "redis_host")
    redis_pwd = CommonConfig.get_cf("config", "env", "redis_pwd")
    redis_db = CommonConfig.get_cf("config", "env", "redis_db")
    db = redisDB(redis_host=redis_host, redis_pwd=redis_pwd, redis_db=redis_db)

