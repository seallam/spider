import time
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from lxml import etree

from database.mysql.entity.proxy_ip import ProxyIp
from proxy_ip_crawler.crawler.ip_crawler import IpCrawler


class Xicidaili(IpCrawler):

	def get_proxy_list(self):
		print('即将执行%s代理ip获取' % self.name)
		# requests的Session可以自动保持cookie,不需要自己维护cookie内容
		session = requests.Session()

		proxy_url = 'http://www.xicidaili.com/nn/1'

		header = {
			'cache-control': "no-cache",
			'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'
		}

		proxy_response = session.request("GET", proxy_url, headers=header)

		html = proxy_response.text

		# soup = BeautifulSoup(html, 'lxml')
		# ip_list = soup.find(id='ip_list').find_all('tr')
		# for ip_element in ip_list:
		# 	# print(type(ip_element))
		# 	# print(ip_element.name)
		# 	tds = ip_element.find_all('td')
		# 	if len(tds) > 0:
		# 		country = ''
		# 		for child in tds[0].children:  # 获取国家属性
		# 			country = tds[0].contents[0].get('alt')
		# 		ip = tds[1].contents[0]
		# 		port = tds[2].contents[0]
		# 	print("=================")

		# 获取id为ip_list的table
		bf1_ip_list = BeautifulSoup(html, 'lxml')
		bf2_ip_list = BeautifulSoup(str(bf1_ip_list.find_all(id='ip_list')), 'lxml')
		ip_list_info = bf2_ip_list.table.contents
		# 爬取每个代理信息
		proxy_list = []
		for index in range(len(ip_list_info)):
			if index % 2 == 1 and index != 1:
				dom = etree.HTML(str(ip_list_info[index]))
				ip = dom.xpath('//td[2]')
				port = dom.xpath('//td[3]')
				protocol = dom.xpath('//td[6]')
				if protocol[0].text.lower() == 'https':
					_type = 2
				elif protocol[0].text.lower() == 'http':
					_type = 1
				else:
					_type = 3

				proxy_ip = ProxyIp(ip=ip[0].text, port=port[0].text, _type=_type, source='http://www.xicidaili.com/', is_alive=1, create_time=datetime.now(), update_time=datetime.now())
				proxy_list.append(proxy_ip)
		return proxy_list

		# # 初始化正则表达式
		# lose_time, waste_time = initpattern()
		# db = DBSession().get_session()
		# for i in range(len(proxy_list)):
		# 	proxy_ip = proxy_list[i]
		# 	# 检查ip
		# 	if check_ip(proxy_ip.ip, lose_time, waste_time) < 200:
		# 		res = db.query(ProxyIp).filter(and_(ProxyIp.ip == proxy_ip.ip, ProxyIp.port == proxy_ip.port))
		# 		if len(res.all()) == 0:  # 数据库不存在时,直接插入
		# 			proxy_ip = fetch_area_info(proxy_ip)
		# 			db.add(proxy_ip)
		# 		# db.add_by_sql("INSERT proxy_ip(ip, port, type, source) VALUES(%s, %s, %s, %s)", ip, port, '1', 'http://www.kuaidaili.com/')
		# 		else:  # 数据库中已有该记录,更新存活时间
		# 			proxy_ip = res.all()[0]
		# 			create_timestamp = datetime.timestamp(proxy_ip.create_time)
		# 			proxy_ip.alive_time = time.time() - create_timestamp
		# db.commit()


if __name__ == '__main__':
	# db = DBSession().get_session()
	# res = db.query(ProxyIp).filter(and_(ProxyIp.ip == '1.85.220.199', ProxyIp.port == 8118))
	# proxy_ip = res.all()[0]
	# print(datetime.datetime.timestamp(proxy_ip.create_time))
	# print(time.time())
	# print(datetime.datetime.now())
	time.sleep(60 * 25)
	while True:
		xici = Xicidaili('西刺代理')
		proxy_ip_list = xici.get_proxy_list()
		xici.save_ip_list(proxy_ip_list)
		print("西刺代理ip入库结束,共处理%s条记录" % len(proxy_ip_list))
		time.sleep(60 * 30)
