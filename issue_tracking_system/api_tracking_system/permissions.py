from operator import truediv
from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Contributors, Project, Issue, Comments
 
class IsAdminAuthenticated(BasePermission):
    
    def has_permission(self, request, view):
        print(view.kwargs)
        SAFE_METHODS = ['GET', 'POST']
        if (request.method in SAFE_METHODS and
        request.user and
        request.user.is_authenticated):
            return True
        else:
            if request.user:
                if "id" in view.kwargs:
                    project = Project.objects.get(id=view.kwargs["id"])
                    if "issue_id" in view.kwargs:
                        issue = Issue.objects.get(id=view.kwargs["issue_id"])
                        if "comment_id" in view.kwargs:
                            comment = Comments.objects.get(id=view.kwargs["comment_id"])
                            if comment.author == request.user:
                                return True
                        if issue.author == request.user:
                            return True
                    if project.author == request.user:
                        return True
                    else:
                        return False
        return False

class ProjectIsAuthorOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        print("has_permission`")
        # return request.user and request.user.is_authenticated
        return True

    def has_object_permission(self, request, view, obj):
        print("oooooooooooooooooooooooooooooooooooooooooooo")
        print(obj)
        print(obj.author)
        print(request.method)
        print(SAFE_METHODS)
        print(request.method)
        print(request.user)
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in SAFE_METHODS:
            print("heeeeeeeeeeeeeerrre1111111")
            return True
        print("heeeeeeeeeeeeeerrre2")
        print(obj.author)
        print(request.user)
        return obj.author == request.user


        # Instance must have an attribute named `owner`.
        # return obj.author == request.user
 


#has object permission, 3 classes 
#creer project permission, commetnpermission
        # return bool(request.user and request.user.is_authenticated and request.user.is_superuser)

    # has object permission marche pas avec put