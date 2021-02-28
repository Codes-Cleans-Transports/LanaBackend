from django.shortcuts import render
from datetime import datetime

from rest_framework import views, serializers
from rest_framework.response import Response

from core.logic import acceptPing, DevicePing, getClusters, getClusterGrouped

import jsonpickle

# Create your views here.


class CreatePingView(views.APIView):

    class InputSerializer(serializers.Serializer):
        location = serializers.CharField()

    def post(self, request, cluster_id, device_id):
        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid()

        acceptPing(DevicePing(id=device_id, clusterId=cluster_id, location=input_serializer.data['location']))

        return Response()


class GetClusterView(views.APIView):

    def get(self, request, cluster_id):

        nodes = getClusterGrouped(cluster_id=cluster_id)
        
        return Response(data=jsonpickle.encode(nodes))

class ListClustersView(views.APIView):

    def get(self, request):
        return Response(data=getClusters())
