# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class PharmacyItem(scrapy.Item):
    #商品名称
    goodsName = scrapy.Field()
    #通用名称
    genericName = scrapy.Field()
    #厂家名称
    manufacturer = scrapy.Field()
    #规格
    specifications = scrapy.Field()
    #批准文号
    approvalNumber = scrapy.Field()
    #实际价格
    actualPrice = scrapy.Field()
    #参考价
    referencePrice = scrapy.Field()
    #地址
    url = scrapy.Field()
    #药店名称
    shopName = scrapy.Field()
