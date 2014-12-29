__author__ = 'keaj'

from __future__ import unicode_literals

import httplib2
import os, json,copy,re
import base64
from apiclient.discovery import build
from oauth2client.client import SignedJwtAssertionCredentials
from utils.Exceptions import  NoSuchBook



class GoogleBooksService(object):
    def loadCredentialsAndAuthorize(self):
        try:
            key = base64.b64decode(os.environ['GBOOKS_PK'])
            credinfo = json.loads(os.environ['BOOK_SERVICE'])

        except KeyError as e:
            with open('config/apiconfig.settings','r') as f:
                apisettings = f.readlines()
                for n in apisettings:
                    k,v=n.split('=',1)
                    os.environ[k]=v
            with open('config/google_api_key','r') as rsa:
                os.environ['GBOOKS_PK']=base64.b64encode(rsa.read())
            key = base64.b64decode(os.environ['GBOOKS_PK'])
            credinfo = json.loads(os.environ['BOOK_SERVICE'])

        scope = [
                'https://www.googleapis.com/auth/books',
                 ]
        self._credentials = SignedJwtAssertionCredentials(
            credinfo['web']['client_email'], key, scope, 'notasecret')
        http = httplib2.Http()
        self._httpClient = self._credentials.authorize(http)
        self._service = build('books', 'v1', http=self._httpClient)

    def __init__(self):
        super(GoogleBooksService, self).__init__()
        self._credentials = None
        self.loadCredentialsAndAuthorize()

    def recordToSerializable(self, record):
        try:
            record = record['items'][0]
        except KeyError:
            raise NoSuchBook
        qdict = {}
        #how to handle it if publisher and title are missing?
        qdict['publisher']=record['volumeInfo']['publisher']
        author = "&".join([authors for authors in record['volumeInfo']['authors']])
        qdict['author']=author
        title = record['volumeInfo']['title']
        subt = ""
        try:
            subt = record['volumeInfo']['subtitle']
        except KeyError:
            pass
            #swallow the exception
        title = ":".join([title,subt]) if subt else title
        qdict['title']=title
        date = record['volumeInfo']['publishedDate'].encode('utf-8')
        if re.match(r'[0-9]{4}-[0-9]{2}-[0-9]{2}',date):
            qdict['publish_date'] = date.split('-')[0]
        else:
            qdict['publish_date']=int(record['volumeInfo']['publishedDate'])
        for a in record['volumeInfo']['industryIdentifiers'] :
            if a['type']=='ISBN_13':
                qdict['isbn_13']=a['identifier']
            elif a['type']=='ISBN_10':
                qdict['isbn_10']=a['identifier']
        qdict['description']=record['volumeInfo'].get('description',"")
        qdict['genre'] = "&".join([a for a in record['volumeInfo']['categories']])
        return qdict

    def getByISBN(self, isbn):
        isbn = isbn.replace("-", '')
        if self._service:
            bookrecord = self._service.volumes().list(q="isbn:%s" % isbn).execute()
            return self.recordToSerializable(bookrecord)
