from rest_framework import permissions

class IsCurrentUserOwnerOrReadOnly(permissions.BasePermission):
  def has_object_permission(self, request, view, obj):
    if request.method in permissions.SAFE_METHODS:
      return True
    else:
      return obj.owner == request.user

class IsAdminOrOwner(permissions.BasePermission):
  def has_object_permission(self, request, view, obj):
    if request.method in permissions.SAFE_METHODS:
      return True
    else: 
      return obj.user == request.user or obj.profile.role == 3 

class IsAdmin(permissions.BasePermission):
  def has_permission(self, request, view):
    return request.user.profile.role == 3