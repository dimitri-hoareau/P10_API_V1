"""issue_tracking_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api_tracking_system.views import *
router = routers.SimpleRouter()

router.register('contributors', ContributorsViewset, basename='contributors')
# router.register('projects', ProjectViewset, basename='project')
router.register('issue', IssueViewset, basename='issue')
router.register('comments', CommentsViewset, basename='comments')

 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('signup/', RegisterApi.as_view(), name='signup'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),

    # path('projects/<id>/issues/', IssuesFromProjectViewset.as_view(), name='issues_from_projet')
    path('projects/', ProjectViewsetList.as_view(), name='project_list'),
    path('projects/<id>/', ProjectViewsetDetail.as_view(), name='project_detail'),
    path('projects/<id>/issues', IssueFromProjectViewsetList.as_view(), name='issues_from_projet'),
    path('projects/<id>/users', UserFromProjectViewsetList.as_view(), name='users_from_projet'),
    path('projects/<id>/users/<user_id>', UserFromProjectViewsetDetail.as_view(), name='users_from_projet_detail'),
    path('projects/<id>/issues/<issue_id>', IssueFromProjectViewsetDetail.as_view(), name='issue_from_projet'),
    path('projects/<id>/issues/<issue_id>/comments', CommentsFromUserFromProjectViewsetList.as_view(), name='comments_from_users_from_projet_list'),
    path('projects/<id>/issues/<issue_id>/comments/<comment_id>', CommentsFromUserFromProjectViewsetDetail.as_view(), name='comments_from_users_from_projet_detail'),


]
 


# https://python.plainenglish.io/django-rest-framework-jwt-auth-with-login-and-register-77f830cd8789
# custom url avec routers avec de nouvelles vues
# enlever api des urls
# voir classes APIViews