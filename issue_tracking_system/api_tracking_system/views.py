from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Contributors, Project, Issue, Comments
from .serializers import ContributorsSerializer, IssueSerializer, ProjectSerializer, CommentsSerializer
 

class ContributorsViewset(ModelViewSet):
 
    serializer_class = ContributorsSerializer
 
    def get_queryset(self):
        return Contributors.objects.all()

class ProjectViewset(ModelViewSet):
 
    serializer_class = ProjectSerializer
 
    def get_queryset(self):
        return Project.objects.all()

class IssueViewset(ModelViewSet):
 
    serializer_class = IssueSerializer
 
    def get_queryset(self):
        return Issue.objects.all()

class CommentsViewset(ModelViewSet):
 
    serializer_class = CommentsSerializer
 
    def get_queryset(self):
        return Comments.objects.all()