# -*- coding: utf-8 -*-
import scrapy

from ejob.items import CatalogItem

class LagouCatalogSpiderSpider(scrapy.Spider):
	name = "lagou_catalog_spider"
	allowed_domains = ["lagou.com"]
	start_urls = ['http://www.lagou.com/']

	def parse(self, response):
		xpath = '//*[@id="sidebar"]//*[@class="menu_box"][.//h2[contains(text(), "金融")]]'
		menu_box = response.xpath(xpath)
		if not menu_box:
			self.logger.error('Menu Element Cannot be found: %s', response.url)
			return None

		menu_main = menu_box.xpath('*[contains(@class, "menu_main")]')
		menu_sub = menu_box.xpath('*[contains(@class, "menu_sub")]')
		if menu_main and menu_sub:
			for link in menu_main.xpath('a'):
				item = LagouCatalogItem()
				item['category'] = '金融'
				item['id'] = link.xpath('@data-lg-tj-no').extract_first()
				item['name'] = link.xpath('text()').extract_first()
				item['url'] = response.urljoin(link.xpath('@href').extract_first())
				yield item
			for dl in menu_sub.xpath('dl'):
				category = dl.xpath('dt/span/text()').extract_first()
				for link in dl.xpath('dd/a'):
					item = CatalogItem()
					item['category'] = category
					item['id'] = link.xpath('@data-lg-tj-no').extract_first()
					item['name'] = link.xpath('text()').extract_first()
					item['url'] = response.urljoin(link.xpath('@href').extract_first())
					yield item
		else:
			self.logger.error('Menu Element Cannot be found: %s', response.url)
			return None
