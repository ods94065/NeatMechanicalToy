from django.db import models
from django.contrib.auth.models import User,Group

class LibraryBook(models.Model):
    isbn_13=models.BigIntegerField("ISBN-13",primary_key=True,unique=True,db_index=True)
    isbn_10=models.PositiveIntegerField("ISBN-10",blank=True)
    title=models.CharField( "Title of book",max_length=250, blank = False,db_index=True)
    author=models.TextField("Comma-separated lis of authors.",max_length=1000)
    publisher=models.CharField("Name of imprint or publisher.",blank=False,max_length=200)
    publish_date = models.DateField("Publication date",null=True)
    description=models.TextField("Summary of book",max_length=2000,blank=True)

class Inventory(models.Model):
    book=models.ForeignKey(LibraryBook,null=False,db_index=True)
    quantity=models.IntegerField("Number of items in inventory",default=0,null=False)

class Store(models.Model):
    name = models.CharField("Name of Store",unique=True,max_length=100)
    allowedUsers = models.ManyToManyField(User,related_name="stores")
    inventory=models.ForeignKey(Inventory)

class UserToStore():
    READ='r'
    WRITE='w'
    READ_WRITE='rw'
    PERMISSION_CHOICES=(
        (READ,'Read'),
        (WRITE,'Write'),
        (READ_WRITE,'Read-Write')
    )
    user=models.ForeignKey(User,null=False)
    store=models.ForeignKey(Store,null=False)
    permission=models.CharField("Kind of access granted to user.",choices=PERMISSION_CHOICES,blank=False,default=READ_WRITE)




# Create your models here.
