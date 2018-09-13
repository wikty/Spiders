# -*- coding: utf-8 -*-
import os, json
from urllib.parse import quote
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from ejob.items import JobItem
from ejob.item_loaders import LagouJobItemLoader


class LagouJobSpiderSpider(CrawlSpider):
	name = "lagou_job_spider"
	allowed_domains = ["lagou.com"]
	start_urls = ['https://www.lagou.com/']
	urls = []
	rules = [
		Rule(LinkExtractor(allow=('/zhaopin/[^/]+/\d+/$', ), restrict_xpaths=('//*[@class="pager_container"]', )), process_request='preprocess_request', follow=True),
		Rule(LinkExtractor(allow=('/jobs/\d+\.html$', ), restrict_xpaths=('//*[@id="s_position_list"]')), callback='parse_job')
	]
	query_str = '&'.join(['{}'.format(quote('city=全国'))])

	def __init__(self, urlfile, *args, **kwargs):
		# scrapy crawl myspider -a category=electronics
		super(LagouJobSpiderSpider, self).__init__(*args, **kwargs)
		with open(urlfile, 'r', encoding='utf8') as f:
			for line in f:
				line = line.strip()
				if not line:
					continue
				item = json.loads(line)
				self.urls.append((item['name'], item['url'], item['id']))

	def start_requests(self):
		for category_name, category_url, category_id in self.urls:
			category_url = '?'.join([category_url, self.query_str])
			request = scrapy.Request(category_url, dont_filter=False)
			request.meta['dont_redirect'] = True
			request.meta['category_name'] = category_name
			request.meta['category_id'] = category_id
			yield request

	def preprocess_request(self, request):
		# request.replace(cookies={'index_location_city': '%E4%B8%8A%E6%B5%B7'})
		# request.replace(url='?'.join(request.url, self.query_str))
		return request

	def parse_job(self, response):
		item = JobItem()
		l = LagouJobItemLoader(item=JobItem(), response=response)
		
		xpath = '//*[contains(@class, "position-content")]/*[contains(@class, "position-content-l")]'
		cl = response.xpath(xpath)
		jn = cl.xpath('*[@class="job-name"]')
		l.add_value('position', jn.xpath('*[@class="name"]/text()').extract_first())
		l.add_value('department', jn.xpath('*[@class="company"]/text()').extract_first())
		jr =cl.xpath('*[@class="job_request"]')
		t = jr.xpath('p/span/text()').extract()
		l.add_value('salary', t[0])
		l.add_value('city', t[1])
		l.add_value('exprience', t[2])
		l.add_value('education', t[3])
		l.add_value('jobtype', t[4])
		l.add_value('tags', jr.xpath('ul[contains(@class, "position-label")]/li/text()').extract())
		l.add_value('postdate', jr.xpath('*[@class="publish_time"]/text()').re_first(r'(\d{4}-\d{2}-\d{2})'))
		jd = response.xpath('//*[@id="job_detail"]')
		l.add_value('temptation', jd.xpath('*[contains(@class, "job-advantage")]/p/text()').extract())
		l.add_value('rawpost', jd.xpath('*[contains(@class, "job_bt")]//p/text()').extract())
		ja = jd.xpath('*[contains(@class, "job-address")]')
		address = ja.xpath('*[contains(@class, "work_addr")]/a[contains(@href, "https://www.lagou.com/")]/text()').extract()
		address += ja.xpath('*[contains(@class, "work_addr")]/text()').extract()
		l.add_value('address', address)
		longitude = ja.xpath('*[@name="positionLng"]/@value').extract_first(default='')
		latitude = ja.xpath('*[@name="positionLat"]/@value').extract_first(default='')
		l.add_value('location', ','.join([longitude, latitude]))

		xpath = '//*[@id="job_company"]'
		jc = response.xpath(xpath)
		l.add_value('company_name', jc.xpath('.//h2/text()').extract_first())
		company_brief = ''
		company_url = ''
		for li in jc.xpath('.//ul[contains(@class, "c_feature")]/li'):
			feature = li.xpath('*[contains(@class, "hovertips")]/text()').extract_first()
			value = ''.join([s.strip() for s in li.xpath('text()').extract() if s.strip()])
			if '领域' in feature:
				l.add_value('company_brief', '领域: {}\n'.format(value))
			elif '发展阶段' in feature:
				l.add_value('company_brief', '发展阶段: {}\n'.format(value))
			elif '规模' in feature:
				l.add_value('company_brief', '规模: {}\n'.format(value))
			elif '公司主页' in feature:
				l.add_value('company_url', li.xpath('a/@href').extract_first())
		yield l.load_item()