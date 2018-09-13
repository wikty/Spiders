# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType


class NotificationSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class PhantomjsMiddleware(object):
    def __init__(self, phantomjs_path=None, extra_script=None):
        if not phantomjs_path:
            raise Exception('phantomjs path should not be empty')
        self.script = None
        if extra_script:
            with open(extra_script, 'r', encoding='utf8') as f:
                self.script = f.read()
        self.driver = webdriver.PhantomJS(phantomjs_path)

    @classmethod
    def from_crawler(cls, crawler):
        phantomjs_path = crawler.settings.get('PHANTOMJS_PATH')
        extra_script = crawler.settings.get('EXTRA_SCRIPT')

        return cls(phantomjs_path, extra_script)

    def process_request(self, request, spider):
        self.driver.get(request.url)
        if self.script:
            self.driver.execute_script(self.script)
        body = self.driver.page_source.encode('utf8')
        response = HtmlResponse(url=self.driver.current_url, body=body)
        return response # end any process_request methods