import httplib2
import os, json,copy,re
import base64
from apiclient.discovery import build
from oauth2client.client import SignedJwtAssertionCredentials


0
class BookService(object):

    def __init__(self):
        super(BookService,self).__init__()
        self._googlebooks = GoogleBooksService()
        self._db = db.getDB()

    def getBookFromCacheByISBN(self,isbn):
        bookfromcache = None
        db_ = self._db
        try:
            isbn = re.sub(r'[-|\s]','',isbn)
            searchterm = 'isbn-13'
            if len(isbn)==10:
                searchterm = 'isbn-10'
            books = db_.books.find({searchterm:isbn})
            bookfromcache = books[0]
        except (AttributeError,IndexError) as e:
            bookfromcache = None
        return bookfromcache

    def addBookToLibrary(self,bookAsLibFormat):
        i13 = bookAsLibFormat['isbn-13']
        jsonquery = {"isbn-13":i13}
        try:
            self._db.books.find(jsonquery)[0]
        except IndexError:
            flask.current_app.logger.info("Adding book with isbn-13 %s to library."%i13)
            self._db.books.save(bookAsLibFormat)

    def addBook(self,bookAsGBJson):
        gbook = bookAsGBJson[u'items'][0]
        #is it already there?
        nubook = {}
        nubook['publisher']=gbook[u'volumeInfo'].get(u'publisher',"")
        nubook['type']=u'book'
        nubook['description']=gbook[u'volumeInfo'].get(u'description',"")
        nubook['title']=gbook[u'volumeInfo'][u'title']
        nubook['authors'] = copy.copy(gbook[u'volumeInfo'].get(u'authors',[]))
        nubook['publish_date']=gbook[u'volumeInfo'].get(u'publishedDate',"")
        isbns = gbook[u'volumeInfo'][u'industryIdentifiers']
        for id in isbns:
            if id[u'type']==u'ISBN_13':
                nubook['isbn-13'] = id[u'identifier']
            elif id[u'type']==u'ISBN_10':
                nubook['isbn-10'] = id[u'identifier']
        self.addBookToLibrary(nubook)

    def getAllBooks(self):
        allthebooks=self._db.books.find()
        return [book for book in allthebooks]

    def getBook(self, isbn):
        book = self.getBookFromCacheByISBN(isbn)
        if not book:
            self.addBook(self._googlebooks.getByISBN(isbn))
            book = self.getBookFromCacheByISBN(isbn)
        return book
