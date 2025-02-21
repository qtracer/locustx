# -*- coding: utf-8 -*-

import json
import random
import sys

import requests
from locust import task, tag

from common import dataHandle
from common.apiCommon import commonTask
from utilTools.getConfig import CommonConfig

class orderMainflow(commonTask):

    @task
    def fun_interrupt(self):
        self.interrupt()
