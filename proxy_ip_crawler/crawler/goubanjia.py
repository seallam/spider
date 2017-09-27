import time
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from database.mysql.entity.proxy_ip import ProxyIp
from proxy_ip_crawler.crawler.ip_crawler import IpCrawler


class Goubanjia(IpCrawler):
	def get_proxy_list(self):
		print('即将执行%s代理ip获取' % self.name)
		proxy_url = 'http://www.goubanjia.com/'
		header = {
			'cache-control': "no-cache",
			'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'
		}
		proxy_list = []
		self.get_proxy_ip(header, proxy_list, proxy_url, 'free/gwgn/index%s.shtml')
		self.get_proxy_ip(header, proxy_list, proxy_url, 'free/gngn/index%s.shtml')
		return proxy_list

	def get_proxy_ip(self, header, proxy_list, proxy_url, ext_url):
		for i in range(1, 3):
			response = requests.request('GET', proxy_url + ext_url % str(i), headers=header)
			if response.status_code == 200:
				html = response.text
				# 获取id为ip_list的table
				bf1_ip_list = BeautifulSoup(html, 'lxml')
				bf2_ip_list = BeautifulSoup(str(bf1_ip_list.find_all(id='list')), 'lxml')
				ip_list = bf2_ip_list.find_all('tr')

				for index in range(1, len(ip_list)):
					if len(ip_list[index].find_all('td')) > 2:
						visible = ip_list[index].find_all('td')[1].text
						if visible == '高匿':
							ip_port = ip_list[index].find_all('td')[0].text.replace('..', '.')
							ip_port = ip_port.split(':')
							ip = ip_port[0]
							port = ip_port[1]
							protocol = ip_list[index].find_all('td')[2].text
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


if __name__ == '__main__':
	time.sleep(60 * 10)
	while True:
		goubanjia = Goubanjia('goubanjia')
		proxy_ip_list = goubanjia.get_proxy_list()
		goubanjia.save_ip_list(proxy_ip_list)
		print("goubanjia代理ip入库结束,共处理%s条ip记录" % len(proxy_ip_list))
		time.sleep(60 * 30)
