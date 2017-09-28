import re
import subprocess as sp

"""
函数说明:检查代理IP的连通性
Parameters:
    ip - 代理的ip地址
    lose_time - 匹配丢包数
    waste_time - 匹配平均时间
Returns:
    average_time - 代理ip平均耗时
Modify:
    2017-05-27
"""


def check_ip(ip, lose_time, waste_time):
	# 命令 -n 要发送的回显请求数 -w 等待每次回复的超时时间(毫秒)
	cmd = "ping -n 3 -w 3 %s"
	# 执行命令
	p = sp.Popen(cmd % ip, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE, shell=True)
	# 获得返回结果并解码
	out = p.stdout.read().decode("gbk")
	# 丢包数
	lose_time = lose_time.findall(out)
	# 当匹配到丢失包信息失败,默认为三次请求全部丢包,丢包数lose赋值为3
	if len(lose_time) == 0:
		lose = 3
	else:
		lose = int(lose_time[0])
	# 如果丢包数目大于2个,则认为连接超时,返回平均耗时1000ms
	if lose > 2:
		# 返回False
		return 1000
	# 如果丢包数目小于等于2个,获取平均耗时的时间
	else:
		# 平均时间
		average = waste_time.findall(out)
		# 当匹配耗时时间信息失败,默认三次请求严重超时,返回平均好使1000ms
		if len(average) == 0:
			return 1000
		else:
			#
			average_time = int(average[0])
			# 返回平均耗时
			return average_time


"""
函数说明:初始化正则表达式
Parameters:
    无
Returns:
    lose_time - 匹配丢包数
    waste_time - 匹配平均时间
Modify:
    2017-05-27
"""


def initpattern():
	# 匹配丢包数
	lose_time = re.compile(u"丢失 = (\d+)", re.IGNORECASE)
	# 匹配平均时间
	waste_time = re.compile(u"平均 = (\d+)ms", re.IGNORECASE)
	return lose_time, waste_time
