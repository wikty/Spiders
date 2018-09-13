from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join, Compose, Identity
from w3lib.html import remove_tags

def take_first_nonempty_from_iterable():
	return TakeFirst()

def str_strip(chars=' '):
	return MapCompose(lambda s: s.strip(chars))

def list_strip(chars=' '):
	return MapCompose(lambda l: ''.join([s.strip(chars) for s in l]))

# def str_strip(chars=' '):
# 	return Compose(lambda l:l[0].strip(chars))

def html_strip():
	return MapCompose(remove_tags)

def comma_join():
	return Join(separator=',')

def newline_join():
	return Join(separator='\n')

def list_join_if_nonempty(separator=''):
	return lambda loader, l: separator.join([s.strip() for s in l if s.strip()])

def filter_word(word):
	return MapCompose(lambda s: None if s == word else s)

class LagouJobItemLoader(ItemLoader):

	default_input_processor = str_strip()
	default_output_processor = Join()

	salary = str_strip(' /')
	city_in = str_strip(' /')
	exprience_in = str_strip(' /')
	education_in = str_strip(' /')
	jobtype_in = str_strip(' /')
	tags_in = list_strip()
	tags_out = list_join_if_nonempty(',')
	temptation_in = Identity()
	temptation_out = newline_join()
	rawpost_in = Identity()
	rawpost_out = newline_join()
	address_in = list_strip(' -\n')
	address_out = list_join_if_nonempty(',')
	company_name_in = str_strip(' \n')
	company_brief_out = newline_join()


class RongypJobItemLoader(ItemLoader):
	default_input_processor = str_strip()
	default_output_processor = Join()

	position_in = str_strip(' \n')
	temptation_out = comma_join()
	company_brief_out = newline_join()
