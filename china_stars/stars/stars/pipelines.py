# -*- coding: utf-8 -*-
import codecs, json, sqlite3
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class StarsCatalogPipeline(object):
	def open_spider(self, spider):
		self.f = codecs.open('stars_catalog.json', 'w', encoding='utf-8')
		self.catalog = {}

	def close_spider(self, spider):
		self.f.write(json.dumps(self.catalog, ensure_ascii=False))
		self.f.close()

	def process_item(self, item, spider):
		if item['capital'] not in self.catalog:
			self.catalog[item['capital']] = []
		self.catalog[item['capital']].append({
			'url': item['url'],
			'name': item['name']
		})
		return item

class StarInfoPipeline(object):
	def process_item(self, item, spider):
		return item

class Sqlite3Pipeline(object):
	def __init__(self, sqlite_file, sqlite_table, sqlite_table_desc, image_dir):
		self.sqlite_file = sqlite_file
		self.sqlite_table = sqlite_table
		self.sqlite_table_desc = sqlite_table_desc
		self.image_dir = image_dir

	@classmethod
	def from_crawler(cls, crawler):
		file = crawler.settings.get('SQLITE_FILE', 'sqlite3.db')
		table = crawler.settings.get('SQLITE_TABLE', 'items')
		tbl_desc = crawler.settings.get('SQLITE_TABLE_DESC')
		image_dir = crawler.settings.get('IMAGES_STORE')
		if not tbl_desc:
			raise Exception('SQLITE_TABLE_DESC is missed in the settings file')
		if not isinstance(tbl_desc, dict):
			raise Exception('SQLITE_TABLE_DESC must be a dictionary')
		return cls(
			sqlite_file=file,
			sqlite_table=table,
			sqlite_table_desc=tbl_desc,
			image_dir=image_dir
		)

	def open_spider(self, spider):
		self.client = sqlite3.connect(self.sqlite_file)
		self.cursor = self.client.cursor()
		sql = 'CREATE TABLE IF NOT EXISTS {table} ({fields})'
		fields = ['id INTEGER PRIMARY KEY AUTOINCREMENT']
		for field, dtype in self.sqlite_table_desc.items():
			if dtype == 'i':
				field = '%s INTEGER' % field
			elif dtype == 'S':
				field = '%s TEXT' % field
			else:
				field = '%s VARCHAR(255)' % field
			fields.append(field)
		sql = sql.format(table=self.sqlite_table, fields=', '.join(fields))
		self.cursor.execute(sql)
		self.client.commit()


	def close_spider(self, spider):
		self.client.close()

	def item2dict(self, item):
		d = {}
		d['album'] = []
		avatar_url = item['avatar']
		for key in self.sqlite_table_desc:
			if key == 'avatar':
				for image in item['images']:
					if image['url'] == avatar_url:
						d['avatar'] = [self.image_dir+'/'+image['path'], avatar_url]
			elif key == 'album':
				for image in item['images']:
					if image['url'] != avatar_url:
						d['album'].append([self.image_dir+'/'+image['path'], image['url']])
			else:
				d[key] = item[key]
		d['avatar'] = json.dumps(d['avatar'], ensure_ascii=False)
		d['album'] = json.dumps(d['album'], ensure_ascii=False)
		return d

	def process_item(self, item, spider):
		d = self.item2dict(item)
		sql = 'INSERT INTO {table} ({keys}) VALUES ({values})'
		
		sql = sql.format(
			table=self.sqlite_table,
			keys= ', '.join(d.keys()),
			values=', '.join(['?']*len(d.keys()))
		)
		
		
		self.cursor.execute(sql, list(d.values()))
		self.client.commit()
		return item