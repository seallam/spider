from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DBSession:
	DB_CONNECT_STRING = 'mysql+mysqldb://lianj:123456@127.0.0.1:3306/my_py?charset=utf8'
	session = None

	def __init__(self):
		engine = create_engine(self.DB_CONNECT_STRING, echo=True, pool_recycle=1800)
		db_session = sessionmaker(bind=engine)
		self.session = db_session()

	def get_session(self):
		return self.session

	def close(self):
		self.session.close()

	def __del__(self):
		if self.session is not None:
			self.session.close()
