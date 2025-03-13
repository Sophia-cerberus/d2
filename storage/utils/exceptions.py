#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @Time        :2021/08/11 11:14
# @Author      :周宇
# @Email       :zhouyu_a@cyou-inc.com
# @Version     :v1.0
# @File        :exceptions.py
# @Desc        :

# (C)Copyright 2019-2020, Beijing AmazGame Age Internet Technology Co.,Ltd.


import logging
import traceback

from rest_framework.views import set_rollback

from utils.response import ErrorResponse

logger = logging.getLogger(__name__)

from rest_framework.exceptions import APIException as DRFAPIException
from rest_framework.exceptions import NotAuthenticated


class APIException(Exception):
    """
    通用异常:(1)用于接口请求是抛出移除, 此时code会被当做标准返回的code, message会被当做标准返回的msg
    """

    def __init__(self, code=400, message='API异常', args=('API异常',)):
        self.args = args
        self.code = code
        self.message = message

    def __str__(self):
        return self.message


def op_exception_handler(ex, context):
    """
    统一异常拦截处理
    目的:(1)取消所有的500异常响应,统一响应为标准错误返回
        (2)准确显示错误信息
    :param ex:
    :param context:
    :return:
    """
    msg = ''
    code = 400
    if isinstance(ex, DRFAPIException):
        set_rollback()
        msg = ex.detail
    elif isinstance(ex, APIException):
        set_rollback()
        msg = str(ex)
    elif isinstance(ex, Exception):
        logger.error(traceback.format_exc())
        msg = str(ex)
    return ErrorResponse(msg=msg, code=code)
