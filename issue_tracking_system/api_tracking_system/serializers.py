from rest_framework.serializers import ModelSerializer
 
from .models import Contributors, Project, Issue, Comments
 
class ContributorsSerializer(ModelSerializer):
 
    class Meta:
        model = Contributors
        fields = ['id', 'permission']

class ProjectSerializer(ModelSerializer):
 
    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type']

class IssueSerializer(ModelSerializer):
 
    class Meta:
        model = Issue
        fields = ['id', 'title', 'description', 'tag', 'status', 'created_time']

class CommentsSerializer(ModelSerializer):
 
    class Meta:
        model = Comments
        fields = ['id', 'description', 'created_time']