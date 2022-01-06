from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .models import Contributors, Project, Issue, Comments
from .serializers import ContributorsSerializer, IssueSerializer, ProjectSerializer, CommentsSerializer, RegisterSerializer, UserSerializer
from rest_framework import generics, permissions, mixins
from rest_framework.response import Response
from django.contrib.auth.models import User
 

class ContributorsViewset(ModelViewSet):
 
    serializer_class = ContributorsSerializer
 
    def get_queryset(self):
        return Contributors.objects.all()

# class ProjectViewset(ModelViewSet):
 
#     serializer_class = ProjectSerializer
 
#     def get_queryset(self):
#         return Project.objects.all()

class IssueViewset(ModelViewSet):
 
    serializer_class = IssueSerializer
 
    def get_queryset(self):
        return Issue.objects.all()

class CommentsViewset(ModelViewSet):
 
    serializer_class = CommentsSerializer
 
    def get_queryset(self):
        return Comments.objects.all()

#Register API
class RegisterApi(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user,    
            context=self.get_serializer_context()).data,
            "message": "User Created Successfully.  Now perform Login to get your token",
        })


class ProjectViewset(APIView):
 
    def get(self, *args, **kwargs):

        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)
 

class IssueFromProjectViewset(APIView):
 
    def get(self, request, id, *args, **kwargs):

        print(id)

        issues = Issue.objects.filter(project=id)
        # projects = Project.objects.all()
        print(issues)

        serializer = IssueSerializer(issues, many=True)
        return Response(serializer.data)



# faire un queryset avec filtre dasn l'url  ?
# API views plus facilement custom 