# -*- coding: cp936 -*-

import urllib,urllib2,cookielib
import time,re
import simplejson as json

def get_min(line_index,txt_file_name,FlightWay,Department_Date,Return_Date):
    #<--------------add cookie for website
    cj=cookielib.LWPCookieJar()
    opener=urllib2.build_opener()
    opener.add_handler(urllib2.HTTPCookieProcessor(cj))
    opener.add_handler(urllib2.HTTPRedirectHandler())
    urllib2.install_opener(opener)
    #-------------->
    #'city_cn.txt'
    file_handle=open(txt_file_name)
    file_city=file_handle.readlines()[line_index]
    department_city=file_city[0:3]
    return_city=file_city[4:7]
    file_handle.close()

    #<-------Start get city information
    def city_name(city,a):
        get_city_url=urllib2.urlopen("http://flights.ctrip.com/international/tools/GetCities.ashx?s="+city+"&a="+str(a)+"&t=0")
        citys=get_city_url.read()
        citys_index=citys.find('@')+1
        citys_str=citys[citys_index:]
        citys_str_index=citys_str.find('，')
        city_name=citys_str[0:citys_str_index].replace(' ','')
        return city_name

    go_city_name=city_name(department_city,0)
    come_city_name=city_name(return_city,1)

    city=go_city_name+'-'+come_city_name+'-'+department_city+'-'+return_city
    #print city
    #---------------get city information End>

    #<--------------form data
    #FlightWay=trip_type   #S mean oneway,D mean roundtrip
    # HomeCityID="1"
    # DestCityID="633"
    #Department_Date="2014-07-25"
    #Return_Date="2014-08-05"
    round_type=""
    if FlightWay=="D":
        round_type="round-"
    #----------------------->
    values_post={
        'FlightWay':FlightWay,
        #'homecity_name':"上海(SHA)",
        #'HomeCityID':HomeCityID,
        #'destcity1_name':"纽约(NYC)",
        #'destcityID':DestCityID,
        'DDatePeriod1':Department_Date,
        'ADatePeriod1':Return_Date
    }

    url_post="http://flights.ctrip.com/international/"+round_type+city
    data_post=urllib.urlencode(values_post)
    req_post=urllib2.Request(url_post,data_post)
    load=urllib2.urlopen(req_post)
    print load.geturl()

    html=load.read()

    # f=open('ctrip.html','w')
    # f.write(html)
    # f.close()

    queryLogTransNo=html[(html.find("name=\"queryLogTransNo\" value=\"")+30):(html.find("name=\"queryLogTransNo\" value=\"")+29+20)]

    RdNo=html[(html.find("RdNo:")+6):(html.find("RdNo:")+6+10)]

    re_ind_list=re.compile(r'id="ind" value="(.+?)" />')
    ind=re.findall(re_ind_list,html)[0]

    re_search_list=re.compile(r'name="searchList" value="(.+?)"/>')
    search_list=re.findall(re_search_list,html)[0]

    count_search_list=search_list.count('~')
    city_pair_airline="first"
    if(count_search_list>0):
        city_pair_airline1=search_list[search_list.find('~')+1:][0:search_list[search_list.find('~')+1:].find('~')]
        city_pair_airline2=search_list[search_list.find('~')+1:][search_list[search_list.find('~')+1:].find('~')+1:]
        print city_pair_airline1,city_pair_airline2
        city_pair_airline=['first',city_pair_airline1,city_pair_airline2]
    # print queryLogTransNo,RdNo,ind

    quert_type="1"
    with_direct_airline="T"

    if count_search_list>0:
        with_direct_airline="F"


    def get_result(queryLogTransNo,quert_type,city_pair_airline_index,with_direct_airline,RdNo,ind):
            search=urllib2.urlopen("http://flights.ctrip.com/international/GetSubstepSearchResults.aspx?IsJSON=T&queryLogTransNo="+queryLogTransNo+"&QueryType="+quert_type+"&cityPairAirline="+city_pair_airline+"&withDirectAirline="+with_direct_airline+"&RdNo="+RdNo+"&sPassType=NOR&ind="+ind)
            url=search.geturl()
            print url
            result=search.read()
            # print result
            return result
    result=""



    def json_handle(result):
        #<------------------write json file----------
        file_result=open('result.json','w')
        file_result.write(result)
        file_result.close()
        #-------------------------------------------->

        #<-----------------read json file and get min price details---
        file_json=file("result.json")
        file_read=file_json.read()
        file_read_json=json.loads(file_read.decode('gb2312'))
        min_price_details=min(file_read_json['FlightList'],key=lambda x:x['TotalPrice'])
        print min_price_details['OwnerAirline'],min_price_details['TotalPrice']

        file_json.close()

    for i in range(0,count_search_list+1):
        if count_search_list==0:
            result=get_result(queryLogTransNo,str(i+1),city_pair_airline[i],with_direct_airline,RdNo,ind)
        else:
            result=get_result(queryLogTransNo,str(i+1),city_pair_airline[i],with_direct_airline,RdNo,ind)
        json_handle(result)

line_index=0
txt_file_name='city.txt'
FlightWay='S'
Department_Date='2014-09-26'
Return_Date='2014-10-04'

#get_min(line_index,txt_file_name,FlightWay,Department_Date,Return_Date)
def for_get_min(way):
    FlightWay=way
    for i in range(0,10):
        if i<3:
            get_min(i,txt_file_name,FlightWay,Department_Date,Return_Date)
        elif i==3:
            if FlightWay=="S":
                FlightWay="D"
            else:
                FlightWay="S"
            get_min(i,txt_file_name,FlightWay,Department_Date,Return_Date)
        else:
            get_min(i,txt_file_name,FlightWay,Department_Date,Return_Date)

for_get_min(FlightWay)