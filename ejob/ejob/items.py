# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class EjobItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class CatalogItem(scrapy.Item):
	id = scrapy.Field()
	name = scrapy.Field()
	url = scrapy.Field()
	category = scrapy.Field()

class JobItem(scrapy.Item):
	position = scrapy.Field()
	department = scrapy.Field()
	description = scrapy.Field()
	tags = scrapy.Field()
	salary = scrapy.Field()
	temptation = scrapy.Field()
	jobtype = scrapy.Field()
	exprience = scrapy.Field()
	education = scrapy.Field()
	requirements = scrapy.Field()
	
	city = scrapy.Field()
	address = scrapy.Field()
	location = scrapy.Field()
	
	url = scrapy.Field()
	site = scrapy.Field()
	rawpost = scrapy.Field()
	postdate = scrapy.Field()
	
	company_name = scrapy.Field()
	company_url = scrapy.Field()
	company_brief = scrapy.Field()
