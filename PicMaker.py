import requests
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from urllib import request
import time

URL_HEAD = 'https://image.thum.io/get/png/width/600/crop/800/viewportWidth/600/'
cache = 'D:\python\WeTwitter\cache\weibo\\'
URL_WEIBO = 'https://m.weibo.cn/detail/'


def get_pic(mid):
    path = cache + mid + '.png'
    if os.path.exists(path):
        print('文件已经存在 ： '+mid)
        return path
    try:
        url = URL_HEAD + URL_WEIBO + mid
        r = requests.get(url)
        r.raise_for_status()  # 异常抛出
        # r.encoding = r.apparent_encoding  # 按表头重编码
        with open(path, 'wb') as f:
            f.write(r.content)
            f.close()
            print(path + ' 文件保存成功')
        return path
    except:
        print('error: save picture is wrong = ' + mid)


def get_tweet_pic(url):
    print('start to print pictweet')
    f = request.urlopen(url,timeout=30)
    result = f.read()
    name = url.split('/')[-1]
    txt = 'D:\python\WeTwitter\cache\\twitter\\%s.html' % name
    if os.path.exists(txt):
        print('文件已经存在 ： '+name)
        return 'D:\python\WeTwitter\cache\\twitter\\%s.png' % name
    htm = open(txt, "wb")
    htm.write(result)
    options = webdriver.ChromeOptions()
    options.add_argument('-headless')
    driver = webdriver.Chrome(chrome_options=options)  # chrome_options=options)
    driver.get(txt)
    driver.set_window_size(600, 1000)
    driver.implicitly_wait(10)
    # WebDriverWait(driver, 30).until()
    # time.sleep(5)
    pic_path = 'D:\python\WeTwitter\cache\\twitter\\%s.png' % name
    driver.save_screenshot(pic_path)
    # picture = Image.open(pic_path)
    # picture = picture.crop((0, 77, 566, 800))
    # picture.save(pic_path)
    print('successful to save tweet pic nad pic_path is '+pic_path)
    return pic_path

# get_tweet_pic('https://mobile.twitter.com/RobertDowneyJr/status/1025779145018470401')
#
# start = time.clock()
# get_pic('4281583655140806')
# end = time.clock()
# print(end-start)
