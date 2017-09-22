import time
from selenium import webdriver

chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--proxy-server=http://223.241.118.111:8010')
# browser = webdriver.Chrome("F:\dev\python\lib\selenium\chromedriver.exe", chrome_options=chrome_options)
browser = webdriver.Chrome('F:\dev\python\lib\selenium\chromedriver.exe')
# service_args = [
# 	'--proxy=223.241.118.111:8010',
# 	# '--proxy-auth=user:pwd',
# 	'--proxy-type=https'
# ]
# browser = webdriver.PhantomJS('F:\dev\python\lib\selenium\phantomjs.exe', service_args=service_args)

browser.get('https://flight.qunar.com/twell/flight/tags/onewayflight_groupdata.jsp?departureCity=%E5%B9%BF%E5%B7%9E&arrivalCity=%E6%88%90%E9%83%BD&departureDate=2017-09-24&returnDate=2017-09-24&nextNDays=0&searchType=OneWayFlight&searchLangs=zh&locale=zh&flightCode=&fxmulti=true&ex_track=&from=flight_dom_search&queryID=10.86.213.130:2a3a37bc:15ea73ba2f9:-3efb&status='+str(time.time())+'&isNewInterface=true&deduce=true')

browser.implicitly_wait(3)
element = browser.find_element('body')
print(element)
