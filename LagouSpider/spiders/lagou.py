# -*- coding: utf-8 -*-
import scrapy, datetime, random
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from LagouSpider.items import LagouJobItemLoder, LagouJobItem
from LagouSpider.uitl.common import get_md5
# from LagouSpider.settings import user_agent_list


class LagouSpider(CrawlSpider):
    name = 'lagou'
    allowed_domains = ['www.lagou.com']
    start_urls = ['https://www.lagou.com/jobs/4325051.html']
    custom_settings = {
        # 降低网站 爬取速度
        'DOWNLOAD_DELAY': 0.25
    }


    rules = (
        Rule(LinkExtractor(allow=r'zhaopin/.*'), follow=True),
        Rule(LinkExtractor(allow=r'gongsi/j\d+.*'), follow=True),
        Rule(LinkExtractor(allow=r'jobs/\d+.html'), callback='parse_job', follow=True),
    )

    def parse_job(self, response):
        # 解析 拉勾网的职位
        item_loader = LagouJobItemLoder(item=LagouJobItem(), response=response)
        item_loader.add_css('title', ".job-name::attr(title)")
        item_loader.add_value('url', response.url)
        item_loader.add_value('url_object_id', get_md5(response.url))
        item_loader.add_css('salary', '.job_request .salary::text')
        item_loader.add_css('job_city', '.job_request span:nth-child(2)::text')
        item_loader.add_css('work_years', '.job_request span:nth-child(3)::text')
        item_loader.add_css('degree_need', '.job_request span:nth-child(4)::text')
        item_loader.add_css('job_type', '.job_request span:nth-child(5)::text')
        item_loader.add_css('publish_time', ".publish_time::text")
        item_loader.add_css('tags', ".position-label li::text")
        item_loader.add_css('job_advantage', '.job-advantage p::text')
        item_loader.add_css('job_desc', '.job-detail')
        item_loader.add_css('job_addr', '.work_addr')
        item_loader.add_css('company_url', '.c_feature li:last-child a::text')
        item_loader.add_css('company_name', '.job_company img::attr(alt)')
        item_loader.add_value('crawl_time', datetime.datetime.now())

        job_item = item_loader.load_item()

        return item_loader.load_item()


    def start_requests(self):
        # 在发起请求 时生成 user_agent
        # 藕合性过高
        # random_index = random.randint(0, len(user_agent_list) - 1)
        # random_agent = user_agent_list[random_index]
        # headers = {
        #     "User-Agent": random_agent
        # }
        return [scrapy.Request('https://www.lagou.com')]


