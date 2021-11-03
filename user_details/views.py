from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import PatientSerializer, HospitalSerializer


class Patient(APIView):
    @staticmethod
    @csrf_exempt
    def post(request):
        if not request.user.username[2] == "P":
            return Response("Invalid", status=status.HTTP_400_BAD_REQUEST)
        # _mutable = request.data._mutable
        # request.data._mutable = True
        request.data['user'] = request.user.id
        # request.data._mutable = _mutable
        serializer = PatientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Hospital(APIView):

    @staticmethod
    @csrf_exempt
    def post(request):
        if not request.user.username[2] == "H":
            return Response("Invalid", status=status.HTTP_400_BAD_REQUEST)
        # _mutable = request.data._mutable
        # request.data._mutable = True
        request.data['user'] = request.user.id
        # request.data._mutable = _mutable
        serializer = HospitalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
