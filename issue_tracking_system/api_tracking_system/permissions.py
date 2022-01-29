from operator import truediv
from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Contributors, Project, Issue, Comments
 

class ProjectIsAuthorOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        # return request.user and request.user.is_authenticated
        return True

    def has_object_permission(self, request, view, obj):

        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user

class IssueIsAuthorOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        # return request.user and request.user.is_authenticated
        return True

    def has_object_permission(self, request, view, obj):
        print(obj.author)
        print(request.user)

        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user

class CommentsIsAuthorOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        # return request.user and request.user.is_authenticated
        return True

    def has_object_permission(self, request, view, obj):

        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user



# 3 différents mais la meme chose ???
# est ce que isAuthenticated utile ? ou juste la permission custom pour list et detail