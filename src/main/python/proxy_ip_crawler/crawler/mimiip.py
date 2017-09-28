import time
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from database.mysql.entity.proxy_ip import ProxyIp
from proxy_ip_crawler.crawler.ip_crawler import IpCrawler
from src.main.python.tools.proxy_pre_heat import PreheatUtils


class Mimiip(IpCrawler):
	def get_proxy_list(self):
		print('即将执行%s代理ip获取' % self.name)
		proxy_url = 'http://www.mimiip.com/'
		header = {
			'cache-control': "no-cache",
			'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'
		}
		preheat = PreheatUtils(proxy_url)
		proxies = preheat.get_proxy_ip()
		proxy_list = []
		flag = False
		for i in range(1, 3):
			response = requests.get(url=(proxy_url + 'gngao/%s') % str(i), proxies=proxies, headers=header)
			html = response.text
			if 'block' in html:
				print('第%s页数据被block' % i)
				flag = True
			while flag:
				proxies = preheat.get_proxy_ip()
				try:
					response = requests.get(url=(proxy_url + 'gngao/%s') % str(i), proxies=proxies, headers=header)
				except:
					print('%s get error' % self.name)
				if response.status_code == 200:
					html = response.text
					if 'block' not in html:
						print('获取网页内容成功')
						flag = False

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
			time.sleep(10)

		return proxy_list


if __name__ == '__main__':
	time.sleep(60 * 20)
	while True:
		mimiip = Mimiip('秘密代理')
		proxy_ip_list = mimiip.get_proxy_list()
		mimiip.save_ip_list(proxy_list=proxy_ip_list)
		print("%s ip入库结束,共处理了%s个ip" % ('秘密代理', len(proxy_ip_list)))
		time.sleep(60 * 30)
