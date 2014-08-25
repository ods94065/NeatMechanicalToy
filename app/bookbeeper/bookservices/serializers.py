from django.forms import widgets
from rest_framework import serializers
from models import LibraryBook,Store,UserToStore,Inventory


class LibraryBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = LibraryBook
        fields = ('isbn_13','isbn_10','title','author','publisher','genre','publish_date','description')
    def restore_object(self, attrs, instance=None):
        return super(LibraryBookSerializer,self).restore_object(attrs,instance)
    def is_valid(self):
        return super(LibraryBookSerializer,self).is_valid()

class InventorySerializer(serializers.ModelSerializer):
    book = LibraryBookSerializer(many=False)
    class Meta:
        model = Inventory
        fields = ('book','quantity','store')
    def restore_object(self,attrs,instance=None):
        return super(InventorySerializer,self).restore_object(attrs,instance)
    def is_valid(self):
        return super(InventorySerializer,self).is_valid()

class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields=('name','allowedUsers')
    def restore_object(self,attrs,instance=None):
        return super(StoreSerializer,self).restore_object(attrs,instance)
    def is_valid(self):
        return super(StoreSerializer,self).is_valid()


class UserToStoreSerializer(serializers.ModelSerializer):
    stores = StoreSerializer(source='store_set',many=True)
    class Meta:
        model = UserToStore
        fields=('user','store','permission')
