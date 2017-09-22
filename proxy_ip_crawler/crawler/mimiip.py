import time

from proxy_ip_crawler.ip_crawler import IpCrawler
import requests


class Mimiip(IpCrawler):
	def get_proxy_list(self):
		proxy_url = 'http://www.mimiip.com/gngao/%s'
		for i in range(1, 3):
			response = requests.get(proxy_url % str(i))
			html = response.text
			time.sleep(2)

		proxy_list = []
		return proxy_list


if __name__ == '__main__':
	mimiip = Mimiip('秘密代理')
	mimiip.get_proxy_list()
