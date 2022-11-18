# coding=utf-8
"""
author: neowong
"""
import asyncio

from asyncdb.mongo_manager import MongoConsumerManager
from share.ob_log import logger


def start_consumer():
    # 测试发一条mongodb请求
    mgr = MongoConsumerManager()
    mgr.run()


if __name__ == "__main__":
    logger.init(module_name="db", log_dir="logs", log_type="both")
    loop = asyncio.get_event_loop()
    start_consumer()
    loop.run_forever()
