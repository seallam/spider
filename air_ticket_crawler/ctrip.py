import json
import random

import time
from lxml import etree

import requests

from database.redis.RedisDB import RedisDB
from tools.proxy_pre_heat import pre_heat, PreheatUtils


def get_json(date, proxies, rk, CK, r):
	# url = 'http://flights.ctrip.com/domesticsearch/search/SearchFirstRouteFlights?DCity1=HRB&ACity1=SHA&
	# SearchType=S&DDate1=2016-05-13&IsNearAirportRecommond=0&rk=5.189667156909168071745&CK=89D3A4A3A5F8A7F7E48ACDD1F451127A&r=0.1440474125154478474718'
	url = 'http://flights.ctrip.com/domesticsearch/search/SearchFirstRouteFlights?DCity1=CAN&ACity1=CTU&' \
	      'SearchType=S&DDate1=%s&IsNearAirportRecommond=0&LogToken=4b57f234e0814617b91d6c60974b8be2&' \
	      'rk=%s&CK=%s&r=%s' % (date, rk, CK, r)

	headers = {'Host': "flights.ctrip.com", 'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0",
	           'Referer': "http://flights.ctrip.com/booking/can-ctu-day-1.html?ddate1=%s" % date}
	res = requests.get(url, headers=headers, proxies=proxies)
	content = res.text
	dict_content = json.loads(content, encoding="gb2312")
	length = len(dict_content['fis'])
	# print length
	for i in range(length):
		# if (dict_content['fis'][i][u'lp']) < 600:
			print('起飞时间:%s' % dict_content['fis'][i][u'dt']),
			print('到达时间:%s' % dict_content['fis'][i][u'at'])
			print('当前价格:%s' % dict_content['fis'][i][u'lp']),
		# print (dict_content['fis'][i][u'dpbn'])


def get_parameter(date, proxies):
	"""获取重要的参数
	date:日期，格式示例：2016-05-13
	"""
	url = 'http://flights.ctrip.com/booking/hrb-sha-day-1.html?ddate1=%s' % date
	res = requests.get(url, proxies=proxies)
	if res.status_code == 200:
		tree = etree.HTML(res.text)
		pp = tree.xpath('''//body/script[1]/text()''')[0].split()
		CK_original = pp[3][-34:-2]
		CK = CK_original[0:5] + CK_original[13] + CK_original[5:13] + CK_original[14:]

		rk = pp[-1][18:24]
		num = random.random() * 10
		num_str = "%.15f" % num
		rk = num_str + rk
		r = pp[-1][27:len(pp[-1]) - 3]

		return rk, CK, r
	else:
		time.sleep(5)
		return get_parameter(date=date, proxies=proxies)


if __name__ == '__main__':
	date = '2017-10-09'
	url = 'http://flights.ctrip.com/'
	pre_heat = PreheatUtils(url)
	proxies = pre_heat.get_proxy_ip()
	rk, CK, r = get_parameter(date=date, proxies=proxies)
	get_json(date=date, proxies=proxies, rk=rk, CK=CK, r=r)
