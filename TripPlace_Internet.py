# -*- coding: cp949 -*-
from TripPlace_XML import *
from http.client import HTTPConnection
from http.server import BaseHTTPRequestHandler, HTTPServer

##global
conn = None
#arcode = None   #走蝕腰硲

regKey = 'nHhF%2FXpBrln%2Fp4eurQr9Hn0sY0dZMB9Te%2ByR5uzHoZKpC%2BoE3ZwREHfHX3QJ%2FGsCXTm6%2FLgAZjZKqAEHLCy4pw%3D%3D'

#regKey = '9dc253be6f5224567ede1f03b84a4e24'

# 革戚獄 OpenAPI 羨紗 舛左 information
server = "api.visitkorea.or.kr"
#server = "apis.daum.net"

# smtp 舛左
host = "smtp.gmail.com"  # Gmail SMTP 辞獄 爽社.
port = "587"


def userURIBuilderArea(server, key, areaCode, page):
    str = "http://" + server + "/openapi/service/rest/KorService/areaBasedList" + "?"

    if page == 1:
        str += "ServiceKey=" + key + "&" + "areaCode=" + areaCode + "&numOfRows=20&pageNo=1&MobileOS=ETC&MobileApp=AppTesting"
    elif page == 2:
        str += "ServiceKey=" + key + "&" + "areaCode=" + areaCode + "&numOfRows=20&pageNo=2&MobileOS=ETC&MobileApp=AppTesting"
    elif page == 3:
        str += "ServiceKey=" + key + "&" + "areaCode=" + areaCode + "&numOfRows=20&pageNo=3&MobileOS=ETC&MobileApp=AppTesting"
    return str

def userURIBuilderCate(server, key, page):
    str = "http://" + server + "/openapi/service/rest/KorService/areaBasedList" + "?"

    if page == 1:
        str += "ServiceKey=" + key + "&" + "cat1=C01&cat2=C0112" + "&numOfRows=20&pageNo=1&MobileOS=ETC&MobileApp=AppTesting"
    elif page == 2:
        str += "ServiceKey=" + key + "&" + "cat1=C01&cat2=C0112" + "&numOfRows=20&pageNo=2&MobileOS=ETC&MobileApp=AppTesting"
    elif page == 3:
        str += "ServiceKey=" + key + "&" + "cat1=C01&cat2=C0112" + "&numOfRows=20&pageNo=3&MobileOS=ETC&MobileApp=AppTesting"
    return str

def connectOpenAPIServer():
    global conn, server
    conn = HTTPConnection(server)


def getTripPlaceDataArea(areaCode, page):
    global server, regKey, conn
    if conn == None:
        connectOpenAPIServer()
    # uri = userURIBuilder(server, key=regKey, query='%20', display="1", start="1", target="book_adv", d_isbn=isbn)

    uri = userURIBuilderArea(server, regKey, areaCode, page)  # 陥製 伊事 URL
    conn.request("GET", uri)
    print(uri)

    req = conn.getresponse()

    if int(req.status) == 200:
        print("且員 舛左研 乞砧 閤焼尽柔艦陥")
        return extractTripPlaceData(req.read())
    else:
        print("蝕獣 且員 舛左澗 閤焼神走 公梅柔艦陥.")
        return None

def getTripPlaceDataCate(page):
    global server, regKey, conn
    if conn == None:
        connectOpenAPIServer()
    # uri = userURIBuilder(server, key=regKey, query='%20', display="1", start="1", target="book_adv", d_isbn=isbn)
    uri = userURIBuilderCate(server, regKey, page)  # 陥製 伊事 URL
    conn.request("GET", uri)
    print(uri)
    req = conn.getresponse()
    if int(req.status) == 200:
        print("且員 舛左研 乞砧 閤焼尽柔艦陥")
        return extractTripPlaceData(req.read())
    else:
        print("蝕獣 且員 舛左澗 閤焼神走 公梅柔艦陥.")
        return None


