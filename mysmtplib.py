# -*- coding: cp949 -*-
from Book_XML import *
from http.client import HTTPConnection
from http.server import BaseHTTPRequestHandler, HTTPServer

##global
conn = None
#arcode = None   #지역번호

regKey = '0c5747ff0e144b9ca77645c4ed19ef1b'

#regKey = '9dc253be6f5224567ede1f03b84a4e24'

# 네이버 OpenAPI 접속 정보 information
server = "api.childcare.go.kr"
#server = "apis.daum.net"

# smtp 정보
host = "smtp.gmail.com"  # Gmail SMTP 서버 주소.
port = "587"


def userURIBuilder(server, key, arcode):
    str = "http://" + server + "mediate/rest/cpmsapi021/cpmsapi021/request" + "?"
    #for key in user.keys():
    #    str += "key" + key + "=" + user[key] + "&"
    str += "key=" + key + "&"  + "arcode" + arcode
    return str

#http://api.childcare.go.kr/mediate/rest/cpmsapi021/cpmsapi021/request?key=50b8109640e3b5947a3788a03cfd151c&arcode=11380

def connectOpenAPIServer():
    global conn, server
    conn = HTTPConnection(server)


def getPreschoolDataFromArcode(arcode):
    global server, regKey, conn
    if conn == None:
        connectOpenAPIServer()
    # uri = userURIBuilder(server, key=regKey, query='%20', display="1", start="1", target="book_adv", d_isbn=isbn)

    uri = userURIBuilder(server, key=regKey, arcode=arcode )  # 다음 검색 URL
    conn.request("GET", uri)

    req = conn.getresponse()
    print(req.status)
    if int(req.status) == 50:
        print("유치원 정보를 모두 받아왔습니다")
        return extractPreschoolData(req.read())
    else:
        print("역시 유치원 정보는 받아오지 못했습니다.")
        return None


def extractPreschoolData(strXml):
    from xml.etree import ElementTree
    tree = ElementTree.fromstring(strXml)
    print(strXml)
    # PreschoolData(Book) 엘리먼트를 가져옵니다.
    itemElements = tree.getiterator("item")  # return list type
    print(itemElements)
    for item in itemElements:
        #isbn = item.find("isbn")
        strTitle = item.find("crname")
        strAddress = item.find("craddr")
        strNumber = item.find("crtel")

        print(strTitle)
        if len(strTitle.text) > 0:
            return {"주소": strAddress.text, "번호": strNumber.text}


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
    # MIMEMultipart의 MIME을 생성합니다.
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    # Message container를 생성합니다.
    msg = MIMEMultipart('alternative')

    # set message
    msg['Subject'] = title
    msg['From'] = senderAddr
    msg['To'] = recipientAddr

    msgPart = MIMEText(msgtext, 'plain')
    bookPart = MIMEText(html, 'html', _charset='UTF-8')

    # 메세지에 생성한 MIME 문서를 첨부합니다.
    msg.attach(msgPart)
    msg.attach(bookPart)

    print("connect smtp server ... ")
    s = mysmtplib.MySMTP(host, port)
    # s.set_debuglevel(1)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(senderAddr, passwd)  # 로긴을 합니다.
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
            html = MakeHtmlDoc(SearchBookTitle(value))  # keyword에 해당하는 책을 검색해서 HTML로 전환합니다.
            ##헤더 부분을 작성.
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html.encode('utf-8'))  # 본분( body ) 부분을 출력 합니다.
        else:
            self.send_error(400, ' bad requst : please check the your url')  # 잘 못된 요청라는 에러를 응답한다.


def startWebService():
    try:
        server = HTTPServer(('localhost', 8080), MyHandler)
        print("started http server....")
        server.serve_forever()

    except KeyboardInterrupt:
        print("shutdown web server")
        server.socket.close()  # server 종료합니다.


def checkConnection():
    global conn
    if conn == None:
        print("Error : connection is fail")
        return False
    return True
