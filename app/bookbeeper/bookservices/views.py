import datetime
import sys

from bookservices.models import LibraryBook, User, UserToStore, Store, Inventory
from bookservices.serializers import *
from django.contrib import auth
from rest_framework.views import APIView
from rest_framework.response import Response
from APIServices import GoogleBooksService
from rest_framework import status,mixins,generics,response
from utils.Exceptions import NoSuchBook
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from utils.Permissions import PostToInventoryPosition
from rest_framework import permissions

class LibraryBookList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):

    permission_classes = (permissions.IsAuthenticated,)
    queryset = LibraryBook.objects.all()
    serializer_class = LibraryBookSerializer

    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)

    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)

class LibraryBookImporterView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
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

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class=LibraryBookSerializer
    queryset = LibraryBook.objects.all()

    def get(self,request,*args,**kwargs):
        return self.retrieve(request,*args,**kwargs)

    def put(self,request, *args,**kwargs):
        return self.update(request,*args,**kwargs)

    def destroy(self,request,*args,**kwargs):
        return self.destroy(request,*args,**kwargs)

class UserList(generics.ListAPIView):
    permission_classes = (permissions.IsAdminUser,permissions.IsAuthenticated)
    queryset = User.objects.all()
    serializer_class=UserSerializer

class UserIndividual(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAdminUser,permissions.IsAuthenticated)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class InventoryList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated)
    queryset = Inventory.objects.all()
    serializer_class=InventorySerializer
    def pre_save(self,obj):
        obj.transaction_date=datetime.datetime.now()

class InventoryIndividual(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated)

    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer

class StoreList(generics.ListCreateAPIView):
    permission_classes=(permissions.IsAuthenticated)
    queryset=Store.objects.all()
    serializer_class = StoreSerializer

class StoreIndividual(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=(permissions.IsAuthenticated)
    queryset=Store.objects.all()
    serializer_class = StoreSerializer

class StoreToUserList(generics.ListCreateAPIView):
    permission_classes=(permissions.IsAuthenticated)
    queryset = UserToStore.objects.all()
    serializer_class=UserToStoreSerializer

class StoreToUserIndividual(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=(permissions.IsAuthenticated)
    queryset=UserToStore.objects.all()
    serializer_class = UserToStoreSerializer


class GetSessionUser(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request):
        user = auth.get_user(request)
        assert user.is_authenticated()
        return response.Response({'user': UserSerializer(user).data})


class Login(APIView):
    def post(self, request):
        form = AuthenticationForm(request, request.DATA)
        if not form.is_valid():
            return response.Response({'error': 'Login is incorrect'}, status=403)

        user = form.get_user()
        auth.login(request, user)
        return response.Response({'user': UserSerializer(user).data})


class Logout(APIView):
    def post(self, request):
        auth.logout(request)
        return response.Response({}, status=204)
