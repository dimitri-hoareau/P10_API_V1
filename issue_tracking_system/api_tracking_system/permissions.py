from operator import truediv
from rest_framework.permissions import BasePermission
from .models import Contributors, Project, Issue, Comments
 
class IsAdminAuthenticated(BasePermission):
    
 
    def has_permission(self, request, view):
        SAFE_METHODS = ['GET', 'POST']
        if (request.method in SAFE_METHODS and
        request.user and
        request.user.is_authenticated):
            return True
        else:
            if request.user:
                project = Project.objects.get(id=view.kwargs["id"])
                if project.author == request.user:
                    return True
                else:
                    return False
        return False

        #recuperer la méthode pour authoriser.. GET POST...

    # Ne donnons l’accès qu’aux utilisateurs administrateurs authentifiés
        # return bool(request.user and request.user.is_authenticated and request.user.is_superuser)