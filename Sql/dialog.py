from Sql.conn import *
import datetime


def add(question, answer, postTime = datetime.datetime.now(), createUser = ''):
    # 添加一条数据
    session.add(Dialog(question=question, answer=answer, postTime=postTime, createUser=createUser))
    session.commit()


def query_by_text(text):
    # 查询数据
    return session.query(Dialog).filter(Dialog.question == text).all()


def query_by_question_and_answer(question, answer):
    return session.query(Dialog).filter(Dialog.question == question, Dialog.answer == answer).all()