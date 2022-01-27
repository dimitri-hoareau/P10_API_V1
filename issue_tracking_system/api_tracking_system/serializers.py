from rest_framework.serializers import ModelSerializer
from rest_framework import  serializers
from rest_framework.permissions import IsAuthenticated
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
 
from .models import Contributors, Project, Issue, Comments
 
class ContributorsSerializer(ModelSerializer):
 
    class Meta:
        model = Contributors
        fields = ['id', 'permission', 'role', 'project', 'user']

class ProjectSerializer(ModelSerializer):
 
    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type']
        # serializers.save()

class IssueSerializer(ModelSerializer):

    # project = ProjectSerializer()
 
    class Meta:
        model = Issue
        fields = ['id', 'title', 'description', 'tag', 'status', 'created_time', 'priority', 'project', 'author', 'assignee' ]

class CommentsSerializer(ModelSerializer):
 
    class Meta:
        model = Comments
        fields = ['id', 'description', 'created_time', 'issue', 'author']


# class IssuesFromProjectSerialize(ModelSerializer):

#         class Meta:
#             model = Comments
#             fields = ['id', 'description', 'created_time', 'issue', 'author']




# Register serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','password','first_name', 'last_name')
        extra_kwargs = {
            'password':{'write_only': True},
        }     
        
    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'],     
        password = validated_data['password']  ,
        first_name=validated_data['first_name'],  
        last_name=validated_data['last_name'])
        return user
        
# User serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'





#comment avoir les infos détaillées pour author ?

#         # serializers.save() overiding serialiser pour l'author