#塊増嬢 鎧澗 員
def extractTripPlaceData(strXml):
    from xml.etree import ElementTree
    tree = ElementTree.fromstring(strXml)
    #print(strXml)
    # TripPlaceData(Book) 燭軒胡闘研 亜閃辛艦陥.
    tripPlaceIndex = 1
    strOut = ""
    ####################失因廃坪?せせせせせせせせせ 腎疏壱推!!!!
    for item in tree.iter("item"):
        tripPlaceTitle = item.find("title")
        tripPlaceAddress = item.find("addr1")
        tripPlaceTel = item.find("tel")
        print(tripPlaceIndex)
        print(tripPlaceTitle.text)

        strOut += """
        """
        strOut += "%d" % tripPlaceIndex + """
        """
        strOut += "  [ " + tripPlaceTitle.text + " ]" + """
        """
        if tripPlaceAddress != None:
            print(tripPlaceAddress.text)
            strOut += "  爽社 : " + tripPlaceAddress.text + """
            """
        if tripPlaceTel != None:
            print(tripPlaceTel.text)
            strOut += "腰硲 : " + tripPlaceTel.text + """
            """

        print()
        strOut += """
        """

        tripPlaceIndex += 1
        #print("  " + tripPlaceTitle.text + "  腰硲 : " + tripPlaceTel + "   爽社 : " + tripPlaceAddress)
    return strOut
    #####################
    #itemElements = tree.getiterator("item")  # return list type
    #print(itemElements)
    #for item in itemElements:
    #    #isbn = item.find("isbn")
    #    strTitle = item.find("title")
    #    strAddress = item.find("add1")
    #    strNumber = item.find("tel")
    #    print(item.get("title"))
    #    print(strTitle)
    #    #if len(strTitle.text) > 0:
    #    return {"爽社": strAddress, "腰硲": strNumber}
    ########################


def sendMain():
    global host, port
    html = ""
    title = str(input('Title :'))
    senderAddr = str(input('sender email address :'))
    recipientAddr = str(input('recipient email address :'))
    msgtext = str(input('write message :'))
    passwd = str(input(' input your password of gmail account :'))
    msgtext = str(input('Do you want to include book data (y/n):'))
    if msgtext == 'y':
        keyword = str(input('input keyword to search:'))
        html = MakeHtmlDoc(SearchBookTitle(keyword))

    import mysmtplib
    # MIMEMultipart税 MIME聖 持失杯艦陥.
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    # Message container研 持失杯艦陥.
    msg = MIMEMultipart('alternative')

    # set message
    msg['Subject'] = title
    msg['From'] = senderAddr
    msg['To'] = recipientAddr

    msgPart = MIMEText(msgtext, 'plain')
    bookPart = MIMEText(html, 'html', _charset='UTF-8')

    # 五室走拭 持失廃 MIME 庚辞研 歎採杯艦陥.
    msg.attach(msgPart)
    msg.attach(bookPart)

    print("connect smtp server ... ")
    s = mysmtplib.MySMTP(host, port)
    # s.set_debuglevel(1)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(senderAddr, passwd)  # 稽延聖 杯艦陥.
    s.sendmail(senderAddr, [recipientAddr], msg.as_string())
    s.close()

    print("Mail sending complete!!!")


class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        from urllib.parse import urlparse
        import sys

        parts = urlparse(self.path)
        keyword, value = parts.query.split('=', 1)

        if keyword == "title":
            html = MakeHtmlDoc(SearchBookTitle(value))  # keyword拭 背雁馬澗 奪聖 伊事背辞 HTML稽 穿発杯艦陥.
            ##伯希 採歳聖 拙失.
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html.encode('utf-8'))  # 沙歳( body ) 採歳聖 窒径 杯艦陥.
        else:
            self.send_error(400, ' bad requst : please check the your url')  # 設 公吉 推短虞澗 拭君研 誓岩廃陥.


def startWebService():
    try:
        server = HTTPServer(('localhost', 8080), MyHandler)
        print("started http server....")
        server.serve_forever()

    except KeyboardInterrupt:
        print("shutdown web server")
        server.socket.close()  # server 曽戟杯艦陥.


def checkConnection():
    global conn
    if conn == None:
        print("Error : 尻衣 叔鳶")
        return False
    return True
