import re, string, json, urllib
import scrapy
from stars.items import StarInfoItem

class StarsSpider(scrapy.Spider):
	name = "stars-spider"
	start_urls = [
		'http://ent.qq.com/c/dalu_star.shtml',
	]
	stars_capital = [c for c in string.ascii_uppercase]
	stars_capital.append('0-9')
	starinfo_fields = {
		'name':'姓名', 
		'another_name':'原名', 
		'gender':'性别', 
		'english_name':'英文名', 
		'birthyear':'出生年', 
		'birthday':'生日', 
		'constellation':'星座', 
		'nationality':'国籍', 
		'area':'地域', 
		'profession':'职业', 
		'height':'身高', 
		'bloodtype':'血型'
	}
	starinfo_url = 'http://datalib.ent.qq.com/star/%d/starinfo.shtml'

	def start_requests(self):
		for url in self.start_urls:
			request = scrapy.Request(url, callback=self.parse)
			yield request

	def parse(self, response):
		for capital in self.stars_capital:
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
							request = scrapy.Request(url, callback=self.parse_star)
							request.meta['capital'] = capital
							request.meta['name'] = name
							request.meta['id'] = int(url.split('/')[-2])
							yield request

	def parse_star(self, response):
		starinfo = StarInfoItem()
		starinfo['starid'] = response.meta['id']
		starinfo['capital'] = response.meta['capital']
		starinfo['name'] = response.meta['name']
		starinfo['url'] = response.url
		avatar_url = response.xpath('//div[@id="star_face"]/a/img/@src').extract_first(default='')
		starinfo['avatar'] = avatar_url
		starinfo['album'] = []
		image_urls = [avatar_url]
		count = 1
		while True:
			imgs = response.xpath('//*[@id="demo%d"]//img/@src' % count).extract()
			count += 1
			if not imgs:
				break
			else:
				image_urls += imgs
		starinfo['image_urls'] = image_urls
		
		xpath = '//div[@id="infos"]//td[strong[contains(text(), "{field}")]]/text()'
		for k, field in self.starinfo_fields.items():
			value = response.xpath(xpath.format(field=field)).extract_first()
			if value:
				starinfo[k] = value.strip()
			else:
				starinfo[k] = ''

		starinfo_url = self.starinfo_url % starinfo['starid']
		body = urllib.request.urlopen(starinfo_url).read().decode('gbk').encode('utf-8').decode('utf-8')
		r = response.replace(body=body)
		xpath = '//div[@id="left"]/table[2]//td[@class="line22"]/text()'
		starinfo['brief'] = r.xpath(xpath).extract_first('').strip()

		yield starinfo