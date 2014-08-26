from django.forms import widgets
from rest_framework import serializers
from models import LibraryBook,Store,UserToStore,Inventory
from django.contrib.auth.models import User


class LibraryBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = LibraryBook
        fields = ('isbn_13','isbn_10','title','author','publisher','genre','publish_date','description')
    def restore_object(self, attrs, instance=None):
        return super(LibraryBookSerializer,self).restore_object(attrs,instance)
    def is_valid(self):
        return super(LibraryBookSerializer,self).is_valid()
    def __unicode__(self):
        return "%s:%s"%(self.isbn_13,self.title)

class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields=('name','allowedUsers')
    def restore_object(self,attrs,instance=None):
        return super(StoreSerializer,self).restore_object(attrs,instance)
    def is_valid(self):
        return super(StoreSerializer,self).is_valid()



class InventorySerializer(serializers.ModelSerializer):
    book = serializers.PrimaryKeyRelatedField(source='book',many=False)
    store = serializers.PrimaryKeyRelatedField(source='store',many=False)
    transaction_date = serializers.Field(source='transaction_date')
    class Meta:
        model = Inventory
        fields = ('book','transaction_date','transaction_type','store')
    def restore_object(self,attrs,instance=None):
        return super(InventorySerializer,self).restore_object(attrs,instance)
    def is_valid(self):
        return super(InventorySerializer,self).is_valid()

class UserSerializer(serializers.ModelSerializer):
    storerel = serializers.PrimaryKeyRelatedField(many=True)
    class Meta:
        model=User
        fields=('id','username','storerel')


class UserToStoreSerializer(serializers.ModelSerializer):
    store = serializers.PrimaryKeyRelatedField(many=False)
    user = serializers.PrimaryKeyRelatedField(many=False)
    class Meta:
        model = UserToStore
        fields=('user','store','permission')
