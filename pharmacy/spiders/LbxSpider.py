# -*- coding: utf-8 -*-
import scrapy
import time
from pharmacy.items import PharmacyItem
import requests
import json


##老百姓
class LbxspiderSpider(scrapy.Spider):
    name = 'LbxSpider'
    allowed_domains = ['www.lbxcn.com']
    start_urls = [
        'https://www.lbxcn.com/hepstorefront/lbx/zh/search?text=%E8%8D%AF%E5%93%81&q=%E8%8D%AF%E5%93%81%3Arelevance&page=0']

    def parse(self, response):
        list = response.xpath(
            '//div[@class="ucol_p_img"]//a/@href').extract()
        if list is not None:
            # 当前页
            nowPage = response.xpath('//input[@id="nowPage"]/@value').extract_first()
            # 只有在第一页的时候需要计算总页数
            if nowPage == '0':
                # 总页数
                totalPage = response.xpath('//input[@id="totalPage"]/@value').extract_first()
                for page in range(1, int(totalPage)):
                    url = response.url
                    next_url = url.replace('page=0', 'page=' + str(page))
                    yield response.follow(next_url, callback=self.parse)
            for target in list:
                target = 'https://www.lbxcn.com%s' % (target)
                yield scrapy.Request(url=target, callback=self.parse_item)

    def parse_item(self, response):
        tab = response.xpath('//table[@class="d_m_tab"]//tr//td/text()').extract()
        title = ['通用名', '批准文号', '规格']
        value = {'genericName': '', 'approvalNumber': '', 'specifications': ''}
        for i in range(0, len(title)):
            for t in range(0, len(tab)):
                t_name = tab[t].replace('：', '')
                if title[i] == t_name:
                    v = tab[t + 1]
                    if t_name == '通用名':
                        value['genericName'] = v
                    if t_name == '批准文号':
                        value['approvalNumber'] = v
                    if t_name == '规格':
                        value['specifications'] = v
        goods_name = response.xpath('//h1[@class="pull-left"]/text()').extract_first()
        actualPrice = response.xpath('//div[@class="pull-right pro_iright"]//div[2]//dl//dd//span[1]/text()')\
            .extract_first()
        referencePrice = response.xpath('//div[@class="pull-right pro_iright"]//div[2]//dl//dd//span[3]/text()') \
            .extract_first()
        item = PharmacyItem()
        item['goodsName'] = goods_name
        item['genericName'] = value['genericName']
        item['specifications'] = value['specifications']
        item['approvalNumber'] = value['approvalNumber']
        item['actualPrice'] = actualPrice.replace('￥','')
        item['referencePrice'] = referencePrice.replace('市场价￥','')
        item['url'] = response.url
        item['shopName'] = '老百姓大药房'
        return item
