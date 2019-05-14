# -*- coding: utf-8 -*-
import scrapy
import time
from pharmacy.items import PharmacyItem
import requests
import json


##康爱多
class KadSpider(scrapy.Spider):

    def __init__(self):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
            'Referer': 'http://www.360kad.com/',
            'Host': 'www.360kad.com'
        }
    def __asdasdasd__(self):
        print(1)


    name = 'KadSpider'
    allowed_domains = ['www.360kad.com']
    # start_urls = ['http://www.360kad.com/Category_122/Index.aspx']

    start_urls = ['http://www.360kad.com/Category_122/Index.aspx','http://www.360kad.com/Category_756/Index.aspx','http://www.360kad.com/Category_15531531/Index.aspx','http://search.360kad.com/?type=1&pageText=%E8%82%9D%E8%83%86%E7%A7%91%E4%B8%93%E7%A7%91%E7%94%A8%E8%8D%AF',
                  'http://search.360kad.com/?pageText=%E7%94%B7%E6%80%A7%E4%B8%93%E7%A7%91%E7%94%A8%E8%8D%AF','http://search.360kad.com/?pageText=%E7%9A%AE%E8%82%A4%E7%A7%91%E4%B8%93%E7%A7%91%E7%94%A8%E8%8D%AF','http://search.360kad.com/?pageText=%E8%82%BF%E7%98%A4%E7%A7%91%E4%B8%93%E7%A7%91%E7%94%A8%E8%8D%AF',
                  'http://search.360kad.com/?pageText=%E7%A5%9E%E7%BB%8F%E7%A7%91%E4%B8%93%E7%A7%91%E7%94%A8%E8%8D%AF','http://search.360kad.com/?pageText=%E6%B6%88%E5%8C%96%E7%B3%BB%E7%BB%9F1','http://search.360kad.com/?pageText=%E5%91%BC%E5%90%B8%E7%B3%BB%E7%BB%9FZ',
                  'http://search.360kad.com/?pageText=%E5%BF%83%E8%84%91%E7%A7%91X','http://search.360kad.com/?pageText=%E9%A3%8E%E6%B9%BFb','http://search.360kad.com/?pageText=%E6%B3%8C%E5%B0%BF%E4%B8%93%E7%A7%91%E7%94%A8%E8%8D%AF','http://search.360kad.com/?pageText=%E5%BF%83%E7%90%86%E7%A7%91%E4%B8%93%E7%A7%91%E7%94%A8%E8%8D%AF',
                  'http://search.360kad.com/?pageText=%E5%86%85%E5%88%86%E6%B3%8C%E7%A7%91N']

    def start_requests(self):
        for url in self.start_urls:
            if url.find('search') >= 0:
                self.headers['Host'] = 'search.360kad.com'
            else:
                self.headers['Host'] = 'www.360kad.com'
            yield scrapy.Request(url, headers=self.headers)

    def parse(self, response):
        current_url = response.url
        list = response.xpath(
            '//ul[@id="YproductList"]//li//div//p//a/@href').extract()
        if len(list) == 0:
            list = response.xpath(
                '//div[@class="plist_li_i"]//p//a/@href').extract()
        next_url = response.xpath('//a[@class="Ynext"]/@href').extract_first()
        if next_url:
            url = 'http://www.360kad.com/%s' % (next_url)
            if response.url.find('search') >= 0:
                url = 'http://search.360kad.com%s' % (next_url)
            if current_url.find('search') >= 0:
                self.headers['Host'] = 'search.360kad.com'
            else:
                self.headers['Host'] = 'www.360kad.com'
            yield scrapy.Request(url, callback=self.parse, headers=self.headers)
        for target in list:
            if url.find('search') < 0:
                target = "http://www.360kad.com%s" % (target)
            self.headers['Referer'] = current_url
            self.headers['Host'] = 'www.360kad.com'
            yield scrapy.Request(url=target, callback=self.parse_item, headers=self.headers)

    def parse_item(self, response):
        detail_text = response.xpath('//div[@id="wrap990list1"]//ul//li/text()').extract()
        title = ['商品名称：', '规格：', '生产企业：', '通用名称：', '批准文号：']
        value = {'商品名称': '', '规格': '', '生产企业': '', '通用名称': '', '批准文号': ''}
        for t in title:
            for detail in detail_text:
                if detail.find(t) >= 0:
                    value['%s' % (t.replace('：', ''))] = detail.replace(t, '')
        product_id = response.xpath("//input[@id='form_wareskucode']/@value").extract_first()
        price_url = 'http://www.360kad.com/product/getprice?wareskucode=%s&quantity=1' % (product_id)
        price_headers = self.headers
        price_headers['Referer'] = response.url
        r = requests.get(url=price_url, headers=price_headers)
        if r is not None:
            r_data = json.loads(r.text)
            actual_price = r_data['StyleInfo']['Price']
            reference_price = r_data['StyleInfo']['OrigPrice']
            item = PharmacyItem()
            item['goodsName'] = value['商品名称'] if '商品名称' in value else ''
            item['genericName'] = value['通用名称'] if '通用名称' in value else ''
            item['manufacturer'] = value['生产企业'] if '生产企业' in value else ''
            item['specifications'] = value['规格'] if '规格' in value else ''
            item['approvalNumber'] = value['批准文号'] if '批准文号' in value else ''
            item['actualPrice'] = actual_price
            item['referencePrice'] = reference_price
            item['url'] = response.url
            item['shopName'] = '康爱多'
            return item
