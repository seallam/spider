from urllib import request
import pymysql

if __name__ == '__main__':
	proxy_url = 'http://ent.kuaidaili.com/api/getproxy/?orderid=990037345175795&num=500&b_pcchrome=1&b_pcie=1&b_pcff=1&protocol=1&method=2&an_ha=1&sp1=1&sp2=1&sep=1'
	proxy_url_request = request.urlopen(proxy_url)
	proxy_url_response = proxy_url_request.read().decode('utf-8')
	print(proxy_url_response)

	# conn = pymysql.connect(host='127.0.0.1', port=3306, user='lianj', passwd='123456', db='lianj_data_center', charset='utf-8')

