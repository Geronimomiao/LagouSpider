# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from LagouSpider.items import LagouJobItemLoder, LagouJobItem
from LagouSpider.uitl.common import get_md5


class LagouSpider(CrawlSpider):
    name = 'lagou'
    allowed_domains = ['www.lagou.com']
    start_urls = ['https://www.lagou.com/']

    rules = (
        # Rule(LinkExtractor(allow=r'zhaopin/.*'), follow=True),
        # Rule(LinkExtractor(allow=r'gongsi/j\d+.*'), follow=True),
        Rule(LinkExtractor(allow=r'jobs/\d+.html'), callback='parse_job', follow=True),
    )

    def parse_job(self, response):
        # 解析 拉勾网的职位
        item_loader = LagouJobItemLoder(item=LagouJobItem(), response=response)
        item_loader.add_css('title', ".job-name::attr(title)")
        item_loader.add_value('url', response.url)
        item_loader.add_value('url_object_id', get_md5(response.url))
        item_loader.add_css('salary', '.job_request .salary::text')

        return item_loader.load_item()
