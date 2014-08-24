from django.forms import widgets
from rest_framework import serializers
from models import LibraryBook


class LibraryBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = LibraryBook
        fields = ('isbn_13','isbn_10','title','author','publisher','genre','publish_date','description')
    def restore_object(self, attrs, instance=None):
        return super(LibraryBookSerializer,self).restore_object(attrs,instance)
    def is_valid(self):
        return super(LibraryBookSerializer,self).is_valid()
