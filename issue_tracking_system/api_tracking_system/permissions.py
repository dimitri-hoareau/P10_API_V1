from operator import truediv
from rest_framework.permissions import BasePermission
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
                # if view.kwargs["id"]:
                if "id" in view.kwargs:
                    project = Project.objects.get(id=view.kwargs["id"])
                    # if view.kwargs["issue_id"]:
                    if "issue_id" in view.kwargs:
                        issue = Issue.objects.get(id=view.kwargs["issue_id"])
                        # if view.kwargs["comment_id"]:
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

        #recuperer la méthode pour authoriser.. GET POST...

    # Ne donnons l’accès qu’aux utilisateurs administrateurs authentifiés
        # return bool(request.user and request.user.is_authenticated and request.user.is_superuser)