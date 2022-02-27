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
from rest_framework.permissions import IsAuthenticated
from api_tracking_system.permissions import ProjectIsAuthorOrReadOnly, IssueIsAuthorOrReadOnly, CommentsIsAuthorOrReadOnly, UsersIsAuthorOrReadOnly
 



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
    permission_classes = [IsAuthenticated]

    def get(self, request,  *args, **kwargs):

        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProjectViewsetDetail(APIView):

    permission_classes =  [IsAuthenticated,ProjectIsAuthorOrReadOnly]

    def get_object(self, id, method):
        try:
            obj = Project.objects.get(id=id)
            self.check_object_permissions(self.request, obj)
            if method == "get" or method == "delete":
                obj = Project.objects.filter(id=id)
            return obj
        except Project.DoesNotExist:
            raise Http404
 
    def get(self, request, id, *args, **kwargs):

        projects = self.get_object(id, "get")
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    def put(self, request, id, format=None):
        project = self.get_object(id, "put")
        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        project = self.get_object(id, "delete")
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

 
class UserFromProjectViewsetList(APIView):
    permission_classes = [IsAuthenticated]
 
    def get(self, request, id, *args, **kwargs):

        contributor = Contributors.objects.filter(project=id)
        serializer = ContributorsSerializer(contributor, many=True)
        return Response(serializer.data)
    
    def post(self, request, id, *args, **kwargs):
        contributors = Contributors.objects.filter(project=id)
        serializer = ContributorsSerializer(data=request.data)
        project = Project.objects.get(id=id)
        if serializer.is_valid():
            validatedData = serializer.validated_data
            user_name = validatedData.get('user')
            for contributor in contributors:
                # if user_name == contributor.user and project == validatedData.get('project'):
                if user_name == contributor.user:
                    return Response({"Error": "this user is already a contributor for this project"}, status=status.HTTP_400_BAD_REQUEST)

            #force to save the contributor on the project 
            serializer.save(project=project)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserFromProjectViewsetDetail(APIView):

    permission_classes = [IsAuthenticated, UsersIsAuthorOrReadOnly]

    def get_object(self, id, user_id, method):
        try:
            obj = Contributors.objects.filter(project=id).filter(user=user_id)
            self.check_object_permissions(self.request, obj)
            return obj
        except Issue.DoesNotExist:
            raise Http404
 
    def get(self, request, id, user_id, *args, **kwargs):
        contributor = self.get_object(id, user_id, "get")
        serializer = ContributorsSerializer(contributor, many=True)
        return Response(serializer.data)


    def delete(self, request, id, user_id, format=None):
        contributor = self.get_object(id, user_id, "get")
        contributor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class IssueFromProjectViewsetList(APIView):
    permission_classes = [IsAuthenticated]
 
    def get(self, request, id, *args, **kwargs):
        issues = Issue.objects.filter(project=id)
        serializer = IssueSerializer(issues, many=True)
        return Response(serializer.data)
    
    def post(self, request, id, *args, **kwargs):
        serializer = IssueSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class IssueFromProjectViewsetDetail(APIView):

    permission_classes = [IsAuthenticated, IssueIsAuthorOrReadOnly]
 
    def get_object(self, project_id, id, method):
        try:
            obj = Issue.objects.filter(project=project_id).get(id=id)
            self.check_object_permissions(self.request, obj)
            if method == "get" or method == "delete":
                obj = Issue.objects.filter(project=project_id).filter(id=id)
            return obj
        except Issue.DoesNotExist:
            raise Http404

    def get(self, request, id, issue_id, *args, **kwargs):
        issues = self.get_object(id, issue_id, "get")
        serializer = IssueSerializer(issues, many=True)
        return Response(serializer.data)


    def put(self, request, id, issue_id, format=None):
        issue = self.get_object(id, issue_id, "put")
        serializer = IssueSerializer(issue, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
 
    def delete(self, request, id, issue_id, format=None):
        issue = self.get_object(id,issue_id, "delete")
        issue.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentsFromUserFromProjectViewsetList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id, issue_id, *args, **kwargs):

        if Issue.objects.filter(project=id).filter(id=issue_id):
            comments = Comments.objects.filter(issue=issue_id)
            serializer = CommentsSerializer(comments, many=True)
            return Response(serializer.data)
        else:
            raise Http404

    def post(self, request, id, issue_id, *args, **kwargs):
        if Issue.objects.filter(project=id).filter(id=issue_id):
            serializer = CommentsSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(author=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            raise Http404



class CommentsFromUserFromProjectViewsetDetail(APIView):

    permission_classes = [IsAuthenticated, CommentsIsAuthorOrReadOnly]

    def get_object(self,project_id, issue_id, id, method):
        if Issue.objects.filter(project=project_id).filter(id=issue_id) and Comments.objects.get(id=id).issue.id == int(issue_id):
            try:
                obj = Comments.objects.get(id=id)
                self.check_object_permissions(self.request, obj)
                if method == "get" or method == "delete":
                    obj = Comments.objects.filter(id=id)
                return obj
            except Comments.DoesNotExist:
                raise Http404
        else:
            raise Http404

    def get(self, request, id, issue_id, comment_id, *args, **kwargs):
        comment = self.get_object(id, issue_id, comment_id, "get")
        serializer = CommentsSerializer(comment, many=True)
        return Response(serializer.data)


    def put(self, request, id, issue_id, comment_id, format=None):
        comment = self.get_object(id, issue_id, comment_id, "put")
        serializer = CommentsSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
 
    def delete(self, request, id, issue_id, comment_id, format=None):
        comment = self.get_object(id, issue_id, comment_id, "delete")
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

