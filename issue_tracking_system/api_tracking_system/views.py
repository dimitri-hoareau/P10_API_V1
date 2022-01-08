from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .models import Contributors, Project, Issue, Comments
from .serializers import ContributorsSerializer, IssueSerializer, ProjectSerializer, CommentsSerializer, RegisterSerializer, UserSerializer
from rest_framework import generics, permissions, mixins
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
 

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

    def post(self, request, format=None):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

 

class IssuesFromProjectViewset(APIView):
 
    def get(self, request, id, *args, **kwargs):

        issues = Issue.objects.filter(project=id)
        serializer = IssueSerializer(issues, many=True)
        return Response(serializer.data)
    
    def post(self, request, id, *args, **kwargs):
        issues = Issue.objects.filter(project=id)
        serializer = IssueSerializer(issues, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class IssueFromProjectViewset(APIView):
 
    def delete(self, request, id, issue_id, format=None):
        print("==========================================================")
        print(id)
        print(issue_id)
        issue = Issue.objects.filter(id=issue_id)
        print(issue)
        issue.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




# faire un queryset avec filtre dasn l'url  ?
# API views plus facilement custom 
# https://www.django-rest-framework.org/tutorial/3-class-based-views/
#rename IssurFromProjectList, IssueFromProjectDetail