# coding=utf-8

import requests
import json

api = 'http://www.tuling123.com/openapi/api'
api_key = '85f4ddf07d984851b5b065e8e52f7f7c'


def query(info, userid=''):
    r = requests.post(api, json={'key': api_key, 'info': info, 'userid': userid})
    return_dict = json.loads(r.text)
    return return_dict

if __name__ == '__main__':
    ret = query('小狗的图片')
    print(ret)
