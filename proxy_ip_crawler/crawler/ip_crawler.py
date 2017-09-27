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
		add_list = []
		start_time = time.time()
		for proxy_ip in proxy_list:
			# 检查ip
			resp_time = check_ip(proxy_ip.ip, lose_time, waste_time)
			result = db.query(ProxyIp).filter(and_(ProxyIp.ip == proxy_ip.ip, ProxyIp.port == proxy_ip.port)).first()
			if result is None:  # 数据库不存在时,直接插入
				if resp_time < 2000:
					proxy_ip = fetch_area_info(proxy_ip)
					if proxy_ip is not None:
						proxy_ip.resp_time = resp_time
						# db.add(proxy_ip)
						add_list.append(proxy_ip)
					# db.commit()
			else:  # proxy_ip is not None and resp_time < 2000:  # 数据库中已有该记录,更新存活时间
				proxy_ip = result
				if resp_time < 2000:
					create_timestamp = datetime.timestamp(proxy_ip.create_time)
					proxy_ip.alive_time = time.time() - create_timestamp
					proxy_ip.resp_time = resp_time
				else:  # resp_time >= 2000:数据库中存在记录并且超时的,score-1
					if proxy_ip.score is None:
						proxy_ip.score = 0
					proxy_ip.score -= 1
					proxy_ip.resp_time = resp_time
			db.commit()

		end_time = time.time()
		exec_time = end_time - start_time
		print('%s代理IP查询结束,查询%s条数据耗时%s秒' % (self.name, len(proxy_list), exec_time))

		# for add_ip in add_list:
		# 	db.add(add_ip)
		# db.flush()
		start_time = time.time()
		db.bulk_save_objects(add_list)
		db.commit()
		# for update_ip in update_list:
		# 	create_timestamp = datetime.timestamp(update_ip.create_time)
		# 	update_ip.alive_time = time.time() - create_timestamp
		# db.commit()
		end_time = time.time()
		exec_time = end_time - start_time
		print('%s代理IP入库结束,共入库%s个IP,耗时%s秒' % (self.name, len(add_list), exec_time))
