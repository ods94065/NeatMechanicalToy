from rest_framework.permissions import BasePermission
from bookservices.models import UserToStore

from django.contrib.auth.models import User

class PostToInventoryPosition(BasePermission):
    def has_permission(self,request,view):
        #figure out how to edit the session cookie. You want to mess with that instead of the request itself.
        try:
            if request.method==u'PUT' or request.method==u'POST':
                storeid = request.session.get('store', None)
                usertostore = UserToStore.objects.all().filter(user=request.user.id,store=storeid)
                if usertostore:
                    return True
            else:
                return True
        except Exception as e:
            return False

