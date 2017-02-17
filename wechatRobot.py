import itchat
import myConfig
import random
import jiandan_img
import requests
import os
from itchat.content import *

# 登陆微信
itchat.auto_login(True, enableCmdQR=2)

Pic = jiandan_img.Page(jiandan_img.web_path['pic'])
pic_total_page_num = Pic.get_total_page_num()
Ooxx = jiandan_img.Page(jiandan_img.web_path['ooxx'])
ooxx_total_page_num = Ooxx.get_total_page_num()


return_msg_dict = {
    'default': '回复对应选项：\n'
               '%s\n'
               '%s'
               % (
                    '· ox 获取一张妹纸图',
                    '· pic 获取一张无聊图'
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
    if return_text == '':
        if text == 'pic':
            pic_path = get_rand_img_page('pic')
            send_img_to_user(pic_path, from_user_name)  # 发送图片给用户
            return
        if text == 'ox':
            pic_path = get_rand_img_page('ooxx')
            send_img_to_user(pic_path, from_user_name)  # 发送图片给用户
            return
    if return_text == '':
        # 给出系统默认回答
        return_text = return_msg_dict['default']
    return return_text


def get_pic_url_file_name(full_url: str):
    # 获取url对应的文件名
    return os.path.basename(full_url)


def get_rand_img_page(pic_type):
    if pic_type == 'pic':
        rand_page = random.randint(1, pic_total_page_num)
        Pic.set_page(rand_page)
        img_page_dict = Pic.get_img_path_dict()
        rand_img_path = img_page_dict[random.randint(0, img_page_dict.__len__()-1)]
    else:
        rand_page = random.randint(1, ooxx_total_page_num)
        Ooxx.set_page(rand_page)
        img_page_dict = Ooxx.get_img_path_dict()
        rand_img_path = img_page_dict[random.randint(0, img_page_dict.__len__() - 1)]
    return rand_img_path


def send_img_to_user(pic_path, from_user_name):
    file_name = get_pic_url_file_name(pic_path)
    file_save_path = './img/' + file_name
    f = open(file_save_path, 'wb')
    f.write(requests.get('http:' + pic_path).content)
    f.close()
    print('download ' + file_name + ' success')
    itchat.send_image(file_save_path, from_user_name)
    print('send ' + file_name + ' success')
    os.remove(file_save_path)
    print('remove ' + file_name + ' success')
    return True

# 注册事件


@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
def text_reply(msg):
    # 文本内容回复
    print('-------start-------')
    auto_reply = AutoReply.is_open_auto_reply()          # 是否开启了自动回复
    from_user_name = msg['FromUserName']                  # 发送者标识
    to_user_name = msg['ToUserName']                    # 接收者标识
    msg_type = msg['MsgType']
    text = msg['Text']                                  # 发送者发送的消息
    print('test', msg)
    print('from user:', from_user_name)
    print('input text: ', text)
    if to_user_name == 'filehelper':            # 处理配置信息
        itchat.send(config_set(text), to_user_name)
        return

    if not auto_reply:
        return
    if msg_type == 10000:
        return
    return get_return_msg(text, from_user_name)


@itchat.msg_register(FRIENDS)
def add_friend(msg):
    # 添加好友自动刷新微信用户列表
    itchat.add_friend(**msg['Text']) # 该操作会自动将新好友的消息录入，不需要重载通讯录
    itchat.send_msg('Nice to meet you!', msg['RecommendInfo']['UserName'])

itchat.run(debug=True)
