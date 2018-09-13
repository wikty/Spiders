# -*- coding: utf-8 -*-
import time, os, json
import requests
import scrapy
from scrapy.mail import MailSender

def get_email_body(title, speaker, address, showtime, reservetime):
	return """
Title: {title}
Speaker: {speaker}
Address: {address}
ShowTime: {showtime}
ReserveTime: {reservetime}

""".format(title=title, speaker=speaker, address=address, showtime=showtime, reservetime=reservetime)

def send_simple_message(title, body, receivers):
	return requests.post(
		"https://api.mailgun.net/v3/sandboxdd4b279d71df4a03ad2388f4af5c81d8.mailgun.org/messages",
		auth=("api", "key-fd8e348bdec8df0586d1a4801aada0e4"),
		data={
			"from": "xiaowenbin@wikty.com",
			"to": receivers,
			"subject": title,
			"text": body}
	)

class EventWisesoeSpiderSpider(scrapy.Spider):
	name = "event_wisesoe_spider"
	login_url = 'http://account.wisesoe.com/WcfServices/SSOService.svc/Account/Logon?callback=jQuery180047063062154941493_1492137595375&UserName={username}&Password={password}&_={timestamp}'
	home_url = 'http://event.wisesoe.com/Authenticate.aspx?returnUrl=Default.aspx'
	
	def start_requests(self):
		config_file = self.settings.get('EVENT_WISESOE_COM_CONFIG')
		if not os.path.exists(config_file):
			self.logger.error('wisesoe config file not exists')
			return None
		
		self.config = {}
		with open(config_file, 'r', encoding='utf8') as f:
			self.config = json.loads(f.read())
		if not self.config:
			self.logger.error('wisesoe config file is emtpy')
			return None
		
		self.username = self.config['username']
		if not self.username:
			self.logger.error('wisesoe username is emtpy')
			return None

		self.password = self.config['password']
		if not self.password:
			self.logger.error('wisesoe password is emtpy')
			return None

		self.receivers = self.config['receivers']
		if not self.receivers:
			self.logger.error('wisesoe receciver is emtpy')
			return None

		yield scrapy.Request(
			self.login_url.format(
				username=self.username, 
				password=self.password, 
				timestamp=int(time.time())),
			callback=self.parse,
			meta={'cookiejar': 1}
		)

	def parse(self, response):
		# self.logger.error(response.body.decode('utf-8'))
		yield scrapy.Request(
			self.home_url,
			callback=self.home_parse,
			meta={'cookiejar': response.meta['cookiejar']}
		)

	def home_parse(self, response):
		# self.logger.error(response.body.decode('utf-8'))
		xpath = '//*[@id="default-menu-control"]//a[contains(text(), "My reservations")]'
		url = response.xpath(xpath).xpath('@href').extract_first()
		url = response.urljoin(url)
		yield scrapy.Request(
			url,
			callback=self.parse_my_reservations,
			meta={'cookiejar': response.meta['cookiejar']}
		)

	def parse_my_reservations(self, response):
		# self.logger.error(response.body.decode('utf-8'))
		xpath = '//table[@id="ctl00_MainContent_GridView1"]/tbody/tr[position() > 1]'
		msg = []
		max_timestamp = self.config['timestamp']
		for tr in response.xpath(xpath):
			title = tr.xpath('td[2]/text()').extract_first(default='').strip()
			speaker = tr.xpath('td[3]/text()').extract_first(default='').strip()
			address = tr.xpath('td[4]/text()').extract_first(default='').strip()
			showtime = tr.xpath('td[5]/text()').extract_first(default='').strip()
			reservation_time = tr.xpath('td[6]/text()').extract_first(default='').strip()
			if reservation_time:
				timestamp = int(time.mktime(time.strptime(reservation_time, '%m/%d/%Y %I:%M:%S %p')))
				if timestamp > max_timestamp:
					max_timestamp = timestamp
				if timestamp > self.config['timestamp']:
					msg.append(get_email_body(title, speaker, address, showtime, reservation_time))

		if msg:
			send_simple_message('讲座通知', '\n'.join(msg), self.receivers)