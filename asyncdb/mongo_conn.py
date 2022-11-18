# coding=utf-8
"""
author: neowong
"""

import pymongo
from pymongo import database, collection


class MongoConn(object):

    def __init__(self, url):
        self.client = pymongo.MongoClient(url)

    def get_db(self, db_name: str) -> database.Database:
        return self.client[db_name]

    def get_collection(self, db_name: str, coll_name: str) \
            -> collection.Collection:
        return self.client[db_name][coll_name]
