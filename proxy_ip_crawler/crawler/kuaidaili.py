import time
from datetime import datetime

from selenium import webdriver

from database.mysql.entity.proxy_ip import ProxyIp
from proxy_ip_crawler.ip_crawler import IpCrawler


class Kuaidaili(IpCrawler):
	def get_proxy_list(self):
		print('即将执行快代理ip获取')
		# proxy_url = "http://ent.kuaidaili.com/api/getproxy/?orderid=990037345175795&num=500&b_pcchrome=1&b_pcie=1&b_pcff=1&protocol=1&method=2&an_ha=1&sp1=1&sp2=1&sep=1"
		#
		# response = requests.request("GET", url=proxy_url)
		#
		# if response.status_code == 200:
		# 	ip_list = response.text.split('\n')
		# 	parse_list(ip_list)
		# 	print("快代理ip入库结束")
		# else:
		# 	print('快代理请求ip失败,状态码%s' % response.status_code)
		# 	response = requests.request("GET", url=proxy_url)
		# 	ip_list = response.text.split('\n')
		# 	parse_list(ip_list)
		proxy_url = 'http://www.kuaidaili.com/free/inha/'
		browser = webdriver.Chrome("F:\dev\python\lib\selenium\chromedriver.exe")
		# browser = webdriver.PhantomJS("F:\dev\python\lib\selenium\phantomjs.exe")
		proxy_list = []
		for i in range(1, 5):
			browser.get(proxy_url + str(i))
			browser.implicitly_wait(3)
			elements = browser.find_elements_by_xpath('//tbody/tr')  # 找到每个代理的位置
			for element in elements:
				ip = element.find_element_by_xpath('./td[1]').text
				port = element.find_element_by_xpath('./td[2]').text
				# anonymous = element.find_element_by_xpath('./td[3]').text
				protocol = element.find_element_by_xpath('./td[4]').text
				# speed = element.find_element_by_xpath('./td[5]').text
				if protocol.lower() == 'https':
					_type = 2
				elif protocol.lower() == 'http':
					_type = 1
				else:
					_type = 3
				proxy_ip = ProxyIp(ip=ip, port=port, _type=_type, source='http://www.kuaidaili.com/', is_alive=1, create_time=datetime.now(), update_time=datetime.now())
				proxy_list.append(proxy_ip)
		time.sleep(5)
		browser.quit()
		return proxy_list


# def parse_list(ip_list):
# 	# 初始化正则表达式
# 	lose_time, waste_time = initpattern()
# 	print("获取快代理ip结束,即将执行入库,共有%s个ip" % len(ip_list))
# 	for ip_port in ip_list:
# 		ip = ip_port.split(":")[0]
# 		port = ip_port.split(":")[1]
#
# 		# 检查ip
# 		if check_ip(ip, lose_time, waste_time) < 200:
# 			db = DBSession().get_session()
# 			res = db.query(ProxyIp).filter(and_(ProxyIp.ip == ip, ProxyIp.port == port))
# 			if len(res.all()) == 0:  # 数据库不存在时,直接插入
# 				proxy_ip = ProxyIp(ip=ip, port=port, _type=1, source='http://www.kuaidaili.com/', is_alive=1, create_time=datetime.now(), update_time=datetime.now())
# 				proxy_ip = fetch_area_info(proxy_ip)
# 				db.add(proxy_ip)
# 				db.commit()
# 			# db.add_by_sql("INSERT proxy_ip(ip, port, type, source) VALUES(%s, %s, %s, %s)", ip, port, '1', 'http://www.kuaidaili.com/')
# 			else:  # 数据库中已有该记录,更新存活时间
# 				proxy_ip = res.all()[0]
# 				create_timestamp = datetime.timestamp(proxy_ip.create_time)
# 				proxy_ip.alive_time = time.time() - create_timestamp
# 				db.commit()


if __name__ == '__main__':
	while True:
		kuai = Kuaidaili('快代理')
		proxy_ip_list = kuai.get_proxy_list()
		kuai.save_ip_list(proxy_ip_list)
		print("快代理ip入库结束,共处理了%s个ip" % len(proxy_ip_list))
		time.sleep(60 * 30)
