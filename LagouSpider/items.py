# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join
from w3lib.html import remove_tags

def remove_splash(value):
    # 过滤 /
    return value.replace('/', '')

def remove_html_tags(value):
    # 过滤 html 标签
    return remove_tags(value)

def handle_jobaddr(value):
    addr_list = value.split('\n')
    addr_list = [item.strip() for item in addr_list if item.strip()!='查看地图']
    return ''.join(addr_list)

class LagouspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class LagouJobItem(scrapy.Item):
    # 拉勾网 职位信息
    url_object_id = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    salary = scrapy.Field()
    job_city = scrapy.Field(
        input_processor=MapCompose(remove_splash)
    )
    work_years = scrapy.Field(
        input_processor=MapCompose(remove_splash)
    )
    degree_need = scrapy.Field(
        input_processor=MapCompose(remove_splash)
    )
    job_type = scrapy.Field()
    publish_time = scrapy.Field()
    tags = scrapy.Field(
        input_processor=Join(',')
    )
    job_advantage = scrapy.Field()
    job_desc = scrapy.Field()
    job_addr = scrapy.Field(
        input_processor=MapCompose(remove_html_tags, handle_jobaddr)
    )
    company_url = scrapy.Field()
    company_name = scrapy.Field()
    crawl_time = scrapy.Field()
    crawl_update_time = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = '''
            insert into lagou_job (url_object_id, url, title, salary, job_city, work_years, degree_need,
             job_type, publish_time, tags, job_advantage, job_desc, job_addr, company_url, company_name,
              crawl_time) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
        params = (self['url_object_id'], self['url'], self['title'], self['salary'], self['job_city'],
                  self['work_years'], self['degree_need'], self['job_type'], self['publish_time'], self['tags'],
                  self['job_advantage'], self['job_desc'], self['job_addr'], self['company_url'], self['company_name'], self['crawl_time'])
        return insert_sql, params


class LagouJobItemLoder(ItemLoader):
    default_output_processor = TakeFirst()