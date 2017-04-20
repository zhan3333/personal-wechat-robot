import itchat
import myImg
import myConfig
import TuLingRobot
import re
import random
import Sql.dialog as dialog
from itchat.content import *

# 登陆微信
itchat.auto_login(True, enableCmdQR=False)

isMeImgDirPath = 'E:/Pictures/is me/'

returnXiaoHan = {
    'default': '嘘，詹光还在睡觉，我是他的微信小管家。您可以发送以下消息，让我做出对应操作：\n'
               '%s\n'
               '%s'
               % (
                    '· 发一张詹光照片',
                    '· 添加自定义消息'
               )
}

configOption = {
    1: '开启自动回复',
    2: '关闭自动回复',
    3: '查看自动回复状态',
    0: '回复：\n'
         '1. %s\n'
         '2. %s\n'
         '3. %s'
    % ('开启自动回复', '关闭自动回复', '查看自动回复状态')
}

AutoReply = myConfig.AutoReply()


def config_set(text):
    # 设置操作
    if text == '1':
        AutoReply.open()
        return '开启自动回复成功'
    if text == '2':
        AutoReply.close()
        return '关闭自动回复成功'
    if text == '3':
        status = AutoReply.is_open_auto_reply()
        if status:
            return '自动回复：开'
        else:
            return '自动回复：关'
    if text == '0':
        return configOption[0]
    return text


def get_user_wechat_mark(name):
    # 获取用户微信标识
    user_info = itchat.search_friends(name=name)
    print(name, user_info)
    if user_info:
        mark = user_info[0]['UserName']
        print(name, mark)
        return mark
    else:
        return ''


def get_return_msg(text, from_user_name):
    # 根据消息内容，做出回复消息
    return_text = ''
    if not isinstance(text, str):
        text = ''
        return_text = '不认识图片'
    if text.find('@q#') != -1 and text.find('@s#') != -1:
        # 添加问答
        q = re.search(r'@q#\S*?#', text)
        s = re.search(r'@s#\S*?#', text)
        if q is None or s is None:
            pass
        else:
            qt = q.group()
            st = s.group()
            question = qt[3:qt.__len__()-1]
            answer = st[3:st.__len__()-1]
            print(question, answer)
            if len(dialog.query_by_question_and_answer(question, answer)) != 0:
                return_text = '问答已经存在了...'
            else:
                dialog.add(question, answer)
                return_text = '添加问答成功:\n' \
                              '问：%s\n' \
                              '答: %s' % (question, answer)

    if return_text == '':
        # 发送照片
        if text == '发一张詹光照片':
            return_text = '@%s@%s' % ('img', myImg.get_random_one_img_list(isMeImgDirPath))
        elif text == '添加自定义消息':
            itchat.send('请复制以下模板，并修改问题与答案', from_user_name)
            return_text = '@q#问题#\n@s#答案#'

    if return_text == '':
        # 根据数据库数据做出回答
        answer_list = dialog.query_by_text(text)
        if len(answer_list) != 0:
            return_text = answer_list[random.randint(0, len(answer_list)-1)].answer
            print(return_text)  # 多条答案中随机取一条答案返回

    if return_text == '':
        # 图灵机器人问答
        tu_ling_ret = TuLingRobot.query(text)
        if 'text' in tu_ling_ret:
            return_text = tu_ling_ret['text']
        if 'url' in tu_ling_ret:
            itchat.send(tu_ling_ret['url'], from_user_name)

    if return_text == '':
        # 给出系统默认回答
        return_text = returnXiaoHan['default']

    return return_text

# 需要查询标识的微信账号或名称等
wechatList = {
    'zhannnnnnnn',
    '小乖乖',
    '詹奕',
    '漫天飞雪'
}
wechatAccount = {}
for wechat_name in wechatList:
    wechatAccount[wechat_name] = get_user_wechat_mark(wechat_name)
returnUserList = {
    wechatAccount['zhannnnnnnn'],
    wechatAccount['小乖乖'],
    wechatAccount['詹奕']
}

# 注册事件


@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING, 'Picture'])
def text_reply(msg):
    # 文本内容回复
    print('-------start-------')
    auto_reply = AutoReply.is_open_auto_reply()          # 是否开启了自动回复
    from_user_name = msg['FromUserName']                  # 发送者标识
    to_user_name = msg['ToUserName']                    # 接收者标识
    text = msg['Text']                                  # 发送者发送的消息
    print('test', msg)
    print('from user:', from_user_name)
    print('input text: ', text)
    if to_user_name == 'filehelper':            # 处理配置信息
        itchat.send(config_set(text), to_user_name)
        return

    if not auto_reply:
        return
    if from_user_name in returnUserList:
        return get_return_msg(text, from_user_name)


@itchat.msg_register(FRIENDS)
def add_friend(msg):
    # 添加好友自动刷新微信用户列表
    itchat.add_friend(**msg['Text']) # 该操作会自动将新好友的消息录入，不需要重载通讯录
    itchat.send_msg('Nice to meet you!', msg['RecommendInfo']['UserName'])

itchat.run(debug=True)
