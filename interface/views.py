from django.shortcuts import render

from rest_framework import views, serializers
from rest_framework.response import Response

# Create your views here.


class CreatePingView(views.APIView):

    class InputSerializer(serializers.Serializer):
        location = serializers.CharField()

    def post(self, request):
        input_serializer = self.InputSerializer(data=request.data)

        return Response()


class GetPingsView(views.APIView):

    def get(self, request):

        return Response()