# coding=utf-8
"""
author: neowong
"""
import os
from asyncdb.mongo_conn import MongoConn
from asyncdb.base import BaseConsumer, RegisterConsumer


@RegisterConsumer("buy")
class Buy(BaseConsumer):
    """
    买入操作表
    数据设计结构:
    "id": 76758572518,
    "symbol": "eosusdt",
    "account-id": 12593019,
    "client-order-id": "",
    "amount": "10.000000000000000000",
    "price": "1.500000000000000000",
    "created-at": 1585030041975,
    "type": "buy-limit",
    "field-amount": "0.0",
    "field-cash-amount": "0.0",
    "field-fees": "0.0",
    "finished-at": 0,
    "source": "spot-api",
    "state": "submitted",
    "canceled-at": 0,
    "has_sold": 0|1      // 是否已卖
    """
    _instance = None
    _database_name = "currency"
    _table_name = "buy"

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = Buy()
        return cls._instance

    def __init__(self):
        super(Buy, self).__init__(self._table_name)
        url = os.environ.get('MONGO_URL')
        self.conn = MongoConn(url).get_collection(Buy._database_name, Buy._table_name)

    async def execute(self, *args, **kwargs):
        pass

    def insert(self, **kwargs):
        """
        :return:
        """
        print("收到db插入请求:", kwargs)
        # data.update({"has_sold": 0})
        ret = self.conn.insert_one(kwargs)
        # logger.info("insert to mongo: {}".format(data))
        return str(ret.inserted_id)

    def get_by_id(self, **kwargs):
        """
        获取指定的订单信息
        """
        print("收到查询请求:", kwargs)
        order_id = kwargs.get("order_id")
        ret = self.conn.find_one({"order_id": order_id}, projection={"_id": False})
        return ret

    def get_unfinished_orders(self, **kwargs):
        ret = self.conn.find({"has_sold": 0})
        return ret


if __name__ == "__main__":
    pass
    # Buy.get_instance().insert("nawHtSjCK8MC77fVb1n3h8xPI08jji1A", "201809/20/1.txt", 1538048261,
    #                                         1538048261, "tencent")
