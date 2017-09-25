# 导入:
import json

from sqlalchemy import Column, String, Integer, DateTime, Numeric
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
	score = Column(Integer, default=0)
	source = Column(String)
	create_time = Column(DateTime)
	update_time = Column(DateTime)

	def __init__(self, _id=None, ip=None, port=None, source=None, _type=None, is_alive=None, score=0, create_time=None, update_time=None):
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
		self.score = score
		self.create_time = create_time
		self.update_time = update_time

	def __repr__(self):
		return "<ProxyIp('%s','%s','%s')>" % (self.id, self.ip, self.port)

	# def _gen_tuple(self):
	# 	def convert_datetime(value):
	# 		if value:
	# 			return value.strftime("%Y-%m-%d %H:%M:%S")
	# 		else:
	# 			return ""
	#
	# 	for col in self.__table__.columns:
	# 		if isinstance(col.type, DateTime):
	# 			value = convert_datetime(getattr(self, col.name))
	# 		elif isinstance(col.type, Numeric):
	# 			value = float(getattr(self, col.name))
	# 		else:
	# 			value = getattr(self, col.name)
	# 		yield (col.name, value)
	#
	# def to_dict(self):
	# 	return dict(self._gen_tuple())
	#
	# def to_json(self):
	# 	return json.dumps(self.to_dict())
	#
	# Base._gen_tuple = _gen_tuple
	# Base.to_dict = to_dict
	# Base.to_json = to_json
# @property
# def type(self):
# 	return self._type
