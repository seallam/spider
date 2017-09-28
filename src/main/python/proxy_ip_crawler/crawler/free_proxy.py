import json
import sys
# import requests
# import requests.utils, pickle
from bs4 import BeautifulSoup
import os.path, os
import threading
# from multiprocessing import Process, Manager
from datetime import datetime
import traceback
import logging
import re, random
import subprocess
import shutil
import platform

output_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'proxy.txt')
global_log = 'http_proxy' + datetime.now().strftime('%Y-%m-%d') + '.log'
if not os.path.exists(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'logs')):
	os.mkdir(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'logs'))
global_log = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'logs', global_log)

logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] [%(levelname)s] [%(module)s] [%(funcName)s] [%(lineno)d] %(message)s', filename=global_log, filemode='a')
log = logging.getLogger(__name__)
# manager = Manager()
# PROXY_LIST = manager.list()
mutex = threading.Lock()
PROXY_LIST = []


def isWindows():
	if "Windows" in str(platform.uname()):
		return True
	else:
		return False


def getTagsByAttrs(tagName, pageContent, attrName, attrRegValue):
	soup = BeautifulSoup(pageContent)
	return soup.find_all(tagName, {attrName: re.compile(attrRegValue)})


def getTagsByAttrsExt(tagName, filename, attrName, attrRegValue):
	if os.path.isfile(filename):
		f = open(filename, 'r')
		soup = BeautifulSoup(f)
		f.close()
		return soup.find_all(tagName, {attrName: re.compile(attrRegValue)})
	else:
		return None


class Site1Thread(threading.Thread):
	def __init__(self, outputFilePath):
		threading.Thread.__init__(self)

		self.outputFilePath = outputFilePath
		self.fileName = str(random.randint(100, 1000)) + ".html"
		self.setName('Site1Thread')

	def run(self):
		site1_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'site.js')

		site2_file = os.path.join(self.outputFilePath, 'site.js')
		if not os.path.isfile(site2_file) and os.path.isfile(site1_file):
			shutil.copy(site1_file, site2_file)
		# proc = subprocess.Popen(["bash","-c", "cd %s && ./casperjs site.js --url=http://spys.ru/free-proxy-list/IE/ --outputfile=%s" % (self.outputFilePath,self.fileName) ],stdout=subprocess.PIPE)
		if isWindows():
			proc = subprocess.Popen(["cmd", "/c", "%s/casperjs site.js --url=http://spys.ru/free-proxy-list/IE/ --outputfile=%s" % (self.outputFilePath, self.fileName)], stdout=subprocess.PIPE)
		else:
			proc = subprocess.Popen(["bash", "-c", "cd %s && ./casperjs site.js --url=http://spys.ru/free-proxy-list/IE/ --outputfile=%s" % (self.outputFilePath, self.fileName)],
			                        stdout=subprocess.PIPE)
		out = proc.communicate()[0]
		htmlFileName = ''
		# 因为输出路径在windows不确定，所以这里加了所有可能的路径判断
		if os.path.isfile(self.fileName):
			htmlFileName = self.fileName
		elif os.path.isfile(os.path.join(self.outputFilePath, self.fileName)):
			htmlFileName = os.path.join(self.outputFilePath, self.fileName)
		elif os.path.isfile(os.path.join(os.path.dirname(os.path.realpath(__file__)), self.fileName)):
			htmlFileName = os.path.join(os.path.dirname(os.path.realpath(__file__)), self.fileName)
		if (not os.path.isfile(htmlFileName)):
			print('Failed to get html content from http://spys.ru/free-proxy-list/IE/')
			print(out)
			sys.exit(3)
		mutex.acquire()
		PROXYList = getTagsByAttrsExt('font', htmlFileName, 'class', 'spy14$')
		for proxy in PROXYList:
			tdContent = proxy.renderContents()
			lineElems = re.split('[<>]', tdContent)
			if re.compile(r'\d+').search(lineElems[-1]) and re.compile('(\d+\.\d+\.\d+)').search(lineElems[0]):
				print(lineElems[0], lineElems[-1])
			PROXY_LIST.append("%s:%s" % (lineElems[0], lineElems[-1]))
		mutex.release()
		try:
			if os.path.isfile(htmlFileName):
				os.remove(htmlFileName)
		except:
			pass


if __name__ == '__main__':
	try:
		if (len(sys.argv)) < 2:
			print("Usage:%s [casperjs path]" % (sys.argv[0]))
			sys.exit(1)
		if not os.path.exists(sys.argv[1]):
			print("casperjs path: %s does not exist!" % (sys.argv[1]))
			sys.exit(2)
		if os.path.isfile(output_file):
			f = open(output_file)
			lines = f.readlines()
			f.close
			for line in lines:
				PROXY_LIST.append(line.strip())
			thread1 = Site1Thread(sys.argv[1])
			thread1.start()
			thread1.join()

		f = open(output_file, 'w')
		for proxy in set(PROXY_LIST):
			f.write(proxy + "\n")
		f.close()
		print("Done!")
	except SystemExit:
		pass
	except:
		errMsg = traceback.format_exc()
		print(errMsg)
		log.error(errMsg)
