import json
import random
import time

import requests
from lxml import etree

from src.main.python.tools.proxy_pre_heat import PreheatUtils


def get_price_calendar(date, proxies, logToken, rk, CK, r):
	# url = 'http://flights.ctrip.com/domesticsearch/search/SearchFirstRouteFlights?DCity1=HRB&ACity1=SHA&
	# SearchType=S&DDate1=2016-05-13&IsNearAirportRecommond=0&rk=5.189667156909168071745&CK=89D3A4A3A5F8A7F7E48ACDD1F451127A&r=0.1440474125154478474718'
	url = 'http://flights.ctrip.com/domesticsearch/search/SearchFirstRouteFlights?DCity1=CAN&ACity1=CTU&' \
	      'SearchType=S&DDate1=%s&IsNearAirportRecommond=0&LogToken=%s&' \
	      'rk=%s&CK=%s&r=%s' % (date, logToken, rk, CK, r)

	headers = {'Host': "flights.ctrip.com", 'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0",
	           'Referer': "http://flights.ctrip.com/booking/can-ctu-day-1.html?ddate1=%s" % date}
	res = requests.get(url, headers=headers, proxies=proxies)
	t = time.time()
	print(int(round(t * 1000)))  # 毫秒级时间戳
	print(url)
	print(res.cookies.get_dict())
	content = res.text
	dict_content = json.loads(content, encoding="gb2312")
	# lps = dict_content['lps']
	# return lps
	# length = len(dict_content['fis'])
	# # print length
	# for i in range(length):
	# 	# if (dict_content['fis'][i][u'lp']) < 600:
	# 		print('起飞时间:%s' % dict_content['fis'][i][u'dt']),
	# 		print('到达时间:%s' % dict_content['fis'][i][u'at'])
	# 		print('当前价格:%s' % dict_content['fis'][i][u'lp']),
		# print (dict_content['fis'][i][u'dpbn'])


def get_parameter(date, proxies):
	"""获取重要的参数
	date:日期，格式示例：2016-05-13
	"""
	url = 'http://flights.ctrip.com/booking/can-ctu-day-1.html?ddate1=%s' % date
	res = requests.get(url, proxies=proxies)
	if res.status_code == 200:
		tree = etree.HTML(res.text)
		pp = tree.xpath('''//body/script[1]/text()''')[0].split()
		CK_original = pp[3][-34:-2]
		CK = CK_original[0:5] + CK_original[13] + CK_original[5:13] + CK_original[14:]

		log_token = pp[3][-68:-36]

		rk = pp[-1][18:24]
		num = random.random() * 10
		num_str = "%.15f" % num
		rk = num_str + rk
		r = pp[-1][27:len(pp[-1]) - 3]

		return rk, CK, r, log_token
	else:
		time.sleep(5)
		return get_parameter(date=date, proxies=proxies)


