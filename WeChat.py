import itchat
import requests
import json
import user
import WeiBo

# from Twitterdown import *

KEY = '415151e48d6a4860884edaa26392f481'
KEYWORD2 = u'hiahia~感谢使用We-Bo。\n您可以发送【菜单】呼出使用指南哟~\n您可以使用以下功能：\
                            \n1.获取最新微博消息请发送【最新微博】\
                            \n2.回复【关闭聊天机器人】可关闭自动聊天功能（回复【开启聊天】可开启）\
                            \n3.回复【最新微博+条数（数字）  eg：最新微博+3】可获得符合数量的最新消息'
KEYWORD = u'hiahia~感谢使用We-Twitter。\n您可以发送【菜单】呼出使用指南哟~\n您可以使用以下功能：\
                            \n1.按照格式【我想关注+XXX(您想关注的推特账号）+的推特】（加号不可省略哟）\
                            \n2.回复【关闭聊天机器人】可关闭自动聊天功能（回复【开启聊天】可开启）\
                            \n3.回复【Twitter热门账户推荐】可进入最新最热的推文推荐'
ADD_NEWUSER_TALK = '欢迎使用本系统，请回复【新用户添加】+【想要长期关注的推特账号列表（以’,‘（英文逗号）连接，如：Donald J. Trump,Robert ' \
                   'Downey JR)，可以为空 】(【】不需要）'

ADD_NEWUSER_TALK2 = '欢迎使用本系统，请回复【新用户添加】，开始使用本系统~'
robot_mode = True


def toadd_focus(username, addlist):
    # return new tweet
    # add the focus to the user's list
    # get_new_tweets(username,number)
    user.add_focus(username, addlist)


# def add_newuser1(username, nickname, user_list):
#     # add to userlist
#     print('log: username:')
#     print(username)
#     print('log: nikename:')
#     print(nickname)
#     print('log: userlist:')
#     print(user_list)
#     add_newuser(username, nickname, user_list)


def add_newuser(username, nikename, message):
    try:
        code = message.split('=')[-1]
        print('code is =' + code)
        userwbinfo = WeiBo.make_new_user(code)
        print(type(userwbinfo))
        dic = {
            'username': username,
            'nikename': nikename,
            # 'access_token':userwbinfo['access_token']
        }
        dic.update(userwbinfo)
        print(dic)
        user.savenew_user(username, dic)
        return True
    except:
        print('logs(inWeChat add_newuser) :error')


'''机器人部分'''


# get_response  (text ) /暂时/  return 机器人回复
def get_response(msg):
    # 利用图灵机器人的api实现自动回复功能，就避免自己一点一点写一堆回复了。
    # POST 发送 DATA 暂未区分图文声音，待补全。开发文档：https://www.kancloud.cn/turing/www-tuling123-com/718227
    print("log: get_response had been used")
    api = 'http://openapi.tuling123.com/openapi/api/v2'
    dat = {
        "perception": {
            "inputText": {
                "text": msg
            },
            "inputImage": {
                "url": "imageUrl"
            },
            "selfInfo": {
                "location": {
                    "city": "北京",
                    "province": "北京",
                    "street": "东门"
                }
            }
        },
        "userInfo": {
            "apiKey": KEY,
            "userId": "fool"
        }
    }
    dat = json.dumps(dat)
    r = requests.post(api, data=dat).json()
    # print(r)
    # 返回的json内容一堆用不上的，就用其中text也是醉了
    # {'emotion': {'userEmotion': {'emotionId': 10300, 'd': 0, 'p': 0, 'a': 0},
    #              'robotEmotion': {'emotionId': 0, 'd': 0, 'p': 0, 'a': 0}},
    #  'intent': {'code': 10004, 'actionName': '', 'intentName': ''},
    # 'results': [{'resultType': 'text', 'values': {'text': '别兴奋别兴奋，很高兴认识你！'}, 'groupType': 1}]}
    mesage = r['results'][0]['values']['text']
    print('log: this is message in get resonse of turing robot :' + mesage)
    return mesage


'''itchat部分'''


# 开始和结束，完全不重要，算是个提示吧
def login():
    print("start working")


