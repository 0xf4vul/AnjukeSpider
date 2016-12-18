# -*- coding: utf-8 -*-
import requests,json,urllib2,time,re


CorpID = "wxafbabc0f0c"
Secret = "caecXr7ixTo5q60lMGmw0dR-2iPcnGXBY"
Totag = "1"
AgentID = "1"
SizeRange = "80"
PriceRange = "110"
UnitPriceRange = "12000"
AnjukeUrl='http://hangzhou.anjuke.com/sale/jianggan/'


def SendMessage(Token,Data):
    url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s" % Token
    Header = "二手房提醒！！"
    values = {"totag": Totag, "msgtype": "text", "agentid": AgentID, "text": {"content": Data},
              "safe": "0"}
    jdata = json.dumps(values, ensure_ascii=False)
    req = urllib2.Request(url, jdata)
    response = urllib2.urlopen(req)
    return response.read()


def GetToken(Data):

    GetAccessToken = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=%s&corpsecret=%s" % (CorpID, Secret)
    req = urllib2.Request(GetAccessToken)
    response_data = urllib2.urlopen(req)
    res = eval(response_data.read())
    Token = res["access_token"]

    Response = SendMessage(Token,Data)
    print Response

def GetProxy():
    ProxyHomeUrl = "http://api.xicidaili.com/free2016.txt"
    Proxy = requests.get(ProxyHomeUrl)
    ProxyUrlList = list(Proxy.content.replace('\r','').split('\n'))
    return ProxyUrlList


def GetHouseInfo(InfoUrlList,data, headers):
    for InfoUrl in InfoUrlList:
        InfoReq = requests.get(InfoUrl,data=data,headers=headers)
        InfoData = InfoReq.content
        Title = re.findall('<title>(.*?)<\/title>', InfoData)[0]
        CommitTime = re.findall('<span>(.*?)<\/span>', InfoData)[0]
        DT = re.findall('<dt>(.*?)<\/dt>', InfoData)
        DD = re.findall('<dd>(.*?)<\/dd>', InfoData)
        HouseType = re.findall('\"housetype\"\:\"(.*?)\"', InfoData)[0]
        Price  = re.findall('<em>(.*?)<\/em>', InfoData)[0]

        UnitPrice = int(DD[6][:-8])
        Size = DD[2][:-9]
        #print Title
        print "面价：" + Size
        print "总价：" + Price
        print "单价：" + str(UnitPrice)
        if (Size > SizeRange ) and (Price <= PriceRange) and (UnitPrice <= UnitPrice):
            Data =  str(Title) + '\n' + "===========" + '\n' + str(HouseType) + '\n' + "===========" + '\n' + str(CommitTime) + '\n' + "===========" + '\n' + DT[6] + DD[0] + '\n' + DT[7] + DD[1] + '\n' + DT[9] + DD[2] + '\n' + DT[10] + DD[3] + '\n' + DT[11] + DD[4] + '\n' + DT[12] + DD[5] + '\n' + DT[13] + DD[6] + '\n' + "===========" + '\n' + InfoUrl
            print Data
            print "sending....."
            GetToken(Data)
        print "=================================="
        time.sleep(2)

def GetInfoUrl(AnjukeUrl):
    for Num in (1,2,3,4,5,6,7,8,9,10):
        AnjukeUrl=AnjukeUrl + "o5-p%s" % Num
        print AnjukeUrl
        headers = {
                    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
        }
        data = None
        HomeReq = requests.post(AnjukeUrl,data=data,headers=headers)
        HomeData = HomeReq.content
        InfoUrlList = re.findall('http:\/\/[a-z]{1,}\.anjuke\.com\/prop\/view\/.*\d+', HomeData)
        print InfoUrlList
        GetHouseInfo(InfoUrlList, data, headers)


GetInfoUrl(AnjukeUrl)





