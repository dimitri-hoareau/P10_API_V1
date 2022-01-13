from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .models import Contributors, Project, Issue, Comments
from .serializers import ContributorsSerializer, IssueSerializer, ProjectSerializer, CommentsSerializer, RegisterSerializer, UserSerializer
from rest_framework import generics, permissions, mixins
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
from django.http import Http404
 

class ContributorsViewset(ModelViewSet):
 
    serializer_class = ContributorsSerializer
 
    def get_queryset(self):
        return Contributors.objects.all()

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


class ProjectViewsetList(APIView):
 
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

class ProjectViewsetDetail(APIView):

    def get_object(self, id):
        try:
            return Project.objects.filter(id=id)
        except Project.DoesNotExist:
            raise Http404
 
    def get(self, request, id, *args, **kwargs):

        projects = self.get_object(id)
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    def post(self, request, id, format=None):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id, format=None):
        project = Project.objects.get(id=id)
        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        project = self.get_object(id)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

 
class UserFromProjectViewsetList(APIView):
 
    def get(self, request, id, *args, **kwargs):

        contributor = Contributors.objects.filter(project=id)
        serializer = ContributorsSerializer(contributor, many=True)
        return Response(serializer.data)
    
    def post(self, request, id, *args, **kwargs):
        serializer = ContributorsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserFromProjectViewsetDetail(APIView):
    
 
    def get(self, request, id, user_id, *args, **kwargs):
        contributor = Contributors.objects.filter(project=id).filter(user=user_id)
        serializer = ContributorsSerializer(contributor, many=True)
        return Response(serializer.data)


    def delete(self, request, id, user_id, format=None):
        contributor = Contributors.objects.filter(project=id).filter(user=user_id)
        contributor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class IssueFromProjectViewsetList(APIView):
 
    def get(self, request, id, *args, **kwargs):

        issues = Issue.objects.filter(project=id)
        serializer = IssueSerializer(issues, many=True)
        return Response(serializer.data)
    
    def post(self, request, id, *args, **kwargs):
        serializer = IssueSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class IssueFromProjectViewsetDetail(APIView):


    def get(self, request, id, issue_id, *args, **kwargs):
        issues = Issue.objects.filter(id=issue_id)
        serializer = IssueSerializer(issues, many=True)
        return Response(serializer.data)


    def put(self, request, id, issue_id, format=None):
        issue = Issue.objects.get(id=issue_id)
        serializer = IssueSerializer(issue, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
 
    def delete(self, request, id, issue_id, format=None):
        issue = Issue.objects.filter(id=issue_id)
        issue.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentsFromUserFromProjectViewsetList(APIView):

    def get(self, request, id, issue_id, *args, **kwargs):

        comments = Comments.objects.filter(issue=issue_id)
        serializer = CommentsSerializer(comments, many=True)
        return Response(serializer.data)
    
    def post(self, request, id, issue_id, *args, **kwargs):
        serializer = CommentsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentsFromUserFromProjectViewsetDetail(APIView):


    def get(self, request, id, issue_id, comment_id, *args, **kwargs):
        comment = Comments.objects.filter(id=comment_id)
        serializer = CommentsSerializer(comment, many=True)
        return Response(serializer.data)


    def put(self, request, id, issue_id, comment_id, format=None):
        comment = Comments.objects.get(id=comment_id)
        serializer = CommentsSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
 
    def delete(self, request, id, issue_id, comment_id, format=None):
        comment = Comments.objects.filter(id=comment_id)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




# http://127.0.0.1:8000/projects/1/users : rajoute pas a un projet spécifique , forcer l'id du project (voir avec postman)
#bloquer les contributor par projet, une seule fois !
# ou enlever project dans le serialiser ?