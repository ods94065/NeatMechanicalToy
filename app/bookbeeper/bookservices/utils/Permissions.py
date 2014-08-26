from rest_framework.permissions import BasePermission
from bookservices.models import UserToStore

from django.contrib.auth.models import User

class PostToInventoryPosition(BasePermission):
    def has_permission(self,request,view):
        try:
            userpk = User.objects.get(id=request.user.id)
            if request.method==u'PUT' or request.method==u'POST':
                storeid = request.data['store']
                usertostore = UserToStore.objects.find(user=userpk.id,store=storeid)
                if usertostore:
                    return True
            else:
                return True
        except Exception as e:
            return False

