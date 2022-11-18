# coding=utf-8
"""
author: neowong
"""
import asyncio
from typing import Dict

from asyncdb.controller import DbController
from share.ob_log import logger


async def send_insert(ctl: DbController) -> Dict:
    print("开始发送插入请求（会自动通过kafka中转）")
    ret = await ctl.send_msg(
        table_name="buy",
        func_name="insert",
        order_id="huobi_1")
    print("收到返回的插入结果：", ret)


async def send_query(ctl: DbController) -> Dict:
    print("开始发送查询请求（会自动通过kafka中转）")
    ret = await ctl.send_msg(
        table_name="buy",
        func_name="get_by_id",
        order_id="huobi_1")
    print("收到返回的查询结果：", ret)


async def send_mongo_msg():
    # 测试发一条mongodb请求
    ctl = DbController()
    asyncio.ensure_future(ctl.run())
    await send_insert(ctl)
    await send_query(ctl)


if __name__ == "__main__":
    logger.init(module_name="caller", log_dir="logs", log_type="both")
    loop = asyncio.get_event_loop()
    asyncio.run_coroutine_threadsafe(send_mongo_msg(), loop)
    loop.run_forever()
