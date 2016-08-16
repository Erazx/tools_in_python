#!/usr/bin/python2.7
# -*- coding: utf-8 -*- 
# 调用百度翻译api，需要在百度开发平台创建一个app
import httplib
import urllib
import random
import sys, optparse
import json

if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')

# the md5 module is deprecated; use hashlib instead
try:
    import hashlib
    hash = hashlib.md5()
except ImportError:
    import md5
    hash = md5.new()

apidomain = 'api.fanyi.baidu.com'
apiurl = '/api/trans/vip/translate'
appid = 'your-baidu-app-apiid'
secretKey = 'baidu-app-secreKey'

p = optparse.OptionParser("%prog -q Query", version='1.0', prog = "baidu_trans.py", epilog = 'http://v.untx.cn')
p.add_option('-q', '--query', dest='Query', help='String to translate')
p.add_option('-f', '--from', dest='From', help='From Language, default "auto"')
p.add_option('-t', '--to', dest='To', help='To Language, default "zh"')

if __name__ == "__main__":
    if len(sys.argv)==1:
        p.print_help()
        sys.exit(1)

    opt, args = p.parse_args()

    if not opt.Query:
        p.print_help()
        sys.exit(1)

    q = opt.Query
    fromLang = opt.From and opt.From or 'auto'
    toLang = opt.To and opt.To or 'zh'
    salt = random.randint(32768, 65536)

    sign = appid+q+str(salt)+secretKey
    hash.update(sign)
    sign = hash.hexdigest()
    myurl = apiurl+'?appid='+appid+'&q='+urllib.quote(q)+'&from='+fromLang+'&to='+toLang+'&salt='+str(salt)+'&sign='+sign

    httpClient = None
 
    try:
        httpClient = httplib.HTTPConnection(apidomain)
        httpClient.request('GET', myurl)
 
        #response是HTTPResponse对象
        response = httpClient.getresponse()
        dict_result = json.loads(response.read())['trans_result'][0]
        #print( dict_result['src'], dict_result['dst'])
        print( "{0}: {1}".format(dict_result['src'], dict_result['dst']))
    except Exception as e:
        print( e)
    finally:
        if httpClient:
            httpClient.close()

