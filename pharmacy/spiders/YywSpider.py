# -*- coding: utf-8 -*-
import scrapy
import time
from pharmacy.items import PharmacyItem
import requests
import json


##1药网
class YywSpider(scrapy.Spider):

    def __init__(self):
        self.header = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

    name = 'YywSpider'
    allowed_domains = ['www.111.com.cn']
    start_urls = ['https://www.111.com.cn/categories/953710-j1.html']

    def parse(self, response):
        list = response.xpath(
            '//div[@class="itemSearchResultCon"]//a[@class="product_pic pro_img"]/@href').extract()
        next_url = response.xpath('//a[@class="next"]/@href').extract_first()
        if next_url:
            yield response.follow(next_url, callback=self.parse)
        for target in list:
            target = 'https://' + target.replace('//', "")
            yield scrapy.Request(url=target, callback=self.parse_item)

    def parse_item(self, response):
        goods_name = response.xpath('//div[@class="goods_intro"]//table//tr[1]//td/text()').extract_first()
        generic_name = response.xpath('//div[@class="goods_intro"]//table//tr[2]//td[1]/text()').extract_first()
        manufacturer = response.xpath('//div[@class="goods_intro"]//table//tr[3]//td[2]/text()').extract_first()
        specifications = response.xpath('//div[@class="goods_intro"]//table//tr[2]//td[2]/text()').extract_first()
        approval_number = response.xpath('//div[@class="goods_intro"]//table//tr[4]//td[1]/text()').extract_first()
        iid = response.xpath('//div[@class="evaluate_mian"]/@iid').extract_first()
        _t = int(round(time.time() * 1000))
        comboInfoUrl = 'https://www.111.com.cn/items/getComboInfo.action?id=%s&_=%s' % (iid, _t)
        r = requests.get(url=comboInfoUrl, headers=self.header)
        if r is not None:
            r_data = json.loads(r.text)
            actual_price = r_data[0]['originalPrice']
            reference_price = r_data[0]['recommendPrice']
            item = PharmacyItem()
            item['goodsName'] = goods_name
            item['genericName'] = generic_name
            item['manufacturer'] = manufacturer
            item['specifications'] = specifications
            item['approvalNumber'] = approval_number.replace(' ','').replace('(','').replace('\n','')
            item['actualPrice'] = actual_price
            item['referencePrice'] = reference_price
            item['url'] = response.url
            item['shopName'] = '1药网'
            return item