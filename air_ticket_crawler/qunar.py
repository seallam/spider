from database.MySQLDBSession import DBSession
from proxy_ip_crawler.module.proxy_ip import ProxyIp
from tools.proxy_pre_heat import pre_heat

# 预热ip
session = DBSession().get_session()
result = session.query(ProxyIp)
# print(result.all())
pre_heat(result.all(), 'https://www.qunar.com/')
# response = requests.get('https://www.qunar.com/')
# print(response.text)