if __name__ == '__main__':
	# pp = "//flights.ctrip.com/domesticsearch/search/SearchFirstRouteFlights?DCity1=CAN&ACity1=CTU&SearchType=S&DDate1=2017-10-09&IsNearAirportRecommond=0&LogToken=8e7334b180e44d4082557ee177d6a62a&CK=9E6F9DDE91389EB9DA981751C60AD849"
	# CK_original = pp[-34:-2]
	# CK = CK_original[0:5] + CK_original[13] + CK_original[5:13] + CK_original[14:]
	# print(CK)
	# LogToken = pp[-68:-36]
	# print(LogToken)
	# date = time.strftime('%Y-%m-%d', time.localtime(time.time()))  # '2017-10-09'
	date = '2017-10-10'
	url = 'http://flights.ctrip.com/'
	pre_heat = PreheatUtils(url)
	proxies = pre_heat.get_proxy_ip()
	rk, CK, r, logToken = get_parameter(date=date, proxies=proxies)
	dic = get_price_calendar(date=date, proxies=proxies, logToken=logToken, rk=rk, CK=CK, r=r)
	# print(dic)
	# for key in dic.keys():
	# 	print(key)
	# 	print(dic[key])

	# s = '{"lps":{"2017-09-28":1130,"2017-09-29":1205,"2017-09-30":1415,"2017-10-01":1390,"2017-10-02":1030,"2017-10-03":840,"2017-10-04":680,"2017-10-05":690,"2017-10-06":820,"2017-10-07":840,"2017-10-08":970,"2017-10-09":630,"2017-10-10":640,"2017-10-11":630,"2017-10-12":630,"2017-10-13":700,"2017-10-14":710,"2017-10-15":710,"2017-10-16":760,"2017-10-17":750,"2017-10-18":770,"2017-10-19":840,"2017-10-20":840,"2017-10-21":770,"2017-10-22":830,"2017-10-23":750,"2017-10-24":690,"2017-10-25":690,"2017-10-26":690,"2017-10-27":690,"2017-10-28":690,"2017-10-29":600,"2017-10-30":600,"2017-10-31":600,"2017-11-01":590,"2017-11-02":590,"2017-11-03":590,"2017-11-04":590,"2017-11-05":540,"2017-11-06":540,"2017-11-07":590,"2017-11-08":540,"2017-11-09":590,"2017-11-10":590,"2017-11-11":540,"2017-11-12":540,"2017-11-13":540,"2017-11-14":540,"2017-11-15":540,"2017-11-16":540,"2017-11-17":590,"2017-11-18":540,"2017-11-19":540,"2017-11-20":540,"2017-11-21":540,"2017-11-22":540,"2017-11-23":540,"2017-11-24":590,"2017-11-25":540,"2017-11-26":540,"2017-11-27":500,"2017-11-28":500,"2017-11-29":500,"2017-11-30":500,"2017-12-01":500,"2017-12-02":500,"2017-12-03":500,"2017-12-04":500,"2017-12-05":500,"2017-12-06":500,"2017-12-07":500,"2017-12-08":540,"2017-12-09":540,"2017-12-10":540,"2017-12-11":540,"2017-12-12":540,"2017-12-13":540,"2017-12-14":540,"2017-12-15":540,"2017-12-16":540,"2017-12-17":540,"2017-12-18":540,"2017-12-19":540,"2017-12-20":540,"2017-12-21":540,"2017-12-22":540,"2017-12-23":540,"2017-12-24":540,"2017-12-25":540,"2017-12-26":540,"2017-12-27":540,"2017-12-28":590,"2017-12-29":770,"2017-12-30":780,"2017-12-31":760,"2018-01-01":770,"2018-01-02":970,"2018-01-03":970,"2018-01-04":970,"2018-01-05":1090,"2018-01-07":970,"2018-01-10":970,"2018-01-11":1200,"2018-01-13":1200,"2018-01-14":1200,"2018-01-16":1200,"2018-01-17":1200,"2018-01-18":1200,"2018-01-20":1200,"2018-01-21":1200,"2018-01-22":1200,"2018-01-25":1200,"2018-01-27":1340,"2018-01-30":1340,"2018-01-31":1340,"2018-02-01":1420,"2018-02-02":1420,"2018-02-03":1420,"2018-02-04":1420,"2018-02-05":1420,"2018-02-06":1420,"2018-02-07":1420,"2018-02-08":1420,"2018-02-09":1420,"2018-02-10":1420,"2018-02-11":1420,"2018-02-13":1420,"2018-02-14":1420,"2018-02-15":1420,"2018-02-16":1420,"2018-02-17":1340,"2018-02-18":1340,"2018-02-19":1200,"2018-02-20":1200,"2018-02-21":1340,"2018-02-22":1340,"2018-02-24":1200,"2018-02-27":1200,"2018-02-28":1200,"2018-03-01":1420,"2018-03-02":1420,"2018-03-05":1200,"2018-03-06":1200,"2018-03-07":1200,"2018-03-08":1200,"2018-03-10":1200,"2018-03-14":1200,"2018-03-15":1200,"2018-03-18":1200,"2018-03-21":1200,"2018-03-22":1200,"2018-03-23":1200,"2018-03-27":1430,"2018-03-30":1430,"2018-04-05":1430,"2018-04-07":1430,"2018-04-19":1430,"2018-06-01":1430,"2018-06-08":1430,"2018-08-13":1430,"2018-08-14":1430}}'
	# dic = json.loads(s)
	# for key in dic['lps'].keys():
	# 	print(key)
	# 	print(dic['lps'][key])
