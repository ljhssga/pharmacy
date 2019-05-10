# -*- coding: utf-8 -*-
import scrapy
from pharmacy.items import PharmacyItem

##先声再康
class XszkspiderSpider(scrapy.Spider):
    name = 'XszkSpider'
    allowed_domains = ['www.zk100.com']
    start_urls = ['http://www.zk100.com/list/kw-_page-1.htm']

    def parse(self, response):
        list = response.xpath('//div[@class="product_list"]//dl//dt//a/@href').extract()
        next_url = response.xpath('//a[@class="pro_pagedown"]/@href').extract_first()
        if next_url:
            url = 'http://www.zk100.com/%s' % (next_url)
            yield response.follow(url, callback=self.parse)
        for target in list:
            yield scrapy.Request(target, callback=self.parse_detail)

    def parse_detail(self, response):

        goods_name = response.xpath('//div[@class="detail_title"]//h2/text()').extract_first()
        generic_name = response.xpath('//div[@class="detail_cf"]//dl[1]//dd/text()').extract_first()
        manufacturer = response.xpath('//div[@class="detail_cf"]//dl[2]//dd/text()').extract_first()
        specifications = response.xpath('//div[@class="detail_cf"]//dl[3]//dd/text()').extract_first()
        approval_number = response.xpath('//div[@class="detail_cf"]//dl[4]//dd/text()').extract_first()
        actual_price = response.xpath('//dl[@id="otc_sales"]//dd//span/text()').extract_first()
        reference_price = response.xpath('//dl[@id="otc_mkt"]//dd//b/text()').extract_first()
        item = PharmacyItem()
        item['goodsName'] = goods_name
        item['genericName'] = generic_name
        item['manufacturer'] = manufacturer
        item['specifications'] = specifications
        item['approvalNumber'] = approval_number
        item['actualPrice'] = actual_price.replace('￥','')
        item['referencePrice'] = reference_price.replace('￥','')
        item['url'] = response.url
        item['shopName'] = '先声再康'
        return item