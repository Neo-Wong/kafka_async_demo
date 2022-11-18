# coding=utf-8
"""
author: neowong
"""
import asyncio
import json
from typing import Dict, Union

from asyncdb.base import RegisterConsumer
from asyncdb.op import KafkaOp
from share.ob_log import logger
from share.singleton import Singleton


class MongoConsumerManager(object, metaclass=Singleton):

    def __init__(self):
        self.kafka_cli = KafkaOp()

    def run(self):
        for topic in RegisterConsumer.events.keys():
            asyncio.ensure_future(self.kafka_cli.receive_msg_with_callback(
                topic, cb=self.callback_from_kafka))

    def callback_from_kafka(self, topic: str, params: Dict[str, Union[str, dict]]) -> int:
        consumer = RegisterConsumer.events[topic]
        func_name = params["key"]
        value = params["value"]
        reply_topic = value.get("reply_topic", None)
        future_id = value.get("future_id", None)

        print(func_name, reply_topic, future_id)
        if not func_name or not getattr(consumer, func_name) \
                or not reply_topic or not future_id:
            logger.error("[callback_from_kafka][topic=%s][params=%s]",
                         topic, value)
            return 0
        ret = getattr(consumer(), func_name)(**value)
        print("db请求执行结果:", ret)
        self.kafka_cli.send_msg(reply_topic, future_id, json.dumps(ret))
        return 1
