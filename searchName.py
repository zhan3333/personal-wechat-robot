import itchat

itchat.auto_login(True)
# 查询筱涵的标志
info = itchat.search_friends(wechatAccount='arlene1124824924')
print('arlene1124824924: ', info[0]['UserName'])
# 查询测试账号的标志
info2 = itchat.search_friends(wechatAccount='zhannnnnnnn')
print('zhannnnnnnn: ', info2[0]['UserName'])
wechatAccount = {
    'arlene1124824924': info[0]['UserName'],
    'zhannnnnnnn': info2[0]['UserName']
}