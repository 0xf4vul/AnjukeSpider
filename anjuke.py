# -*- coding: utf-8 -*-
import urllib2
import re,time,json
import redis


def SendMessage(Token,Data):
    url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s" % Token
    Header = "二手房提醒！！"
    values = {"totag": "1", "msgtype": "text", "agentid": "1", "text": {"content": Data},
              "safe": "0"}
    jdata = json.dumps(values, ensure_ascii=False)
    req = urllib2.Request(url, jdata)
    response = urllib2.urlopen(req)
    return response.read()


def GetToken(Data):
    CorpID = "wxaf10bc0f0c"
    Secret = "caecXr7ixToQgGSYW5OjLEZhDZ6J8h5q60lMGmw0dR-2iPcnGXBY"
    get_AccessToken = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=%s&corpsecret=%s" % (CorpID, Secret)

    req = urllib2.Request(get_AccessToken)
    response_data = urllib2.urlopen(req)
    res = eval(response_data.read())
    Token = res["access_token"]

    Response = SendMessage(Token,Data)
    print Response

def GetInfoUrl():
    for Num in (1,2,3,4,5,6,7):
        url='http://qd.anjuke.com/sale/licangqu/b199-o5-p%s/' % Num
        headers = {
                    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
        }
        data = None
        HomeReq = urllib2.Request(url, data, headers)
        HomeResponse = urllib2.urlopen(HomeReq)

        HomeData = HomeResponse.read()
        InfoUrl = re.findall('href="(.*?)"', HomeData)

        InfoUrlList = re.findall('http:\/\/qd\.anjuke\.com\/prop\/view\/.*\d+', HomeData)
        #print InfoUrl

        r = redis.Redis(host="127.0.0.1",port="6379",db=1)
        try:
            lid = json.loads(r.get('HourseUrl'))
        except Exception as e:
            print e
            lid = None
        if lid is None:
            lid = list()
        counter = 0
        if InfoUrlList not in lid:
            counter += 1
            lid.append(InfoUrlList)
            print "Add %s to Redis OK" % InfoUrlList
        r['HourseUrl'] = json.dumps(lid)
        if counter >0 :
            b = GetHouseInfo(InfoUrlList,data, headers)
        else:
            print 'Nothing is NEWS'

def GetHouseInfo(InfoUrlList,data, headers):
    for InfoUrl in InfoUrlList:
        #print InfoUrl
        InfoReq = urllib2.Request(InfoUrl, data, headers)
        InfoResponse = urllib2.urlopen(InfoReq)
        InfoData = InfoResponse.read()
        Title = re.findall('<title>(.*?)<\/title>', InfoData)[0]
        #print InfoData
        CommitTime = re.findall('<span>(.*?)<\/span>', InfoData)[0]
        DT = re.findall('<dt>(.*?)<\/dt>', InfoData)
        DD = re.findall('<dd>(.*?)<\/dd>', InfoData)
        HouseType = re.findall('\"housetype\"\:\"(.*?)\"', InfoData)[0]
        #print HouseType
        #print CommitTime
        Price  = int(re.findall('<em>(.*?)<\/em>', InfoData)[0])
        UnitPrice = int(DD[6][:-8])
        Size = DD[2][:-9]
        print Size
        print Price
        print UnitPrice
        Data =  str(Title) + '\n' + "===========" + '\n' + str(HouseType) + '\n' + "===========" + '\n' + str(CommitTime) + '\n' + "===========" + '\n' + DT[6] + DD[0] + '\n' + DT[7] + DD[1] + '\n' + DT[9] + DD[2] + '\n' + DT[10] + DD[3] + '\n' + DT[11] + DD[4] + '\n' + DT[12] + DD[5] + '\n' + DT[13] + DD[6] + '\n' + "===========" + '\n' + InfoUrl
        print Data
        if (Size > 80 ) and (Price <= 115) and (UnitPrice <= 12000):
            print "sending....."
            GetToken(Data)
        #print DT[15] + "|" + DT[16] + "|" + DT[17] + "|" + DT[18] + "|" + DT[19] + "|" + DT[20] + "|" + DT[21] + "|" + DT[22] + "|" + DT[23] + "|" + DT[24] + "|" + DT[25] + "|" + DT[26] + "|" + DT[27]
        #print DD[0] + "|" + DD[1] + "|" + DD[2] + "|" + DD[3] + "|" + DD[4] + "|" + DD[5] + "|" + DD[6] + "|" + DD[7] + "|" + DD[8] + "|" + DD[9] + "|" + DD[10] + "|" + DD[11] + "|" + DD[12] + "|" + DD[13] + "|" + DD[14] + "|" + DD[15] + "|" + DD[16]
        #print DT[6] + DD[0] + '\n' + DT[7] + DD[1] + '\n' + DT[9] + DD[2] + '\n' + DT[10] + DD[3] + '\n' + DT[11] + DD[4] + '\n' + DT[12] + DD[5] + '\n' + DT[13] + DD[6]
        print "=================================="
        time.sleep(5)

GetInfoUrl()
