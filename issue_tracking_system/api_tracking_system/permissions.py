from operator import truediv
from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Contributors, Project, Issue, Comments
 

class ProjectIsAuthorOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        # return request.user and request.user.is_authenticated
        return True

    def has_object_permission(self, request, view, obj):
        is_contributor = False
        contributors = Contributors.objects.filter(project=obj.id)
        for contributor in contributors:
            if request.user == contributor.user:
                is_contributor = True

        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if  request.method in SAFE_METHODS and is_contributor:
            return True
        return obj.author == request.user

class IssueIsAuthorOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        # return request.user and request.user.is_authenticated
        return True

    def has_object_permission(self, request, view, obj):
        is_contributor = False
        contributors = Contributors.objects.filter(project=obj.id)
        for contributor in contributors:
            if request.user == contributor.user:
                is_contributor = True

        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in SAFE_METHODS and is_contributor:
            return True
        return obj.author == request.user

class CommentsIsAuthorOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        # return request.user and request.user.is_authenticated
        return True

    def has_object_permission(self, request, view, obj):
        is_contributor = False
        contributors = Contributors.objects.filter(project=obj.id)
        for contributor in contributors:
            if request.user == contributor.user:
                is_contributor = True

        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in SAFE_METHODS and is_contributor:
            return True
        return obj.author == request.user


class UsersIsAuthorOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        # return request.user and request.user.is_authenticated
        return True

    def has_object_permission(self, request, view, obj):
        is_contributor = False
        contributors = Contributors.objects.filter(project=obj.id)
        for contributor in contributors:
            if request.user == contributor.user:
                is_contributor = True

        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in SAFE_METHODS and is_contributor:
            return True
        return obj.author == request.user


