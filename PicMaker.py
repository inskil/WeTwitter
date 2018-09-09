import requests
import os
from selenium import webdriver
from urllib import request
import time

URL_HEAD = 'https://image.thum.io/get/auth/2068-347275389/prefetch/png/width/600/crop/800/'
root = os.getcwd()
cache = os.path.join(root,'cache','weibo')
URL_WEIBO = 'https://m.weibo.cn/detail/'
FIANL_URL = 'https://image.thum.io/get/auth/2068-347275389/png/width/600/crop/800/'



def get_pic(mid):
    path = os.path.join(cache,mid+'.png')
    print(path)
    if os.path.exists(path):
        print('文件已经存在 ： ' + mid)
        return path
    url = URL_WEIBO + mid
    print(url)
    name = url.split('/')[-1]
    options = webdriver.ChromeOptions()
    options.add_argument('-headless')
    driver = webdriver.Chrome(chrome_options=options)  # chrome_options=options)
    driver.get(url)
    driver.set_window_size(600, 1000)
    driver.implicitly_wait(10)
    # WebDriverWait(driver, 30).until()
    # time.sleep(5)
    driver.save_screenshot(path)
    # picture = Image.open(pic_path)
    # picture = picture.crop((0, 77, 566, 800))
    # picture.save(pic_path)
    print('successful to save tweet pic nad pic_path is ' + path)
    return path



def get2_pic(mid):
    path = cache + mid + '.png'
    if os.path.exists(path):
        print('文件已经存在 ： '+mid)
        return path
    try:
        urlre = URL_HEAD + URL_WEIBO + mid
        url = FIANL_URL + URL_WEIBO + mid
        print(urlre,url)
        r = requests.post(urlre)
        print(r)
        time.sleep(1)
        print(r.text)
        if r.text == 'Image is cached':
            re = requests.get(url)
            re.raise_for_status()  # 异常抛出
        # r.encoding = r.apparent_encoding  # 按表头重编码
        with open(path, 'wb') as f:
            f.write(re.content)
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
    txt = os.path.join(root, 'cache', 'twitter', '%s.html' % name)
    pic_path = os.path.join(root, 'cache', 'twitter', '%s.png' % name)
    if os.path.exists(txt):
        print('文件已经存在 ： '+name)
        return pic_path
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
    driver.save_screenshot(pic_path)
    # picture = Image.open(pic_path)
    # picture = picture.crop((0, 77, 566, 800))
    # picture.save(pic_path)
    print('successful to save tweet pic nad pic_path is '+pic_path)
    return pic_path

if not os.path.exists('cache'):
    os.makedirs(r'cache/weibo')
    os.makedirs(r'cache/twitter')
get_tweet_pic('https://mobile.twitter.com/RobertDowneyJr/status/1025779145018470401')
# get_pic('4282475565809158')
