from bookservices.models import LibraryBook
from bookservices.serializers import LibraryBookSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from APIServices import GoogleBooksService
from rest_framework import status,mixins,generics
from utils.Exceptions import NoSuchBook


class LibraryBookList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = LibraryBook.objects.all()
    serializer_class = LibraryBookSerializer

    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)

    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)

class LibraryBookImporterView(APIView):
    def get(self,request,pk,format=None):
        book = None
        try:
            book = LibraryBook.objects.get(isbn_13=pk)
            serializer = LibraryBookSerializer(book)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception:
            #go find it on google books!
            try:
                gbs = GoogleBooksService()
                book = gbs.getByISBN(str(pk))
                serializer = LibraryBookSerializer(data = book)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data,status=status.HTTP_201_CREATED)
                else:
                   return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
            except NoSuchBook:
                return Response({'requested_isbn':pk,'error':"Book could not be imported. Likely, the ISBN is wrong, but the book could also be rare. If this is the case, you can enter it manually.",
                                 }, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({'requested_isbn':pk,'error':e.message},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LibraryBookIndividual(mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.DestroyModelMixin,
                            generics.GenericAPIView):

    serializer_class=LibraryBookSerializer
    queryset = LibraryBook.objects.all()

    def get(self,request,*args,**kwargs):
        return self.retrieve(request,*args,**kwargs)

    def put(self,request, *args,**kwargs):
        return self.update(request,*args,**kwargs)

    def destroy(self,request,*args,**kwargs):
        return self.destroy(request,*args,**kwargs)