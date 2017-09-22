import json

import requests
from sqlalchemy import func

from database.MySQLDBSession import DBSession
from proxy_ip_crawler.module.proxy_ip import ProxyIp


def fetch_area_info(proxy_ip, db):
	# print(type(proxy_ip))
	fetch_url = f'http://ip.taobao.com/service/getIpInfo.php?ip={proxy_ip.ip}'
	response = requests.request('GET', fetch_url)
	result = json.loads(response.text)
	if result['code'] == 0:
		proxy_ip.country = result['data']['country']
		proxy_ip.country_code = result['data']['country_id']
		proxy_ip.province = result['data']['region']
		proxy_ip.province_code = result['data']['region_id']
		proxy_ip.city = result['data']['city']
		proxy_ip.city_code = result['data']['city_id']
		db.commit()


def fetch_area_info(proxy_ip):
	fetch_url = f'http://ip.taobao.com/service/getIpInfo.php?ip={proxy_ip.ip}'
	response = requests.request('GET', fetch_url)
	result = json.loads(response.text)
	if result['code'] == 0:
		proxy_ip.country = result['data']['country']
		proxy_ip.country_code = result['data']['country_id']
		proxy_ip.province = result['data']['region']
		proxy_ip.province_code = result['data']['region_id']
		proxy_ip.city = result['data']['city']
		proxy_ip.city_code = result['data']['city_id']
		return proxy_ip


if __name__ == '__main__':
	session = DBSession().get_session()
	total = session.query(func.count(ProxyIp.id)).scalar()
	pageSize = 10
	page = int(total / pageSize) + (0 if total % pageSize == 0 else 1)
	for i in range(page):
		res = session.query(ProxyIp).order_by(ProxyIp.id).limit(pageSize).offset(i * pageSize)
		# print(len(result.all()))
		for j in range(len(res.all())):
			print('正在执行第%s/%s条记录', j, pageSize)
			# print(result.all()[j])
			fetch_area_info(res.all()[j], session)
	# result = session.query(ProxyIp)
	# result.order_by('id')
	# result.offset(5)
	# result.limit(10)
	# db = DB()
	# res = db.get_by_sql("SELECT * FROM proxy_ip")
	# total = len(result.all())
	# for i in range(total):
	# 	print('正在执行第%d/%d条记录', i, total)
	# 	fetch_area_info(result.all()[i])


