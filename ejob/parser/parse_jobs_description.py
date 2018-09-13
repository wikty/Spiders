from scrapy.selector import Selector

def parse(filename):
	content = ''
	with open(filename, 'r', encoding='utf8') as f:
		content = f.read()
	sl = Selector(text=content)