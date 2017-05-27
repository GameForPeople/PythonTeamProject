# -*- coding: cp949 -*-
from xml.dom.minidom import parse, parseString
from xml.etree import ElementTree

##### global
xmlFD = -1
TripPlaceDoc = None


#### xml ���� �Լ� ����
def LoadXMLFromFile():
    fileName = str(input("please input file name to load :"))
    global xmlFD, TripPlaceDoc
    try:
        xmlFD = open(fileName)
    except IOError:
        print("invalid file name or path")
    else:
        try:
            dom = parse(xmlFD)
        except Exception:
            print("loading fail!!!")
        else:
            print("XML Document loading complete")
            TripPlaceDoc = dom
            return dom
    return None


def TripPlacesFree():
    if checkDocument():
        TripPlaceDoc.unlink()


def PrintDOMtoXML():
    if checkDocument():
        print(TripPlaceDoc.toxml())


def PrintBookList(tags):
    global TripPlaceDoc
    if not checkDocument():
        return None

    booklist = TripPlaceDoc.childNodes
    book = booklist[0].childNodes
    for item in book:
        if item.nodeName == "book":
            subitems = item.childNodes
            for atom in subitems:
                if atom.nodeName in tags:
                    print("title=", atom.firstChild.nodeValue)


def AddBook(bookdata):
    global TripPlaceDoc
    if not checkDocument():
        return None

    # book ������Ʈ ����
    newBook = TripPlaceDoc.createElement('book')
    newBook.setAttribute('ISBN', bookdata['ISBN'])
    # Title ������Ʈ ����
    titleEle = TripPlaceDoc.createElement('title')
    # �ؽ�Ʈ ��� ����
    titleNode = TripPlaceDoc.createTextNode(bookdata['title'])
    # �ؽ�Ʈ ��带 Title ������Ʈ�� ����
    try:
        titleEle.appendChild(titleNode)
    except Exception:
        print("append child fail- please,check the parent element & node!!!")
        return None
    else:
        titleEle.appendChild(titleNode)

    # Title ������Ʈ�� Book ������Ʈ�� ����.
    try:
        newBook.appendChild(titleEle)
        booklist = TripPlaceDoc.firstChild
    except Exception:
        print("append child fail- please,check the parent element & node!!!")
        return None
    else:
        if booklist != None:
            booklist.appendChild(newBook)


def SearchBookTitle(keyword):
    global TripPlaceDoc
    retlist = []
    if not checkDocument():
        return None

    try:
        tree = ElementTree.fromstring(str(TripPlaceDoc.toxml()))
    except Exception:
        print("Element Tree parsing Error : maybe the xml document is not corrected.")
        return None

    # get Book Element
    bookElements = tree.getiterator("book")  # return list type
    for item in bookElements:
        strTitle = item.find("title")
        if (strTitle.text.find(keyword) >= 0):
            retlist.append((item.attrib["ISBN"], strTitle.text))

    return retlist


def MakeHtmlDoc(BookList):
    from xml.dom.minidom import getDOMImplementation
    # get Dom Implementation
    impl = getDOMImplementation()

    newdoc = impl.createDocument(None, "html", None)  # DOM ��ü ����
    top_element = newdoc.documentElement
    header = newdoc.createElement('header')
    top_element.appendChild(header)

    # Body ������Ʈ ����.
    body = newdoc.createElement('body')

    for bookitem in BookList:
        # create bold element
        b = newdoc.createElement('b')
        # create text node
        ibsnText = newdoc.createTextNode("ISBN:" + bookitem[0])
        b.appendChild(ibsnText)

        body.appendChild(b)

        # BR �±� (������Ʈ) ����.
        br = newdoc.createElement('br')

        body.appendChild(br)

        # create title Element
        p = newdoc.createElement('p')
        # create text node
        titleText = newdoc.createTextNode("Title:" + bookitem[1])
        p.appendChild(titleText)

        body.appendChild(p)
        body.appendChild(br)  # line end

    # append Body
    top_element.appendChild(body)

    return newdoc.toxml()


def printBookList(blist):
    for res in blist:
        print(res)


def checkDocument():
    global TripPlaceDoc
    if TripPlaceDoc == None:
        print("Error : Document is empty")
        return False
    return True