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

        print(type(request.user))
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

    def post(self, request, id, format=None):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
 
    def get(self, request, id, user_id, *args, **kwargs):
        contributor = Contributors.objects.filter(project=id).filter(user=user_id)
        serializer = ContributorsSerializer(contributor, many=True)
        return Response(serializer.data)


    def delete(self, request, id, user_id, format=None):
        contributor = Contributors.objects.filter(project=id).filter(user=user_id)
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
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class IssueFromProjectViewsetDetail(APIView):

    permission_classes = [IsAuthenticated, IssueIsAuthorOrReadOnly]
 
    def get_object(self, id, method):
        try:
            obj = Issue.objects.get(id=id)
            self.check_object_permissions(self.request, obj)
            if method == "get" or method == "delete":
                obj = Issue.objects.filter(id=id)
            return obj
        except Issue.DoesNotExist:
            raise Http404

    def get(self, request, id, issue_id, *args, **kwargs):
        issues = self.get_object(issue_id, "get")
        # issues = Issue.objects.filter(id=issue_id)
        serializer = IssueSerializer(issues, many=True)
        return Response(serializer.data)


    def put(self, request, id, issue_id, format=None):
        # issue = Issue.objects.get(id=issue_id)
        issue = self.get_object(issue_id, "put")
        serializer = IssueSerializer(issue, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
 
    def delete(self, request, id, issue_id, format=None):
        issue = self.get_object(issue_id, "delete")
        # issue = Issue.objects.filter(id=issue_id)
        issue.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentsFromUserFromProjectViewsetList(APIView):
    permission_classes = [IsAuthenticated]

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

    permission_classes = [IsAuthenticated, CommentsIsAuthorOrReadOnly]

    def get_object(self, id, method):
        #TODO get only comments from the id_issue
        try:
            obj = Comments.objects.get(id=id)
            self.check_object_permissions(self.request, obj)
            if method == "get" or method == "delete":
                obj = Comments.objects.filter(id=id)
            return obj
        except Comments.DoesNotExist:
            raise Http404


    def get(self, request, id, issue_id, comment_id, *args, **kwargs):
        comment = self.get_object(comment_id, "get")
        # comment = Comments.objects.filter(id=comment_id)
        serializer = CommentsSerializer(comment, many=True)
        return Response(serializer.data)


    def put(self, request, id, issue_id, comment_id, format=None):
        # comment = Comments.objects.get(id=comment_id)
        comment = self.get_object(comment_id, "put")
        serializer = CommentsSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
 
    def delete(self, request, id, issue_id, comment_id, format=None):
        # comment = Comments.objects.filter(id=comment_id)
        comment = self.get_object(comment_id, "delete")
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




# tout le monde peut supprimer les contributeurs // non seul le créateur du projet en question

# reste a tester : permission pour http://127.0.0.1:8000/projects/1/issues/7