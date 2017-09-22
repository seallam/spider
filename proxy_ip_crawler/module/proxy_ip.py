# 导入:
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ProxyIp(Base):
	__tablename__ = 'proxy_ip'

	id = Column('id', Integer, primary_key=True)
	ip = Column(String)
	port = Column(Integer)
	country = Column(String)
	country_code = Column(String)
	province = Column(String)
	province_code = Column(String)

	city = Column(String)
	city_code = Column(String)
	district = Column(String)
	district_code = Column(String)
	type = Column(Integer)
	isAlive = Column(Integer)
	alive_time = Column(Integer)
	source = Column(String)
	create_time = Column(DateTime)
	update_time = Column(DateTime)

	def __init__(self, _id=None, ip=None, port=None, source=None, _type=None, is_alive=None, create_time=None, update_time=None):
		self.id = _id
		self.ip = ip
		self.port = port
		self.country = None
		self.province = None
		self.city = None
		self.district = None
		self.type = _type
		self.isAlive = is_alive
		self.source = source
		self.create_time = create_time
		self.update_time = update_time

	def __repr__(self):
		return "<ProxyIp('%s','%s','%s')>" % (self.id, self.ip, self.port)

# @property
# def type(self):
# 	return self._type
