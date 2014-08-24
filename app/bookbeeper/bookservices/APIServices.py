__author__ = 'keaj'
import httplib2
import os, json,copy,re
import base64
from apiclient.discovery import build
from oauth2client.client import SignedJwtAssertionCredentials



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
            credinfo[u'web'][u'client_email'], key, scope, 'notasecret')
        http = httplib2.Http()
        self._httpClient = self._credentials.authorize(http)
        self._service = build('books', 'v1', http=self._httpClient)

    def __init__(self):
        super(GoogleBooksService, self).__init__()
        self._credentials = None
        self.loadCredentialsAndAuthorize()

    def recordToSerializable(self, record):
        record = record[u'items'][0]
        qdict = {}
        qdict[u'publisher']=record[u'volumeInfo'][u'publisher']
        author = "&".join([authors for authors in record[u'volumeInfo'][u'authors']])
        qdict[u'author']=unicode(author)
        title = record[u'volumeInfo'][u'title']
        subt = ""
        try:
            subt = record[u'volumeInfo'][u'subtitle']
        except KeyError:
            pass
            #swallow the exception
        title = ":".join([title,subt]) if subt else title
        qdict[u'title']=unicode(title)
        qdict[u'publish_date']=unicode("%s-01-01"%(record[u'volumeInfo'][u'publishedDate']))
        for a in record[u'volumeInfo'][u'industryIdentifiers'] :
            if a[u'type']=='ISBN_13':
                qdict[u'isbn_13']=a[u'identifier']
            elif a[u'type']=='ISBN_10':
                qdict[u'isbn_10']=a[u'identifier']
        qdict[u'description']=record[u'volumeInfo'].get(u'description',"")

        return qdict

    def getByISBN(self, isbn):
        isbn = isbn.replace("-", '')
        if self._service:
            bookrecord = self._service.volumes().list(q="isbn:%s" % isbn).execute()
            return self.recordToSerializable(bookrecord)
