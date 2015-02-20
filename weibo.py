import urllib.request
import http.cookiejar
import base64
import json
import urllib.parse
import rsa
import binascii
import os
import re
import time
import datetime
import random


username=''
password=''


cookiejar=http.cookiejar.LWPCookieJar(username)
cookie=urllib.request.HTTPCookieProcessor(cookiejar)
httphandle=urllib.request.HTTPHandler()
opener=urllib.request.build_opener(cookie,httphandle)
urllib.request.install_opener(opener)

opener.addheaders = [('Referer', 'http://weibo.com/3217179555/C5cxAC7GN?type=comment')]

publickey='EB2A38568661887FA180BDDB5CABD5F21C7BFD59C090CB2D245A87AC253062882729293E5506350508E7F9AA3BB77F4333231490F915F6D63C55FE2F08A49B353F444AD3993CACC02DB\
784ABBB8E42A9B1BBFFFB38BE18D78E87A0E41B9B8F73A928EE0CCEE1F6739884B9777E4FE9E88A1BBE495927AC4A799B3181D6442443'
pubkey=int(publickey,16)

postdata={
    'entry':'weibo',
    'gateway':'1',
    'from':'',
    'savestate':'7',
    'useticket':'1',
    'pagerefer':'http://login.sina.com.cn/sso/logout.php?entry=miniblog&r=http%3A%2F%2Fweibo.com%2Flogout.php%3Fbackurl%3D%252F',
    'vsnf':'1',
    'su':'',
    'service':'miniblog',
    'servertime':'',
    'nonce':'',
    'pwencode':'rsa2',
    'rsakv':'1330428213',
    'sp':'',
    'sr':'1920*1080',
    'encoding':'UTF-8',
    'prelt':'269',
    'url':'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
    'returntype':'META',
    'showpin':'0'
    }
def gettime():
    return time.mktime(datetime.datetime.now().timetuple())
    
def openurl(url,chart='utf-8',data=None):
    result=opener.open(url,data)
    result=result.read()
    if(chart!='null'):
        return result.decode(chart)
    else:
        return result

"""

login_about get begin


"""
def b64(sth):
    return base64.b64encode(sth.encode()).decode('utf-8')

def get_su():
    string=urllib.parse.quote(username)
    return b64(string)

def get_sp(st,nc):
    key=rsa.PublicKey(pubkey,65537)
    message=str(st)+'\t'+str(nc)+'\n'+password
    sp=rsa.encrypt(message.encode(),key)
    sp=binascii.b2a_hex(sp)
    return sp.decode('utf-8')
def get_servertime():#and nonce

    url='http://login.sina.com.cn/sso/prelogin.php?entry=weibo&su=%s&checkpin=1&rsakt=mod' %(get_su())
    page=opener.open(url)
    data=json.loads(page.read().decode('utf-8'))
    
    result=[]
    result.append(str(data['servertime']))
    result.append(str(data['nonce']))
    result.append(str(data['pcid']))
    return result
"""

login_about get end

match begin

"""
def match(pattern,string):
    a=re.compile(pattern)
    result=re.findall(a,string)
    return result
def match_fanscount(string):
    a=r'fans" >([0-9]+)'
    result=match(a,string)
    if(result!=[]):
        return result[0]
    else:
        return 20000
def match_login_url(string):
    a=r'[a-zA-z]+://[^\s]*=0'
    result=match(a,string)
    return result[0]
def match_uid(string):
    a=r'usercard="id=([0-9]+)" href="'
    result=match(a,string)
    return result
def match_name(string):
    a=r"CONFIG\['onick'\]='(.+)'"
    result=match(a,string)
    return result[0]
def replace_(st):
    a='\\'
    
    return st.replace(a,'')
"""

match end

do login begin

"""
def login(postdata):
    result=get_servertime()
    servertime=result[0]
    nonce=result[1]

    postdata['su']=get_su()
    postdata['sp']=get_sp(servertime,nonce)
    postdata['servertime']=servertime
    postdata['nonce']=nonce
    
    postdata=urllib.parse.urlencode(postdata)
    url='http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)'
    
    headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.94 Safari/537.36 OPR/27.0.1689.66 (Edition Baidu)',
         }
    req=urllib.request.Request(url,postdata.encode(),headers)
    text=urllib.request.urlopen(req)
    text=text.read()
    
    text=text.decode('gbk')
    result=match_login_url(text)
    opener.open(result)
    cookiejar.save()
def auto_login():
    cookiejar.load()
    html=openurl('http://weibo.com/','gbk')
    url=match_login_url(html)
    opener.open(url)
    """
    opener.open('http://passport.weibo.cn/sso/crossdomain?action=login&savestate=1&retcode=0')
    result=openurl('http://weibo.com/2598335181/follow?rightmod=1&wvr=6')
    print(result)"""

"""


"""


if(os.path.exists(username)==True):
    print('检测到cookie,自动登录')
    auto_login()
else:
    login(postdata)


