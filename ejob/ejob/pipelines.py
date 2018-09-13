# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os, json, codecs, hashlib
from urllib.parse import quote
import scrapy
from scrapy.exceptions import DropItem

class EjobPipeline(object):
	def process_item(self, item, spider):
		return item

class JsonStorePipeline(object):
	"""Store Scrapy item into a json line file that is named by spider name."""

	def __init__(self, datafile):
		# self.f = codecs.open(datafile, 'a+', encoding='utf-8')
		self.f = codecs.open(datafile, 'w', encoding='utf-8')

	def process_item(self, item, spider):
		try:
			item_dict = dict(item)
			self.f.write(json.dumps(item_dict, ensure_ascii=False)+'\n')
		except Exception as e:
			raise DropItem(e)
		return item

	@classmethod
	def from_crawler(cls, crawler):
		datadir = crawler.settings['DATA_DIR']
		dataext = crawler.settings['DATA_EXT']
		datafile = os.path.join(datadir, crawler.spider.name + dataext)
		i = 1
		while os.path.isfile(datafile):
			datafile = os.path.join(datadir, crawler.spider.name + '_%d' % i + dataext)
			i += 1
		return cls(datafile)

	def open_spider(self, spider):
		pass

	def close_spider(self, spider):
		if not self.f.closed:
			self.f.close()


class ScreenshotBySplashPipeline(object):
	"""Use Splash to render screenshot of every Scrapy item"""

	def __init__(self, splash_url, screenshot_dir, screenshot_format, screenshot_url_field, screenshot_file_field):
		self.splash_url = splash_url
		self.screenshot_dir = screenshot_dir
		self.screenshot_format = screenshot_format
		self.screenshot_url_field = screenshot_url_field
		self.screenshot_file_field = screenshot_file_field
	
	@classmethod
	def from_crawler(cls, crawler):
		# URL like this: "http://localhost:8050/render.png?url={}"
		splash_url = crawler.settings['SPLASH_URL']
		screenshot_dir = crawler.settings['SCREENSHOT_DIR'] # screenshot files' storage directory
		# may be is "url", the page to be screenshot
		screenshot_url_field = crawler.settings['SCREENSHOT_URL_FIELD']
		# may be is "screenshot", the generated screenshot location
		screenshot_file_field = crawler.settings['SCRAEENSHOT_FILE_FIELD']
		# png, jpg, gif and so on
		screenshot_format = crawler.settings['SCREENSHOT_FORMAT']
		return cls(splash_url, screenshot_dir, screenshot_format, screenshot_url_field, screenshot_file_field)

	def process_item(self, item, spider):
		try:
			url_field = self.screenshot_url_field
			splash_url = self.splash_url
			screenshot_ext = self.screenshot_format
			encoded_item_url = quote(item[url_field])
			url = splash_url.format(encoded_item_url)
			url_hash = hashlib.md5(url.encode("utf8")).hexdigest()
			filename = "{}.{}".format(url_hash, screenshot_ext)
			request = scrapy.Request(url)
			request.meta['screenshot_filename'] = filename
			# Deferred Process item
			dfd = spider.crawler.engine.download(request, spider)
			dfd.addBoth(self.return_item, item)
		except Exception as e:
			raise DropItem(e)
		return dfd

	def return_item(self, response, item):
		screenshot_dir = self.screenshot_dir
		file_field = self.screenshot_file_field
		if response.status != 200:
			# Error happened, return item.
			return item

		# Save screenshot to file
		filename = response.meta['filename']
		with open(os.path.join(screenshot_dir, filename), 'wb') as f:
			f.write(response.body)
		item[file_field] = filename
		return item