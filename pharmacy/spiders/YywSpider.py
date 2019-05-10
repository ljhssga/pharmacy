# -*- coding: utf-8 -*-
import scrapy
from pharmacy.items import PharmacyItem


##1药网
class YywspiderSpider(scrapy.Spider):
    name = 'YywSpider'
    allowed_domains = ['www.111.com.cn']
    start_urls = ['https://www.111.com.cn/categories/953710-j1.html']

    def parse(self, response):
        list = response.xpath('//div[@class="itemSearchResultCon"]//a[@class="product_pic pro_img"]/@href').extract_first()
        # next_url = response.xpath('//a[@class="next"]/@href').extract_first()
        # if next_url:
        #     yield response.follow(next_url, callback=self.parse)
        # for target in list:
        target = 'https://' + list.replace('//', "")
        yield scrapy.Request(url=target, callback=self.parse_item)

    def parse_item(self, response):
        goods_name = response.xpath('//div[@class="goods_intro"]//table//tr[1]//td/text()').extract_first()
        generic_name = response.xpath('//div[@class="goods_intro"]//table//tr[2]//td[1]/text()').extract_first()
        manufacturer = response.xpath('//div[@class="goods_intro"]//table//tr[3]//td[2]/text()').extract_first()
        specifications = response.xpath('//div[@class="goods_intro"]//table//tr[2]//td[2]/text()').extract_first()
        approval_number = response.xpath('//div[@class="goods_intro"]//table//tr[4]//td[1]/text()').extract_first()
        # actual_price = response.xpath('//span[@class="good_price"]/text()').extract_first()
        # item = PharmacyItem()
        # item['goodsName'] = goods_name
        # item['genericName'] = generic_name
        # item['manufacturer'] = manufacturer
        # item['specifications'] = specifications
        # item['approvalNumber'] = approval_number.replace(' ','').replace('(','')
        # item['actualPrice'] = actual_price.replace('￥', '')
        # # item['referencePrice'] = reference_price.replace('￥', '')
        # item['url'] = response.url
        # item['shopName'] = '1药网'
        # return item
