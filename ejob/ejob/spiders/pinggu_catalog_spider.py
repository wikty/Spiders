# -*- coding: utf-8 -*-
import scrapy


class PingguCatalogSpiderSpider(scrapy.Spider):
	name = "pinggu_catalog_spider"
	allowed_domains = ["pinggu.org"]
	start_urls = ['http://bbs.pinggu.org/z_rc.php']

	def parse(self, response):
		pass
