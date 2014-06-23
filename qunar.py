import urllib2
import re

city={"go":"pvg","come":"nyc"}
def get_city(q):
    city_url="http://www.qunar.com/suggest/livesearch2.jsp?lang=zh&q="+q+"&sa=true&ver=1&callback=XQScript_"
    city_req=urllib2.urlopen(city_url)
    city_read=city_req.read()
    re_key=re.compile(r'"key":"(.+?)"')
    key=re.findall(re_key,city_read)[0]
    return key
city["go"]=get_city(city["go"])
city["come"]=get_city(city["come"])
print city

search_url="http://flight.qunar.com/site/interroundtrip_compare.htm?fromCity="+city["go"]+"&toCity="+city["come"]+"&fromDate=2014-09-06&toDate=2014-09-18&from=fi_ont_search&isInter=true"
# url="http://flight.qunar.com/"
search_req=urllib2.urlopen(search_url)
# print search_req.geturl()
print search_req.read()



http://flight.qunar.com/twelli/flight/thunder_interRoundTripFlightInfo.jsp?&departureCity=%E4%B8%8A%E6%B5%B7&arrivalCity=%E7%BA%BD%E7%BA%A6&departureDate=2014-09-06&returnDate=2014-09-18&prePay=true&locale=zh&op=2&nextNDays=0&searchLangs=zh&searchType=RoundTripFlight&reset=false&queryID=192.168.37.236%3A-5926927d%3A146a8c11772%3A5189&ismore=true&timeStamp=1402991211140&_token=29876

192.168.37.236:-5926927d:146a9088ac7:-1efd
192.168.37.236:-5926927d:146a9088ac7:-1efd