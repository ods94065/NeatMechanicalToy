from __future__ import unicode_literals

__author__ = 'keaj'

import base64
import httplib2
import json
import os
import re

from apiclient import discovery
from oauth2client import client


class NoSuchBook(Exception):
    pass


class GoogleBooksService(object):
    def __init__(self):
        super(GoogleBooksService, self).__init__()
        self._credentials = None
        self.loadCredentialsAndAuthorize()

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
        self._credentials = client.SignedJwtAssertionCredentials(
            credinfo['web']['client_email'], key, scope,
            private_key_password='notasecret')
        http = httplib2.Http()
        self._httpClient = self._credentials.authorize(http)
        self._service = discovery.build('books', 'v1', http=self._httpClient)

    def recordToSerializable(self, record):
        try:
            record = record['items'][0]
        except KeyError:
            raise NoSuchBook

        volumeInfo = record['volumeInfo']
        requiredFields = ('industryIndentifiers','title')
        if any(field not in volumeInfo for field in requiredFields):
            # yes, some records are missing these!
            # we'll treat them as flat-out broken.
            raise NoSuchBook
        if set('ISBN_10','ISBN_13').isdisjoint(
                set(identifier['type']
                for identifier in volumeInfo['industryIdentifiers'])):
            # just in case there are industryIdentifiers but no ISBNs
            raise NoSuchBook

        qdict = {}
        qdict['publisher']=volumeInfo.get('publisher','')
        author = "&".join([authors for authors in volumeInfo.get('authors',[])])
        qdict['author']=author
        title = volumeInfo['title']
        subt = volumeInfo.get('subtitle','')
        title = ": ".join([title,subt]) if subt else title
        qdict['title']=title

        if 'publishedDate' in volumeInfo:
            date = volumeInfo['publishedDate']
            if re.match(r'[0-9]{4}-[0-9]{2}-[0-9]{2}',date):
                cleanedDate = date.split('-')[0]
            elif re.match(r'[0-9]{4}-[0-9]{2}', date):
                cleanedDate = date.split('-')[0]
            elif re.match(r'[0-9]{4}', date):
                cleanedDate = date
            else:
                raise ValueError('Unsupported publish date type: %s' % date)
            qdict['publish_date'] = cleanedDate

        for a in volumeInfo['industryIdentifiers']:
            if a['type']=='ISBN_13':
                qdict['isbn_13']=a['identifier']
            elif a['type']=='ISBN_10':
                qdict['isbn_10']=a['identifier']
        qdict['description']=volumeInfo.get('description',"")
        if 'categories' in volumeInfo:
            qdict['genre'] = "&".join([a for a in volumeInfo['categories']])
        return qdict

    def getByISBN(self, isbn):
        isbn = isbn.replace("-", '')
        if self._service:
            bookrecord = self._service.volumes().list(q="isbn:%s" % isbn).execute()
            return self.recordToSerializable(bookrecord)
