# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
from pharmacy.mongoclient import MongoClient


class MongoPipeline(object):

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        if item['goodsName'] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            client = MongoClient()
            goodsName = item['goodsName']
            self.ids_seen.add(goodsName)
            query = {'goodsName': goodsName}
            drug = client.find_one(query)
            if drug is not None:
                if drug['goodsName'] == item['goodsName']:
                    print('---数据已存在，查看当前数据价格是否变更---')
                    if drug['actualPrice'] == item['actualPrice']:
                        print('----当前价格数据未变更---')
                    else:
                        print('-----当前价格数据已变更，数据更新')
                        client.update(query=query,data=dict(item))
                else:
                    print('----数据不存在，入库----')
                    client.insert_one(dict(item))
            else:
                print('----数据不存在，入库----')
                client.insert_one(dict(item))
        return 'success'