import requests


def pre_heat(*proxy_ips, url, num=100):
	print('即将预热网站%s' % url)
	success_ip = []
	for proxy_ip in proxy_ips:
		if proxy_ip.type == 1:
			prototype = 'http'
		else:
			prototype = 'https'
		proxy_str = '%s://%s:%s' % (prototype, proxy_ip.ip, proxy_ip.port)
		proxies = {
			prototype: proxy_str
		}
		response = requests.get(url, proxies=proxies)
		if response.status_code == 200:
			# 保存预热成功的ip
			if len(success_ip) == num:
				print('网站%s预热结束,即将返回结果' % url)
				pass
			success_ip.append(proxy_ip)
	return success_ip
