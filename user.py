import json

"""
初期使用简单的列表直接构造即可，后期可考虑并行问题，
使用类进行在线的数据统计和数据库记录用户数据，目前还不用。
"""
FILE = 'userinfo.json'
user_number = 0
# user_list = {'WT':
#                  {'username': '@e200cc6d0c446c7dd2efd98e5424e2df990a4379c123be4796920b2e8176b55e',
#                   'nikename': 'WT', 'robot_mode': True, 'access_token': '2.00EeAykBfSv8zCbc1f8224abfxU1fE'}}
user_list ={}

def get_access_token(nikename):
    return user_list[nikename]['access_token']


def updatelist(nikename, thisuser):
    user_list.update({nikename: thisuser})
    down_userlist()
    return True


# 昵称查询用户
def get_user_username(nikename):
    try:
        return user_list[nikename]
    except:
        return u'没有这个人呢~'


def chg_robotmode(thisuser, to):
    thisuser['robot_mode'] = to
    print('changemode')
    # print(thisuser)
    updatelist(thisuser['nikename'], thisuser)


# 查询用户昵称
def get_user_nikename(thisuser):
    return thisuser['NickName']


# 这人在不在用户列表里
def in_user_list(nikename, username):
    if nikename in user_list:
        list = user_list[nikename]
        if not list['username'] == username:
            list['username'] = username
            updatelist(nikename, list)
        return True
    else:
        return False


# 获得thisuser的机器人开关模式
def get_user_robotmode(thisuser):
    return thisuser['robot_mode']


# 获得thisuser的关注列表
def get_user_focuslist(thisuser):
    return thisuser['focus_list']


# 添加新关注对象
def add_focus(nikename, addlist):
    user = get_user(nikename)
    for addname in addlist:
        if addname in get_user_focuslist(user):
            continue
        user['focus_list'] += [addname]
    updatelist(nikename, user)
    return None


# 新用户添加  1已弃用
def savenew_user1(username, nickname, focus_list):
    # print('old userlist:')
    # print(user_list)
    new = {'UserName': username, 'NickName': nickname, 'robot_mode': True, 'focus_list': focus_list}
    global user_number
    user_number += 1
    updatelist(username, new)
    print('new userlist:')
    print(user_list)


def savenew_user(nikename, dic):
    # print('old userlist:')
    # print(user_list)
    dic.update({'robot_mode': True})
    # print('new user info dic :')
    # print(dic)
    global user_number
    user_number += 1
    updatelist(nikename, dic)
    print('new userlist:')
    print(user_list)


# 数一下一共多少个用户
def get_user_numer():
    return user_number


# 返回这个用户的字典，字典格式{'UserName':''，'NickName'：，'robot_mode': ,'focus_list':['','','']
def get_user(nikename):
    # print('this user:')
    # print(user_list[nikename])
    return user_list[nikename]


def update_userlist():
    # 增加导入功能
    try:
        f = open(FILE, "r")
        global user_list
        user_list = json.load(f)
        print('read in is successful')
        print(user_list)
        f.close()
    except:
        print("logs file error user")


def down_userlist():
    # 增加导出功能
    try:
        f = open(FILE, "w")
        json.dump(user_list, f)
        f.close()
    except:
        print("logs file error user")


def main():
    update_userlist()
