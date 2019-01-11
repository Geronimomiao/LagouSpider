# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     crawl_xici_ip
   Description :   爬取西刺的 IP 代理
   Author :       wsm
   date：          2019-01-11
-------------------------------------------------
   Change Activity:
                   2019-01-11:
-------------------------------------------------
"""
__author__ = 'wsm'
import requests, MySQLdb
from scrapy.selector import Selector

conn = MySQLdb.connect(host='127.0.0.1', user='root', passwd='Geronimo1701', db='article_spider', charset='utf8')
cursor = conn.cursor()

def crawl_ips():
    # 爬取西刺免费 IP 代理
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0"}
    for i in range(1, 1000):
        re = requests.get('https://www.xicidaili.com/nn/{0}'.format(i), headers=headers)

        select = Selector(text=re.text)
        all_trs = select.css('#ip_list tr')
        ip_list= []

        for tr in all_trs[1:]:
            # 去掉表头
            speed_str = tr.css(".bar::attr(title)").extract_first()
            if speed_str:
                speed = float(speed_str.split('秒')[0])
            all_texts = tr.css('td::text').extract()

            ip = all_texts[0]
            port = all_texts[1]
            proxy_type = all_texts[5]

            ip_list.append((ip, port, proxy_type, speed))

        for ip_info in ip_list:
            insert_sql = '''
                insert into proxy_ip(ip, port, proxy_type, speed) values (%s, %s, %s, %s)
            '''
            params = ip_info
            cursor.execute(insert_sql, params)
            conn.commit()


class GetIP(object):

    def delete_ip(self, ip):
        # 从数据库 删除无效的 ip
        delete_sql = '''
            delete from proxy_ip where ip = '{0}'
        '''.format(ip)
        cursor.execute(delete_sql)
        conn.commit()
        return True

    def judge_ip(self, ip, port):
        http_url = 'https://www.baidu.com'
        proxy_url = 'http://{0}:{1}'.format(ip, port)
        try:
            proxy_dict = {
                'http': proxy_url
            }
            response = requests.get(http_url, proxies=proxy_dict)
            return True
        except Exception as e:
            print('invalid ip and port')
            self.delete_ip(ip)
            return False
        else:
            code = response.status_code
            if code >= 200 and code < 300:
                print('effective ip')
                return True
            else:
                print('invalid ip and port')
                self.delete_ip(ip)
                return False

    def get_random_ip(self):
        # 从数据库中 获得一个 随机可用 IP
        random_sql = '''
            select ip, port from proxy_ip where proxy_type = 'HTTP' ORDER BY RAND() LIMIT 1
        '''
        result = cursor.execute(random_sql)
        for ip_info in cursor.fetchall():
            ip = ip_info[0]
            port = ip_info[1]

            self.judge_ip(ip, port)

# print(crawl_ips())

get_ip = GetIP()
get_ip.get_random_ip()