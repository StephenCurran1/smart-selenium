"""Constants that are not managed by devops"""
# -*- coding: utf-8 -*-
import os
LOG_FORMAT = "%(asctime)s %(name)s@{}s [%(process)d] %(levelname)-8s %(message)s [in %(pathname)s:%(funcName)s:%(lineno)d]".format(os.getenv('HOSTNAME'))
LOG_DATE_FORMAT = '%m-%d %H:%M'



DEV_FLAG = 'DEV'
DEV_MQ_SLEEP = 30 # seconds

PROD_FLAG = 'PROD'

