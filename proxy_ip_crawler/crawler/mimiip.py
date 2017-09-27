import time
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from database.mysql.entity.proxy_ip import ProxyIp
from proxy_ip_crawler.crawler.ip_crawler import IpCrawler


class Mimiip(IpCrawler):
	def get_proxy_list(self):
		print('即将执行%s代理ip获取' % self.name)
		proxy_url = 'http://www.mimiip.com/'
		proxy_list = []
		for i in range(1, 3):
			response = requests.get((proxy_url + 'gngao/%s') % str(i))
			html = response.text
			soup = BeautifulSoup(html, 'lxml')
			bf2_ip_list = BeautifulSoup(str(soup.find_all('table')), 'lxml')
			ip_list = bf2_ip_list.find_all('tr')
			for index in range(1, len(ip_list)):
				if len(ip_list[index].find_all('td')) > 2:
					ip = ip_list[index].find_all('td')[0].text
					port = ip_list[index].find_all('td')[1].text
					protocol = ip_list[index].find_all('td')[5].text
					if protocol.lower() == 'https':
						_type = 2
					elif protocol.lower() == 'http':
						_type = 1
					else:
						_type = 3
					# print('ip为[%s], 端口为:%s, %s, http协议为:%s' % (ip, port, visible, protocol))
					proxy_ip = ProxyIp(ip=ip, port=port, _type=_type, source=proxy_url, is_alive=1, create_time=datetime.now(), update_time=datetime.now())
					proxy_list.append(proxy_ip)
			time.sleep(2)

		return proxy_list


if __name__ == '__main__':
	time.sleep(60 * 20)
	while True:
		mimiip = Mimiip('秘密代理')
		proxy_ip_list = mimiip.get_proxy_list()
		mimiip.save_ip_list(proxy_list=proxy_ip_list)
		print("快%s ip入库结束,共处理了%s个ip" % ('秘密代理', len(proxy_ip_list)))
		time.sleep(60 * 30)
