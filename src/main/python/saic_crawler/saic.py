import json
import random

from selenium import webdriver

from database.redis.RedisDB import RedisDB

if __name__ == '__main__':
	redis = RedisDB().get_redis()
	zcount = redis.zcard('sbj.saic.gov.cn')
	zset = redis.zrange('sbj.saic.gov.cn', 0, zcount)
	# for i in range(len(zset)):
	# 	ip_json = json.loads(zset[i])
	# 	print(ip_json)
	ip_json = json.loads(zset[random.randint(0, zcount)])
	enter_url = 'http://sbj.saic.gov.cn/sbcx/'
	# chrome_options = webdriver.ChromeOptions()
	# chrome_options.add_argument('--proxy-server=%s://%s:%s' % (ip_json['prototype'], ip_json['ip'], ip_json['port']))
	# browser = webdriver.Chrome("F:\dev\python\lib\selenium\chromedriver.exe", chrome_options=chrome_options)
	# browser.set_page_load_timeout(5)
	# browser.set_script_timeout(5)
	browser = webdriver.Chrome("F:\dev\python\lib\selenium\chromedriver.exe")
	# service_args = [
	# 	'--proxy=%s:%s' % (ip_json['ip'], ip_json['port']),
	# 	# '--proxy-auth=user:pwd',
	# 	'--proxy-type=%s' % ip_json['prototype']
	# ]
	# browser = webdriver.PhantomJS('F:\dev\python\lib\selenium\phantomjs.exe', service_args=service_args)

	browser.get(enter_url)
	browser.implicitly_wait(5)

	browser.find_element_by_css_selector('.TRS_Editor').find_element_by_tag_name('a').click()
	browser.implicitly_wait(5)
	browser.find_element_by_css_selector('.left_side')[1].find_element_by_tag_name('table').click()

