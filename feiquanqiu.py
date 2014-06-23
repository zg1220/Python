# -*- coding: cp936 -*-
from urllib2 import Request,urlopen,URLError,HTTPError
import simplejson as json
import logging,os,export_excel

os.system("title feiquanqiu")

#<-----start defina log file
def log(info,warning):
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s>>>>>>\n %(message)s',
                        datefmt='%d/%m/%Y %H:%M:%S',
                        filename='feiquanqiu.log',
                        filemode='a')
    if warning is None:
        logging.info(info+"\n")
    else:
        logging.warning(warning+"\n")
#-----------end defina log file---->

def process(departureAirport,destinationAirport,departureDate,returnDate):
    try: 
        url="http://www.feiquanqiu.com/ticketsearch?departureAirport="+departureAirport+"&destinationAirport="+destinationAirport+"&departureDate="+departureDate+"&returnFromAirport=&returnToAirport=&returnDate="+returnDate+"&type=roundtrip&adults=1&children=0&cabin=E" #date format 07/30/2014
        req=Request(url)
        url_open=urlopen(req)
        rea=url_open.read()
        result=json.loads(rea)
        routings=result['airTicketListResponse']['routings']
        min_price_details=routings=result['airTicketListResponse']['routings'][0]
        return(min_price_details['mainAirlineCode'],min_price_details['totalSalesPrice'])
    except HTTPError,e:
        if e.code==503:
            print 'ERROR CODE:',e.code
            process(departureAirport,destinationAirport,departureDate,returnDate)
    except URLError,e:
        print 'We failed to reach a server.'
        print 'Reason: ',e.reason
    
file_date=open('city.txt')
city_txt=file_date.readlines()
departureDate=city_txt[10].strip()
returnDate=city_txt[11].strip()
file_date.close()

for i in range(0,10):
    file_city_txt=open('city.txt')
    citys=file_city_txt.readlines()[i]
    departureAirport=citys[0:3]
    destinationAirport=citys[4:7]
    print departureAirport,destinationAirport
    airline,price=process(departureAirport,destinationAirport,departureDate,returnDate)
    get_info="%s-%s  %s %s" %(departureAirport,destinationAirport,airline,price)
    airline_price="%s %s" %(airline,price)
    log(get_info,None)
    export_excel.writeExcel("CHINA-USA分析(06212014).xlsx","Sheet1","I"+str(5+i),airline_price)
    
file_city_txt.close()
