from Sql.conn import *
import datetime

# dialog = Dialog(question='提一个问题', answer='好的', postTime=datetime.datetime.now(), createUser='zhan')
# session.add(dialog)
# session.commit()
ret = session.query(Dialog.id).filter(Dialog.id==2).scalar()
print(ret)