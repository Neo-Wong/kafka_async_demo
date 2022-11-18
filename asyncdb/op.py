# coding=utf-8
"""
author: neowong
desc: 将MongoDB操作通过kafka封装起来
"""
import os
import asyncio
import json
import traceback
from typing import Callable, Dict, List, Any

from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import kafka_errors
from share.singleton import Singleton


class KafkaOp(object, metaclass=Singleton):

    def __init__(self):
        self.url = os.environ.get('KAFKA_URL')
        self.producer = KafkaProducer(
            bootstrap_servers=[self.url],
            key_serializer=lambda k: json.dumps(k).encode(),
            value_serializer=lambda v: json.dumps(v).encode())

    def send_msg(self, topic: str, key: str, msg: str):
        future = self.producer.send(topic, key=key, value=msg)
        try:
            future.get(timeout=10)
        except kafka_errors:
            traceback.format_exc()

    def receive_msg(self, topic: str, num: int, group_id: str = "") \
            -> List[Dict]:
        consumer = KafkaConsumer(topic, bootstrap_servers=self.url,
                                 group_id=group_id)
        ret: list = [Dict]
        t = 0
        for msg in consumer:
            if t >= num:
                break
            ret.append({
                "key": json.loads(msg.key.decode()),
                "value": json.loads(msg.value.decode())})
            t += 1
        return ret

    async def receive_msg_with_callback(self, topic: str,
                                  cb: Callable[[Any, Dict[str, Any]], int],
                                  group_id: str = "aa"):
        consumer = KafkaConsumer(topic, bootstrap_servers=self.url,
                                 group_id=group_id)
        for msg in consumer:
            try:
                cb(topic, {
                    "key": json.loads(msg.key.decode()),
                    "value": json.loads(msg.value.decode())
                })
            except Exception:
                print(traceback.format_exc())
                pass
            await asyncio.sleep(0)
