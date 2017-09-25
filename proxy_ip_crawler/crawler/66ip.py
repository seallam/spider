import time
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from lxml import etree

from database.mysql.entity.proxy_ip import ProxyIp
from proxy_ip_crawler.ip_crawler import IpCrawler


class IP66(IpCrawler):
	def get_proxy_list(self):
		print('即将开始爬取66ip的ip')
		proxy_url = 'http://www.66ip.cn/%s.html'
		proxy_list = []
		for i in range(1, 3):
			response = requests.get(proxy_url % str(i))
			if response.status_code == 200:
				response.encoding = 'gb2312'
				html = response.text
				bf1_ip_list = BeautifulSoup(html, 'lxml')
				bf2_ip_list = BeautifulSoup(str(bf1_ip_list.find_all(id='main')), 'lxml')
				ip_list_info = bf2_ip_list.table.find_all('tr')

				for index in range(1, len(ip_list_info)):
					dom = etree.HTML(str(ip_list_info[index]))
					ip = dom.xpath('//td[1]')
					port = dom.xpath('//td[2]')
					# print(ip[0].text + ':' + port[0].text)
					proxy_ip = ProxyIp(ip=ip[0].text, port=port[0].text, _type=1, source='http://www.66ip.cn/', is_alive=1, create_time=datetime.now(), update_time=datetime.now())
					proxy_list.append(proxy_ip)
		return proxy_list


if __name__ == '__main__':
	while True:
		ip66 = IP66('66免费代理')
		proxy_ip_list = ip66.get_proxy_list()
		ip66.save_ip_list(proxy_ip_list)
		print('66ip入库结束,共处理%s条记录' % len(proxy_ip_list))
		time.sleep(60 * 30)
