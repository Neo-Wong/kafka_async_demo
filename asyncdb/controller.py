# coding=utf-8
"""
author: neowong
"""
import asyncio
import json
import uuid
from asyncio import Future
from typing import Dict

from asyncdb.op import KafkaOp
from share.ob_log import logger
from share.singleton import Singleton


class DbController(object, metaclass=Singleton):

    def __init__(self):
        self.future_dict: Dict[str, Future] = {}
        self.kafka_cli = KafkaOp()
        self.loop = asyncio.get_running_loop()
        self.proc_topic = "test_1"   # 每个进程自己一个独立的topic
        self.group_id = "cc"

    async def run(self):
        await self.kafka_cli.receive_msg_with_callback(
            self.proc_topic, self.callback, self.group_id)

    def callback(self, topic: str, params: Dict[str, str]) -> int:
        try:
            future_id = params["key"]
            ret = params["value"]
            if future_id in self.future_dict:
                self.future_dict[future_id].set_result(ret)
                del self.future_dict[future_id]
            else:
                logger.error("[future missed][future_id=%s][ret=%s]",
                             future_id, ret)
        except Exception:
            pass
        return 1

    async def send_msg(self, table_name: str, func_name: str,
                       **kwargs) -> Dict:
        future_id: str = uuid.uuid1().hex
        wait_future: Future = self.loop.create_future()
        kwargs["future_id"] = future_id
        kwargs["reply_topic"] = self.proc_topic
        self.kafka_cli.send_msg(topic=table_name, key=func_name,
                                msg=kwargs)
        self.future_dict[future_id] = wait_future
        ret = await wait_future
        return ret
