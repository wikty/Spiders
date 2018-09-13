# -*- coding: utf-8 -*-
import os, json, re
from urllib.parse import quote
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from ejob.items import JobItem
from ejob.item_loaders import RongypJobItemLoader

def filter_job_url(url):
	m = re.search(r'openings_id=\d+$', url)
	if not m:
		return None
	return url

def process_page_request(request):
	return request

class RongypJobSpiderSpider(CrawlSpider):
	name = "rongyp_job_spider_test"
	allowed_domains = ["rongyp.com"]
	start_urls = ['http://www.rongyp.com/']
	urls = [('category', 'https://www.rongyp.com/index.php?m=Home&c=Job&a=jobSearch&tb_city=&tb_jobtype=&tb_jobtype_two=2132&tb_salary=&tb_workyear=&tb_degree=&tb_worknature=&dayscope=&keyword=&orderby=&company_size=')]
	rules = [
		Rule(LinkExtractor(tags=('a', ), restrict_xpaths=('//*[class="rightmember-page"]', )), process_request=process_page_request, follow=True),
		Rule(LinkExtractor(tags=('a', ), attrs=('href', ), unique=True, restrict_xpaths=('//*[@class="ryp-search-list"]/*[@class="ryp-search-li"]/p', ), process_value=filter_job_url), callback='parse_job'),
	]
	# query_str = '&'.join(['{}'.format(quote('city=全国'))])

	def __init__(self, urlfile=None, *args, **kwargs):
		# scrapy crawl myspider -a category=electronics
		super(RongypJobSpiderSpider, self).__init__(*args, **kwargs)
		if urlfile:
			with open(urlfile, 'r', encoding='utf8') as f:
				for line in f:
					line = line.strip()
					if not line:
						continue
					self.urls.append((item['name'], item['url']))
		else:
			print('URL file is missed')

	def start_requests(self):
		for category_name, category_url in self.urls:
			# category_url = '?'.join([category_url, self.query_str])
			request = scrapy.Request(category_url, dont_filter=False)
			request.meta['dont_redirect'] = True
			request.meta['category_name'] = category_name
			yield request

	# def preprocess_value(self, value):
	# 	m = re.search(r'openings_id=\d+$', value)
	# 	print(value, m)
	# 	if not m:
	# 		return None
	# 	return value

	def preprocess_request(self, request):
		# request.replace(cookies={'index_location_city': '%E4%B8%8A%E6%B5%B7'})
		# request.replace(url='?'.join(request.url, self.query_str))
		return request

	def parse_job(self, response):

		item = JobItem()
		l = RongypJobItemLoader(item=JobItem(), response=response)
		info = response.xpath('//*[contains(@class, "ryp-info")]/*[contains(@class, "ryp-mask")]')
		l.add_value('position', info.xpath('h1/text()').extract_first())
		l.add_value('salary', info.xpath('h6/*[@class="salary"]/text()').extract_first())
		t = ''.join(info.xpath('h6/text()').extract())
		t = [s.strip() for s in t.split('|') if s.strip()]
		if len(t) < 3:
			t += ['']*(3-len(t))
		l.add_value('jobtype', t[0])
		l.add_value('education', t[1])
		l.add_value('exprience', t[2])
		l.add_value('temptation', response.xpath('//*[contains(@class, "ryp-weals")]/a/text()').extract())
		l.add_value('rawpost', response.xpath('//*[contains(@class, "ryp-detail-content")]/p/text()').extract())
		company = response.xpath('//*[contains(@class, "ryp-detail-right")]//*[@class="company"]')
		l.add_value('company_name', company.xpath('h3/a/text()').extract_first())
		company_brief = ''
		for detail in company.xpath('*[@class="detail"]'):
			detail_name = ''.join(detail.xpath('text()').extract())
			detail_value = detail.xpath('span/text()').extract_first(default='')
			if '区域' in detail_name:
				l.add_value('company_brief', '区域: {}'.format(detail_value))
			elif '行业' in detail_name:
				l.add_value('company_brief', '行业: {}'.format(detail_value))
			elif '规模' in detail_name:
				l.add_value('company_brief', '规模: {}'.format(detail_value))
		
		l.add_value('address', response.xpath('//*[contains(@class, "ryp-map")]//*[contains(@class, "company-adress")]/text()').extract_first())
		yield l.load_item()