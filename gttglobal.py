# -*- coding: cp936 -*-

import urllib,urllib2,cookielib
import re,xe #xe is the file of converter
import simplejson as json
import logging
import os
import export_excel

os.system("title gttglobal")
def log(info,warning):
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s>>>>>>\n %(message)s',
                        datefmt='%d/%m/%Y %H:%M:%S',
                        filename='gttglobal.log',
                        filemode='a')
    if warning is None:
        logging.info(info+"\n")
    else:
        logging.warning(warning+"\n")

#<---------start use xe.py module get currency converter
converter_CNY=xe.convert()
#----------end start get currency converter---------->
url="http://www.gttglobal.com/"

# The global cookie jar used for all requests
cj = cookielib.LWPCookieJar()
opener = urllib2.build_opener()
opener.add_handler(urllib2.HTTPCookieProcessor(cj))
opener.add_handler(urllib2.HTTPRedirectHandler())
urllib2.install_opener(opener)

#<<<----------begin log in
values={
    '__VIEWSTATE':"/wEPDwUJNzUwNTU4MTQ0D2QWAgIDD2QWBGYPDxYCHgdWaXNpYmxlZ2QWAgIDDw9kFgIeB29uY2xpY2sFFHJldHVybiBMb2dpbkNoZWNrKCk7ZAIBDw8WAh8AaGRkZIgq1mmiBE7/lp2PRN2bRp2rQOZSa/+8wCiNB2Ay0Z/6",
    '__EVENTVALIDATION':"/wEdAAco9qakZ7KhXPH/+eLDn2IwEeYAWJOna7Xnq7ux65LUo15PlMxnLsamw2ojvACFzIvjLIXuyIbiBAawz4RVdPEm3gMgf6178p6BltFYL6I0mRPPZAvojWDOku8yQK/H3V9oN7TLx+5jNlzoB2SojyGNtVMfWADlVOngGpJdKIiJcONuDokYC1ZXEZAtLE1TKQ8=",
    'action':"login",
    'location':"/index.php",
    'Header4Index1$txtUserId':"lzg",
    'Header4Index1$txtUserPwd':"lzg2011",
    'Header4Index1$txtUserPwdFirst':"Password",
    'Header4Index1$btnLogin':"Login",
    'hidUserType':"",
    'IsLogin':"false"
}
data=urllib.urlencode(values)
req=urllib2.Request(url,data)
response=urllib2.urlopen(req)
#end log in--------->>>

#<<<------begin define global 
#end define global -------->>>
def get_result(flight_type,origin,destination,depart_Date,return_Date,gds):
    search_info_url="http://www.gttglobal.com/MultiGds/Step1.aspx?type="+flight_type+"&cabin=ALL&origin1="+origin+"&destination1="+destination+"&date1="+depart_Date+"&origin2=&destination2=&date2="+return_Date+"&adt=1&chd=0&airline=&gds="+gds #w,S,A,T
    request_search_info=urllib2.urlopen(search_info_url)
    #print request_search_info.geturl()
    read_search_info=request_search_info.read()

    re_params=re.compile(r'params=(.+?)&')
    params=re.findall(re_params,read_search_info)[0]

    def get_data(params):
        global status,nextkey,result #use global 
        result_json_url="http://www.gttglobal.com/Multigds/SearchHandler.ashx?params="+params+"&nextkey="+nextkey
        result_json=urllib2.urlopen(result_json_url).read()
        json_result=json.loads(result_json)
        list_result=len(json_result['list'])
        for i in range(0,list_result):
            result=result+json_result['list'][i]['itins']
        status=json_result['status']
        nextkey=json_result['nextkey']
    global run
    status_count=0
    while run:
        if status=="ok":
            get_data(params)
            status_count+=1
            if status_count>20:
                run=False
        else:
            run=False

flight_type="RoundTrip" #type=RoundTrip/OneWay

file_handle_date=open('city.txt')

city_txt=file_handle_date.readlines()
depart_Date=city_txt[10].strip()
return_Date=city_txt[11].strip()

file_handle_date.close()





for i in range(0,10):
    file_handle=open('city.txt')
    result=[]
    run=True
    nextkey=""
    status="ok"
    file_city=file_handle.readlines()[i]
    origin=file_city[0:3]
    destination=file_city[4:7]
    print origin,destination
    get_result(flight_type,origin,destination,depart_Date,return_Date,"W,S,A,T")
    min_ticket=min(result,key=lambda x:float(x['tp']))
    segments=""
    if flight_type!="OneWay":
        segments="RoundTrip:%d" %(len(min_ticket['tps'][0]['segments'])+len(min_ticket['tps'][1]['segments']))
    else:
        segments="OneWay:%d"%(len(min_ticket['tps'][0]['segments']))
    want_result="%s-%s %s %.2f %s %s" %(origin,destination,(min_ticket['ma']),(float(min_ticket['tp'])*float(converter_CNY)),min_ticket['gds'],segments)
    log(want_result,None)
    gtt_price_details="%s %.2f"%((min_ticket['ma']),(float(min_ticket['tp'])*float(converter_CNY)))
    gtt_remark_gds=""
    if min_ticket['gds']=="S":
        gtt_remark_gds="Sabre"
    if min_ticket['gds']=="W":
        gtt_remark_gds="Worldspan"
    if min_ticket['gds']=="A":
        gtt_remark_gds="Amadeus"
    if min_ticket['gds']=="T":
        gtt_remark_gds=="Travelsky"
    gtt_remark_segments=u"。" #add u avoid ascii error
    if len(min_ticket['tps'][0]['segments'])+len(min_ticket['tps'][1]['segments'])>4:
        gtt_remark_segments=u"，多行程。"
    gtt_remark=u"为"+gtt_remark_gds+u"价格"+gtt_remark_segments
    #user module and export excel file 
    export_excel.writeExcel("CHINA-USA分析(06212014).xlsx","Sheet1","K"+str(5+i),gtt_price_details)
    export_excel.writeExcel("CHINA-USA分析(06212014).xlsx","Sheet1","L"+str(5+i),gtt_remark)


file_handle.close()


