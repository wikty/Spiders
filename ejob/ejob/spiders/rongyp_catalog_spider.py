# -*- coding: utf-8 -*-
import scrapy

from ejob.items import CatalogItem

class RongypCatalogSpiderSpider(scrapy.Spider):
	name = "rongyp_catalog_spider"
	allowed_domains = ["rongyp.com"]
	start_urls = ['https://www.rongyp.com/index.php?m=Home&c=Job&a=jobSearch']

	def start_requests(self):
		for url in self.start_urls:
			request = scrapy.Request(url, callback=self.parse)
			request.meta['dont_redirect'] = True
			yield request

	def parse(self, response):
		for li in response.xpath('//ul[@id="tabBox"]/li'):
			category = li.xpath('.//h2/text()').extract_first()
			for link in li.xpath('.//dl/dd/a'):
				item = CatalogItem()
				name = link.xpath('text()').extract_first()
				url = link.xpath('@href').extract_first()
				if (not url) or (not name) or (name == '其它'):
					continue
				item['id'] = ''
				item['category'] = category
				item['name'] = name
				item['url'] = response.urljoin(url)
				yield item