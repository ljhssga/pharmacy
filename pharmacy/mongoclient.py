import pymongo
from scrapy.conf import settings


class MongoClient():
    def __init__(self):
        # 链接数据库
        client = pymongo.MongoClient(host=settings['MONGO_HOST'], port=settings['MONGO_PORT'])
        self.db = client[settings['MONGO_DB']]
        self.coll = self.db[settings['MONGO_COLL']]
        self.ids_seen = set()

    ##查询单个对象
    def find_one(self, query):
        return self.coll.find_one(query)

    ##新增单条记录
    def insert_one(self, data):
        return self.coll.insert_one(data)

    ##新增多条记录
    def find_many(self, **query):
        return self.coll.find(query)

    ##修改数据
    def update(self, query, data):
        data = {'$set': data}
        return self.coll.update_one(query, data)

    ##删除数据
    def delete_one(self,query):
        return self.coll.delete_one(query)
#
# d = MongoClient()
# print(d.find_many().count())