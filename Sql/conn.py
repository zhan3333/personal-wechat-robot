# 导入:
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 初始化数据库连接:
engine = create_engine('mysql+mysqlconnector://root:zhan@localhost:3306/personal-wechat-robot', echo=True)

Base = declarative_base()
metadata = MetaData(engine)


class Dialog(Base):
    __tablename__ = 'dialogs'

    id = Column(Integer, primary_key=True)
    question = Column(String(255))
    answer = Column(String(255))
    postTime = Column(TIMESTAMP)
    createUser = Column(String(255))

    def __repr__(self):
        return "<Dialog(question='%s', answer='%s', postTime='%s', createUser='%s')>" % (self.question, self.answer, self.postTime, self.createUser)

# dialog_table = Dialog.__table__
Base.metadata.create_all(engine)    # 当表不存在时创建表

Session = sessionmaker(bind=engine)
session = Session()
