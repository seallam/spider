import time
from datetime import datetime

from sqlalchemy import and_

from database.mysql.MySQLDBSession import DBSession
from database.mysql.entity.proxy_ip import ProxyIp
from proxy_ip_crawler.check_ip import initpattern, check_ip
from proxy_ip_crawler.fetch_area_info import fetch_area_info


class IpCrawler(object):
	name = None

	def __init__(self, name):
		self.name = name
		pass

	def get_proxy_list(self):
		pass

	def save_ip_list(self, proxy_list):
		# 初始化正则表达式
		lose_time, waste_time = initpattern()
		print("获取%sip结束,即将执行入库,共有%s条数据,即将执行入库" % (self.name, len(proxy_list)))
		db = DBSession().get_session()
		for proxy_ip in proxy_list:
			# 检查ip
			if check_ip(proxy_ip.ip, lose_time, waste_time) < 200:
				res = db.query(ProxyIp).filter(and_(ProxyIp.ip == proxy_ip.ip, ProxyIp.port == proxy_ip.port))
				if len(res.all()) == 0:  # 数据库不存在时,直接插入
					proxy_ip = fetch_area_info(proxy_ip)
					db.add(proxy_ip)
				else:  # 数据库中已有该记录,更新存活时间
					proxy_ip = res.all()[0]
					create_timestamp = datetime.timestamp(proxy_ip.create_time)
					proxy_ip.alive_time = time.time() - create_timestamp
		db.commit()

