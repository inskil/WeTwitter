# coding=utf-8
import requests
import os
import time

APP_KEY = '2740277281'
APP_SECRET = 'a39525d92fd1264e2ff66a0791591dde'
GET_TOKEN_INFO = 'https://api.weibo.com/oauth2/get_token_info'
CALLBACK_URL = 'https://api.weibo.com/oauth2/default.html'
Auth_URL = 'https://api.weibo.com/oauth2/authorize'
Auth_URL_APP = 'https://open.weibo.cn/oauth2/authorize'
Access_Token_URL = 'https://api.weibo.com/oauth2/access_token'
ACCESS_TOKEN_MY = '2.00EeAykBfSv8zCbc1f8224abfxU1fE'
# url = Auth_URL + '?' + 'client_id=' + APP_KEY + '&redirect_uri=' + CALLBACK_URL
EXPIR_IN_MY = 157660782
MY_CODE = '768f3836b244ae2ca804d70b71cfb2f5'

# h5的授权界面
GET_UESER_URL = 'https://open.weibo.com/oauth2/authorize?client_id=2740277281&redirect_uri=https://api.weibo.com/oauth2/default.html'


# params ={
#     'client_id':APP_KEY,
#     'redirect_uri':CALLBACK_URL
# }


def get_token_info(access_token):
    params = {'access_token': access_token}
    r = requests.post(GET_TOKEN_INFO, params)
    print(r.url)
    print(r.text)
    return r.text


def get_Access_Token(code):
    params = {
        'client_id': APP_KEY,
        'client_secret': APP_SECRET,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': CALLBACK_URL
    }
    r = requests.post(Access_Token_URL, params)
    print(r.url)
    print(r.text)
    userinfo = r.text
    print(userinfo)
    # add_newuser()
    return userinfo


class NewTimeLine:
    news = {}
    count = 1
    userid = 1
    access_token = ''
    mode = False
    mid = ''

    def __init__(self, access_token, count=1):
        # access_token	true	string	采用OAuth授权方式为必填参数，OAuth授权后获得。
        # since_id	false	int64	若指定此参数，则返回ID比since_id大的微博（即比since_id时间晚的微博），默认为0。
        # max_id	false	int64	若指定此参数，则返回ID小于或等于max_id的微博，默认为0。
        # count	false	int	单页返回的记录条数，最大不超过100，默认为20。
        # page	false	int	返回结果的页码，默认为1。
        # base_app	false	int	是否只获取当前应用的数据。0为否（所有数据），1为是（仅当前应用），默认为0。
        # feature	false	int	过滤类型ID，0：全部、1：原创、2：图片、3：视频、4：音乐，默认为0。
        # trim_user	false	int	返回值中user字段开关，0：返回完整user字段、1：user字段仅返回user_id，默认为0。
        GET_USER_TIMELINE = 'https://api.weibo.com/2/statuses/home_timeline.json'
        try:
            params = {'access_token': access_token,
                      'count': count,
                      }
            r = requests.get(GET_USER_TIMELINE, params)
            print(r.text)
            self.access_token = access_token
            self.count = count
            self.news = r.json()['statuses'][0]
        except:
            print('Error: 最新消息字典获取失败，请求速度过快，尝试歇一歇')

    print('logs:this is the news:')
    print(news)


@property
def print_mse(self):
    # 推送三要素，时间，地点，人物。地点就算了。人物，时间，以及图片内容。
    re = []
    pic = self.get_pic()
    name = self.get_name()
    tim = self.get_time()
    print(tim)
    st = '你关注的对象' + name + '在:' + tim + ' 更新了微博,以下为微博内容：'
    if self.is_retweet_mode():
        st = '你关注的对象' + self.get_name() + + '在' + self.get_time() + '转发了微博,以下为原微博内容：'
        re = re + [['text', st]]
        st = self.get_retweet_text()
        re = re + [['text', st]]
        if not len(pic) == 0:
            for pict in pic:
                re = re + [['pic', pict]]
        st = self.get_name() + '评论内容为：\n'
    else:
        if not len(pic) == 0:
            re = re + [['text', st]]
            for pict in pic:
                re = re + [['pic', pict]]
            st = '文字内容为：'
    st = st + self.get_text()
    re = re + [['text', st]]
    st = '原文链接为' + self.get_url
    re = re + [['text', st]]
    return re


# 检测是否为转发别人的内容
def is_retweet_mode(self):
    if 'retweeted_status' in self.news:
        self.mode = True
        return True
    return False


# 获取转发原文的文字内容
def get_retweet_text(self):
    state = self.news['retweeted_status']
    statext = state['text']
    stausername = state['user']['name']
    text = '原博主@' + stausername + '的内容为\n“' + statext + '”'
    print('logs: statext=' + text)
    return text


# 获取关注对象的微博博文的文字内容
def get_text(self):
    text = self.news['text']
    print('logs: mytext=' + text)
    return text


# 从api获取图片链接，下载到本地后返回本地地址方便推送到微信，返回为一个地址列表
def get_pic(self):
    cache = '\cachepic\\'
    print('logs: this is pic function')

    def download(List):
        pic_path = []
        for url in List:
            try:
                path = cache + url.split('/')[-1]
                r = requests.get(url, timeout=30)
                r.raise_for_status()  # 异常抛出
                r.encoding = r.apparent_encoding  # 按表头重编码
                if not os.path.exists(cache):
                    os.makedirs(cache)
                if not os.path.exists(path):
                    with open(path, 'wb') as f:
                        f.write(r.content)
                        f.close()
                        print(path + ' 文件保存成功')
                        pic_path.append(path)
                else:
                    print('文件已经存在')
            except:
                print('error: save picture is wrong' + url)
                continue
        return pic_path

    focus = self.news
    if self.is_retweet_mode():
        focus = self.news['retweeted_status']
    print(focus['pic_urls'])
    pic = focus['pic_urls']
    pic_url = []
    for url_dict in pic:
        url = url_dict['thumbnail_pic']
        url = url.replace('thumbnail', 'large')
        pic_url.append(url)
    pic_path = download(pic_url)
    return pic_path


# 获得微博发送的消息，返回的为一个时间文字段，哪一年哪一月哪一日这样
def get_time(self):
    tim = self.news['created_at']
    tim = tim.replace(' +0800 ', ' ')
    tim = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(tim))
    print("logs: time is " + tim)
    return tim


# 拼接一下原微博地址这样
@property
def get_url(self):
    # http://api.weibo.com/2/statuses/go 根据ID跳转到单条微博页
    GOTO_URL = 'http://api.weibo.com/2/statuses/go?'
    url = GOTO_URL + ('uid=%s/id%s' % (self.get_uid(), self.get_mid()))
    return url


# 获取uid以供使用这样
def get_uid(self):
    self.userid = self.news['user']['id']
    return self.userid


# 获取mid以供使用这样
def get_mid(self):
    self.mid = self.news['mid']
    return self.mid


# 获取用户名字（关注对象）  备注名字
def get_screenname(self):
    return self.news['user']['screen_name']


# 获取用户名字（关注对象）
def get_name(self):
    try:
        nam = self.news['user']['name']
        print('logs: this is getname and name is:')
        print(nam)
    except:
        nam = 'error'
        print('error to get name')
    return nam





re = NewTimeLine(ACCESS_TOKEN_MY)
print(re.print_mse)
