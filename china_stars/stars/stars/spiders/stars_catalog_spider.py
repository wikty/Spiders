import re, string, json
import scrapy

class StarsSpider(scrapy.Spider):
	name = "stars-catalog-spider"
	start_urls = [
		'http://ent.qq.com/c/dalu_star.shtml',
	]
	stars_capital = [c for c in string.ascii_uppercase]
	stars_capital.append('0-9')

	def start_requests(self):
		for url in self.start_urls:
			request = scrapy.Request(url, callback=self.parse)
			yield request

	def parse(self, response):
		f = open('stars_catalog.json', 'w', encoding='utf-8')
		stars = {}

		for capital in self.stars_capital:
			stars[capital] = []
			count = 1
			while True:
				rowid = capital + ('%d' % count)
				count += 1
				links = response.xpath('//tr[@id="%s"]//a' % rowid)
				if not links:
					break
				else:
					for link in links:
						url = link.xpath('@href').extract_first()
						name = link.xpath('@title').extract_first()
						if url is None:
							self.logger.error('url is empty')
						elif name:
							stars[capital].append({
								'name': name,
								'url': url
							})
		f.write(json.dumps(stars, ensure_ascii=False))