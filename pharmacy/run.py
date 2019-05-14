import scrapy
from scrapy.crawler import CrawlerProcess
from pharmacy.spiders.XszkSpider import XszkspiderSpider
from pharmacy.spiders.YywSpider import YywSpider
from pharmacy.spiders.LbxSpider import LbxspiderSpider

process = CrawlerProcess()  # 括号中可以添加参数
process.crawl(LbxspiderSpider)
process.start()
