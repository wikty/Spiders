# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

import os
from scrapy import signals
from scrapy.http import HtmlResponse
from selenium import webdriver


class EjobSpiderMiddleware(object):
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


class BaseJsRequestMiddleware(object):
    
    def __init__(self, driver_path, extra_script_file=None):
        if not os.path.isfile(driver_path):
            raise Exception('driver path [%s] not exists' % driver_path)
        if extra_script_file and not os.path.isfile(extra_script_file):
            raise Exception('extra script file [%s] not exists' % extra_script_file)
        
        self.driver = None
        self.script = None
        if extra_script_file:
            with open(extra_script_file, 'r', encoding='utf8') as f:
                self.script = f.read()

    def get_dirver(self, **kwargs):
        if not self.driver:
            self.driver = webdriver.PhantomJS(executable_path=self.driver_path, **kwargs)
        return self.driver

    def process_request(self, request, spider):
        driver = self.get_dirver()
        driver.get(request.url)
        url = driver.current_url
        encoding = request.encoding
        if self.script:
            driver.execute_script(self.script)
        body = driver.page_source.encode(encoding)
        response = HtmlResponse(url=url, body=body, encoding=encoding)
        return response # end any process_request methods


class PhantomjsRequestMiddleware(BaseJsRequestMiddleware):
    
    def __init__(self, phantomjs_path=None, extra_script_file=None):
        super(PhantomjsRequestMiddleware, self).__init__(phantomjs_path, extra_script_file)

    @classmethod
    def from_crawler(cls, crawler):
        phantomjs_path = crawler.settings.get('PHANTOMJS_PATH')
        extra_script_file = crawler.settings.get('EXTRA_SCRIPT_FILE')

        return cls(phantomjs_path, extra_script_file)
