import pymysql


class DB:
	conn = None

	def __init__(self):
		self.conn = pymysql.connect(host='127.0.0.1', port=3306, user='lianj', passwd='123456', db='my_py', charset='utf8')

	def get_by_sql(self, sql, *param):
		cursor = self.conn.cursor()  # 初始化游标
		result = cursor.fetchmany(cursor.execute(sql, param))
		self.conn.commit()  # 提交上面的sql语句到数据库执行
		return result

	def get_unique_by_sql(self, sql, *param):
		cursor = self.conn.cursor()  # 初始化游标
		result = cursor.fetchmany(cursor.execute(sql, param))
		self.conn.commit()  # 提交上面的sql语句到数据库执行
		return result[0][0]

	def add_by_sql(self, sql, *param):
		cursor = self.conn.cursor()  # 初始化游标
		cursor.execute(sql, param)
		self.conn.commit()  # 提交上面的sql语句到数据库执行

	# 带参数的更新方法,eg:sql='insert into pythontest values(%s,%s,%s,now()',params=(6,'C#','good book')
	def update_by_sql(self, sql, *param):
		cur = self.conn.cursor()
		count = cur.execute(sql, param)
		self.conn.commit()
		return count
