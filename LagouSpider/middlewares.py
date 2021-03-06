# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from fake_useragent import UserAgent
from LagouSpider.tools.crawl_xici_ip import GetIP

class LagouspiderSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class LagouspiderDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class RandomUserAgentMiddleware(object):
    # 随机更换 user-agent
    def __init__(self, crawler):
        super(RandomUserAgentMiddleware, self).__init__()
        # self.user_agent_list = crawler.settings.get('user_agent', [])
        self.ua = UserAgent()
        self.ua_type = crawler.settings.get('RANDOM_UA_TYPE', 'random')

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_request(self, request, spider):

        def get_ua():
            return getattr(self.ua, self.ua_type)

        # random_agent = get_ua()
        request.headers.setdefault('User-Agent', get_ua())


class RandomProxyMiddleware(object):
    # 动态设置 IP 代理
    def process_request(self, request, spider):
        # request.meta['proxy'] = 'http://121.61.32.209:9999'
        get_ip = GetIP()
        request.meta['proxy'] = get_ip.get_random_ip()


import time
from selenium import webdriver
from scrapy.http import HtmlResponse

class JSPageMiddleware(object):
    # 初始化 可以 在 spider 中做 否则当 spider 关闭时 chrome 不会 关闭
    # def __init__(self):
    #     self.browser = webdriver.Chrome(executable_path='/Users/wsm/Downloads/chromedriver')
    #     super(JSPageMiddleware, self).__init__()

    # 抓去 动态加载 页面的数据
    def process_request(self, request, spider):
        if spider.name == 'lagou':
            # chrome_opt = webdriver.ChromeOptions()
            # # 1允许所有图片；2阻止所有图片；3阻止第三方服务器图片
            # prefs = {
            #     'profile.default_content_setting_values': {
            #         'images': 2
            #     }
            # }
            # chrome_opt.add_experimental_option('prefs', prefs)
            #
            # browser = webdriver.Chrome(executable_path='/Users/wsm/Downloads/chromedriver', chrome_options=chrome_opt)
            spider.browser.get(request.url)
            time.sleep(1)
            print("访问:{0}".format(request.url))
            # 当 scrapy 遇到 HtmlResponse 会直接返回 不会再将 res 交给 下载器
            return HtmlResponse(url=spider.browser.current_url, body=spider.browser.page_source, encoding='utf8', request=request)


