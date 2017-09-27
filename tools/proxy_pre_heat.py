import json
import random
from datetime import datetime

import requests
import time

from database.mysql.MySQLDBSession import DBSession
from database.mysql.entity.proxy_ip import ProxyIp
from database.redis.RedisDB import RedisDB


def pre_heat(url, num=50):
	print('即将预热网站%s' % url)
	host = get_host(url)
	success_ip = []
	redis = RedisDB().get_redis()
	mysql = DBSession().get_session()
	proxy_ips = mysql.query(ProxyIp).filter(ProxyIp.source != url).all()
	flag = True
	count = 0
	while flag:
		i = random.randint(0, len(proxy_ips) - 1)
		if count != 0 and count % 5 == 0:
			print('已经执行了%s次' % count)
		proxy_ip = proxy_ips[i]
		proxy_ips.remove(proxy_ip)
		if proxy_ip.type == 1:
			prototype = 'http'
		else:
			prototype = 'https'
		proxy_str = '%s://%s:%s' % (prototype, proxy_ip.ip, proxy_ip.port)
		proxies = {
			prototype: proxy_str
		}
		if proxy_ip.score is None:
			score = 0
		else:
			score = proxy_ip.score
		try:
			header = {
				'cache-control': "no-cache",
				'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'
			}
			response = requests.get(url, headers=header, proxies=proxies, timeout=5)
			if response.status_code == 200:
				# 保存预热成功的ip
				success_ip.append(proxy_ip)
				# 更新分数
				proxy_ip.score = score + 1
				# 更新存活时间
				create_timestamp = datetime.timestamp(proxy_ip.create_time)
				proxy_ip.alive_time = time.time() - create_timestamp
				# 保存到redis
				obj = {
					"ip": proxy_ip.ip,
					"port": proxy_ip.port,
					"source": proxy_ip.source,
					"prototype": prototype
				}
				redis.zadd(host, json.dumps(obj), time.time())
			else:  # 获取网页内容失败(超时等)
				print(response.status_code)
				proxy_ip.score = proxy_ip.score - 1
		except:
			proxy_ip.score = score - 1
		count += 1
		if redis.zcard(host) >= num or count >= 1500:  # 预热得到足够的数据后跳出循环
			print('网站%s预热结束,即将返回结果' % url)
			flag = False

	mysql.commit()
	redis.expire(host, 60 * 60 * 24 * 2)  # 数据保存2天
	return success_ip


def get_host(url):
	return str(url).replace('http', '').replace('https', '').replace('://', '').replace('/', '')


def random_int_list(start, stop, length):
	start, stop = (int(start), int(stop)) if start <= stop else (int(stop), int(start))
	length = int(abs(length)) if length else 0
	random_list = []
	for i in range(length):
		random_list.append(random.randint(start, stop))
	return random_list


if __name__ == '__main__':
	# db = DBSession().get_session()
	# result = db.query(ProxyIp)
	# print(dict(result.all()))
	# random_list = random_int_list(0, len(result.all()), 110)
	# # print(random_list)
	# proxy_ips = db.query(ProxyIp).filter(ProxyIp.id.in_(random_list))
	# print(len(proxy_ips.all()))
	# redis = RedisDB().get_redis()
	# redis.zadd('test', 'test', time.time())
	# pre_heat('http://flights.ctrip.com/')
	# pre_heat('http://sbj.saic.gov.cn/', 50)
	pre_heat('http://ent.kuaidaili.com/', 50)
	# pre_heat('https://www.tianyancha.com/')
