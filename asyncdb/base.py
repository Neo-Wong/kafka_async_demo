# coding=utf-8
"""
author: neowong
"""
from typing import Dict, Callable


class BaseConsumer(object):
    """
    基础处理类
    """

    def __init__(self, col_name: str):
        """

        :param col_name: dict
        """
        self.col_name = col_name

    async def execute(self, *args, **kwargs):
        raise NotImplementedError


class RegisterConsumer(object):
    """
    事件管理器，将命令码与handler进行绑定
    """
    events: Dict[str, BaseConsumer] = dict()

    def __init__(self, col_name):
        self.col_name = col_name

    def __call__(self, consumer):
        self.events[self.col_name] = consumer
        return consumer
