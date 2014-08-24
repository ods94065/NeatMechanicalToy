import logging
import os
import sys,json
import httplib,urllib2,requests

def utf8RawInput(prompt):
    encoding = sys.stdin.encoding
    return raw_input(prompt.encode(encoding)).decode(encoding).encode('utf-8')
def UrlRequest(url,method='GET',data=None):
    dat = None
    req = urllib2.Request(url)
    resp = None
    if data:
        dat=json.dumps(data)
    if method=='GET':
        resp = requests.get(url)
    elif method=='POST':
        resp = requests.post(url,dat)
    return resp.text


def getUserInput():
    isbn = utf8RawInput('ISBN-13?')
    title = utf8RawInput('Title?')
    author = utf8RawInput('Author?')
    publisher = utf8RawInput('Publisher?')
    date_published = utf8RawInput('Date (YYYY)?')
    desc = utf8RawInput('Brief Description:')
    return {'isbn_13':isbn,'isbn_10':None, 'author':author,'title':title,'publisher':publisher,'publish_date':date_published,'description':desc}

if __name__=="__main__":
    book=getUserInput()
    ret = UrlRequest('http://127.0.0.1:8000/library/','POST',book)
    print ret