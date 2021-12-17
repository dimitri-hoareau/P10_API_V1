from rest_framework.serializers import ModelSerializer
 
from .models import Contributors
 
class ContributorsSerializer(ModelSerializer):
 
    class Meta:
        model = Contributors
        fields = ['id', 'permission']