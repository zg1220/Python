import urllib,urllib2,cookielib,re

def convert():
    accept="text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
    accept_encoding="gzip,deflate,sdch"
    accept_language="en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2"
    connection="keep-alive"
    host="www.xe.com"
    user_agent="Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36"

    headers={'Accept':accept,
             #'Accept-Encoding':accept_encoding,#if add encoding,the last read can't input right
             'Accept-Language':accept_language,
             'Connection':connection,
             'Host':host,
             'User-Agent':user_agent}

    values={'Amount':"1",
          'From':"USD",
          'To':"CNY"}

    url="http://www.xe.com/currencyconverter/convert/?" #Amount=1&From=USD&To=CNY
    data=urllib.urlencode(values)
    req=urllib2.Request(url,data,headers)
    res=urllib2.urlopen(req)
    rea=res.read()
    re_converter=re.compile(r'USD&nbsp;=&nbsp;(.+?)&nbsp;CNY')
    converter=re.findall(re_converter,rea)[0]
    return converter

