import json
"""
初期使用简单的列表直接构造即可，后期可考虑并行问题，
使用类进行在线的数据统计和数据库记录用户数据，目前还不用。
"""
FILE = 'userinfo.json'
user_number = 0
user_list = {'@e200cc6d0c446c7dd2efd98e5424e2df990a4379c123be4796920b2e8176b55e':
                 {'username':'@e200cc6d0c446c7dd2efd98e5424e2df990a4379c123be4796920b2e8176b55e',
                  'nikename':'WT','robot_mode':True,'access_token':'2.00EeAykBfSv8zCbc1f8224abfxU1fE'}}


def get_access_token(username):
    return user_list[username]['access_token']


def updatelist(username, thisuser):
    user_list.update({username: thisuser})
    down_userlist()
    return True


# 昵称查询用户
def get_user_username(nikename):
    for username in user_list:
        if user_list[username]['Nikename'] == nikename:
            return username
    else:
        return u'没有这个人呢~'


def chg_robotmode(thisuser, to):
    thisuser['robot_mode'] = to
    print('changemode')
    # print(thisuser)
    updatelist(thisuser['UserName'], thisuser)


# 查询用户昵称
def get_user_nikename(thisuser):
    return thisuser['NickName']


# 这人在不在用户列表里
def in_user_list(username):
    if username in user_list:
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
def add_focus(username, addlist):
    user = get_user(username)
    for addname in addlist:
        if addname in get_user_focuslist(user):
            continue
        user['focus_list'] += [addname]
    updatelist(username, user)
    return None


# 新用户添加
def savenew_user1(username, nickname, focus_list):
    print('old userlist:')
    print(user_list)
    new = {'UserName': username, 'NickName': nickname, 'robot_mode': True, 'focus_list': focus_list}
    global user_number
    user_number += 1
    updatelist(username, new)
    print('new userlist:')
    print(user_list)


def savenew_user(username,dic):
    print('old userlist:')
    print(user_list)
    dic.update({'robot_mode': True})
    print('new user info dic :')
    print(dic)
    global user_number
    user_number += 1
    updatelist(username,dic)
    print('new userlist:')
    print(user_list)


# 数一下一共多少个用户
def get_user_numer():
    return user_number


# 返回这个用户的字典，字典格式{'UserName':''，'NickName'：，'robot_mode': ,'focus_list':['','','']
def get_user(username):
    print('this user:')
    print(user_list[username])
    return user_list[username]

def update_userlist():
    # 增加导入功能
    try:
        f = open(FILE,"rb")
        global user_list
        print(f.read())
        user_list = json.load(f)
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

main()

# new_user(u'pj', u'凌晨', ['李楠'])
# print(user_list)
# user = get_user('pj')
# print(user)
# print(get_user_numer())
# print('robot')
# print(get_user_robotmode(user))
# print(get_user_nikename(user))
# print(get_user_focuslist(user))
# add_focus('pj', ['tw','fsf'])
# changerobotmode(user, False)
# print('user:')
# print(user)
# print('userlist:')
# print(user_list)
