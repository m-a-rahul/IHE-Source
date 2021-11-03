from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import PatientSerializer, HospitalSerializer


class GetUserDetails(APIView):
    @staticmethod
    @csrf_exempt
    def get(request):
        try:
            if request.user.username[2] == "P":
                serializer = PatientSerializer(request.user.patient, many=False)
            elif request.user.username[2] == "H":
                serializer = HospitalSerializer(request.user.hospital, many=False)
            return Response(serializer.data)
        except:
            return Response('RelatedObjectDoesNotExist', status=status.HTTP_200_OK)


class CreateUpdateUserDetails(APIView):
    @staticmethod
    @csrf_exempt
    def post(request):
        request.data['user'] = request.user.id
        if request.data['update']:
            print('Update')
            try:
                if request.user.username[2] == "P":
                    serializer = PatientSerializer(instance=request.user.patient, data=request.data)

                elif request.user.username[2] == "H":
                    serializer = HospitalSerializer(instance=request.user.hospital, data=request.data)
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            print('Create')
            if request.user.username[2] == "P":
                serializer = PatientSerializer(data=request.data)
            elif request.user.username[2] == "H":
                serializer = HospitalSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

