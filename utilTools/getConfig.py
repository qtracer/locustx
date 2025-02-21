# -*- coding:utf-8 -*-
import configparser
import os

cf = configparser.ConfigParser()
cfConfig = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config/config.ini")

class CommonConfig(object):

    @staticmethod
    def get_cf(role, section, key):
        if role == "config":
            cf.read(cfConfig, encoding="utf-8")
            value = cf.get(section, key)
            return value

    @staticmethod
    def set_cf(section, key, value):
        cf.read(cfConfig, encoding="utf-8")
        if not cf.has_section(section):
            cf.add_section(section)
        cf.set(section, key, value)
        with open(cfConfig, 'w') as configfile:
            cf.write(configfile)


if __name__ == "__main__":
    print(CommonConfig.get_cf("config", "env", "host"))

