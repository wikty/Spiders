# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class StarsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class StarInfoItem(scrapy.Item):
	starid = scrapy.Field()
	url = scrapy.Field()
	capital = scrapy.Field()
	name = scrapy.Field()
	another_name = scrapy.Field()
	english_name = scrapy.Field()
	gender = scrapy.Field()
	birthyear = scrapy.Field()
	birthday = scrapy.Field()
	constellation = scrapy.Field()
	nationality = scrapy.Field()
	area = scrapy.Field()
	profession = scrapy.Field()
	height = scrapy.Field()
	bloodtype = scrapy.Field()
	brief = scrapy.Field()
	avatar = scrapy.Field()
	album = scrapy.Field()
	image_urls = scrapy.Field()
	images = scrapy.Field()

