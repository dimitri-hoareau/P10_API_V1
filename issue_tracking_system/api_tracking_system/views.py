from django.shortcuts import render


from rest_framework.views import APIView
from rest_framework.response import Response
 
from .models import Contributors
from .serializers import ContributorsSerializer
 
class ContributorsAPIView(APIView):
 
    def get(self, *args, **kwargs):
        contributors = Contributors.objects.all()
        serializer = ContributorsSerializer(contributors, many=True)
        return Response(serializer.data)
