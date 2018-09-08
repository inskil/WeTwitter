from bs4 import BeautifulSoup, NavigableString
from urllib import request
import PicMaker
import WeChat

# f = open('read.html',encoding='UTF-8')
# # f = request.urlopen(endpoint+request.quote(user))
# html = f.read().encode('utf-8')
# # print(html.decode("gbk"))
# soup = BeautifulSoup(f,'lxml')
# f.close()

def search(user):
    endpoint = "https://twitter.com/search?f=users&src=typd&q="
    print('search twitter start....')
    f = request.urlopen(endpoint + request.quote(user))
    # html = f.read().encode('utf-8')
    soup = BeautifulSoup(f, 'lxml')
    find = soup.find_all(attrs={"class": 'ProfileCard-avatarLink js-nav js-tooltip'},limit=8)
    re = []
    i= 0
    for tag in find:
        if i >= 5 :break
        i += 1
        dic = tag.attrs
        re.append([dic['href'][1:],dic['title']])
        # print(dic['href'][1:] +' this is ' + dic['title'])
    print(re)
    f.close()
    return re

def find_byid(id):
    print('start to spider to find tweets')
    print('id is '+id)
    URL = 'https://twitter.com/%s' % id
    print(URL)
    URL_MOBILE ='https://mobile.twitter.com'
    f = request.urlopen(URL)
    # html = f.read().encode('utf-8')
    soup = BeautifulSoup(f, 'lxml')
    find = soup.find_all(class_='tweet-timestamp js-permalink js-nav js-tooltip',limit=5)
    # print(find)
    re_url = []
    re_text= []
    for tag in find:
        dic = tag.attrs
        url = URL_MOBILE + dic['href']
        re_url.append(url)
        # print(dic['href'][1:] +' this is ' + dic['title'])
    # print(soup)
    find = soup.find_all(class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text',limit=5)
    # print(find)
    for tag in find:
        # print(type(tag))
        # print(tag)
        try:
            str = tag.string
            if str == None:
                str = ''
                try:
                    for intag in tag:
                        # intag =tag[0]
                        if not intag.string ==None:
                            str += intag.string
                    print(str)
                    re_text.append(str)
                except:
                    print('error to read a string in tag')
            else:re_text.append(str)
        except:print('error to read the string')
    print(re_text)
    print(re_url)
    f.close()
    soup.clear()
    re ={'pic':re_url,'text':re_text}
    return re

def get_tweets_pic(username,count,url_list):
    i= 0
    re = []
    try:
        for url in url_list:
            if i >= count:break
            else:
                print(url)
                re.append(PicMaker.get_tweet_pic(url))
                i += 1
    except:
        print('down pic tweet error')
    print('all pic had down sucessfully')
    WeChat.itchat.send('推送的图片已经制作好了哟~准备接受啦啦啦~', username)
    for path in re:
        WeChat.itchat.send_image(path,username)
    return True


# find_byid('RobertDowneyJr')
# search('希拉里')