def ext():
    itchat.send('老铁注意啦,程序结束啦', '@b097dea2b0373bbeb1e73931e1f5c604005e870d9b2744652dd1fb0c8c1f11b3')
    print("end working")


# itchat.content.NOTE 系统消息，比如撤回  card ，名片消息 ATTACHMENT，文件
# 检测到该用户没有添加消息时候将会提示
@itchat.msg_register([itchat.content.MAP, itchat.content.CARD, itchat.content.PICTURE, itchat.content.RECORDING,
                      itchat.content.ATTACHMENT, itchat.content.VIDEO, itchat.content.FRIENDS, itchat.content.SYSTEM, ])
def simple_reply(msg):
    # print(msg)
    # print(msg['Type'])
    reply = (u"暂时无法识别" + msg['Type'] + u"哟~请发送文字(づ￣3￣)づ╭❤～")
    if not user.in_user_list(msg.get('FromUserName')):
        itchat.send(ADD_NEWUSER_TALK2, msg.get('FromUserName'))
    return reply


# text 部分注册信息，基本回复处理
@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):
    print("log: text here had somethings\n")
    print(msg)
    message = msg['Text']
    print('message is :' + message)
    username = msg.get('FromUserName')
    print('log: username=' + username)
    # if a new user
    if not user.in_user_list(username) and not ('新用户添加' in message) and not ('code=' in message):
        replay = ADD_NEWUSER_TALK2
        return replay
    # new user add part
    if '新用户添加' in message:
        # message_list = message.split('+')
        # print(message_list)
        # if len(message_list) == 1:
        #     print('logq')
        #     focus_list = []
        # else:
        #     focus_list = message_list[1].split(',')
        # print('log: focuslist')
        # print(focus_list)
        # nikename = itchat.search_friends(userName=msg['FromUserName'])['NickName']
        # add_newuser(username, nikename, focus_list)
        url = WeiBo.GET_UESER_URL
        re_msg = u'使用本功能需要得到微博授权哟~,点击网页进行授权,授权成功后复制网址链接回复到窗口哟~：' + url
        return re_msg
    if 'code=' in message and 'http' in message:
        nikename = itchat.search_friends(userName=msg['FromUserName'])['NickName']
        if add_newuser(username, nikename, message):
            return u'授权成功，机器人默认开启，请随意调戏哟~'
        return u'授权失败，联系本人吧'
    thisuser = user.get_user(username)
    # robot_mode part
    if user.get_user_robotmode(thisuser):
        replay = get_response(message)
    else:
        replay = None
    if '聊天' in message:
        if '开启' in message:
            user.chg_robotmode(thisuser, True)
            replay = u'开启成功，请随意调戏'
        elif '关闭' in message:
            user.chg_robotmode(thisuser, False)
            replay = u'关闭成功'
    elif replay == message:
        replay = u"不太懂你在说什么嘛~不过可以：\n" + KEYWORD2

    # 微博部分
    if (u'最新微博' in message):
        if '+' in message:
            count = int(message.split('+')[-1])
            replay = WeiBo.get_newTimeLine(username,count=count)
        else:
            replay = WeiBo.get_newTimeLine(username,1)
        for info in replay:
            if info[0] == 'text':
                itchat.send(info[1], username)
            elif info[0] == 'pic':
                itchat.send_image(info[1], username)
        replay = '以上为最新消息~'
    # if ('获取')

    # twitter function part
    # if (u'推特' in message) or (u'twitter' in message) or (u'Twitter' in message) or (u'菜单' in message):
    #     replay = KEYWORD
    #     if '我想关注' in message:
    #         fous_username = message.split('+')[1]
    #         toadd_focus(username, fous_username)

    return replay


def wechat_begin():
    itchat.auto_login(loginCallback=login, exitCallback=ext, hotReload=True)
    print('Nice to start testing ,I AM BUGGER')
    itchat.send('hello,程序启动啦', '@b097dea2b0373bbeb1e73931e1f5c604005e870d9b2744652dd1fb0c8c1f11b3')
    # itchat.send('hello', '@89445c069241e9e17b916e24269e0c069642710095a2fbbedc079ecfe378eb04')   不知为何不能发送消息给自己  蓝瘦


def wechat_run():
    itchat.run()

user.main()
wechat_begin()
wechat_run()
