from proxy_ip_crawler.crawler.ip_crawler import IpCrawler


class Mayidaili(IpCrawler):
	def get_proxy_list(self):
		proxy_list = []
		return proxy_list


if __name__ == '__main__':
	mayi = Mayidaili('蚂蚁代理')
	mayi.get_proxy_list()
