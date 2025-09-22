from rest_framework import permissions

class IsOwnerOrAdmin(permissions.BasePermission):
    """ فقط صاحب سفارش و ادمین دسترسی دارند"""
    def has_object_permission(self,request,view,obj):
        return object.user== request.user or request.user.is_staff