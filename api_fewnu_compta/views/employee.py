from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from django.http import HttpResponse

from ..models import Employee
from ..serializers import EmployeeSerializer

class EmployeeList(APIView):

    def get(self, request, format=None):
        employees = Employee.objects.filter(archived=False).all()
        serializer = EmployeeSerializer(employees, many=True)

        return Response(serializer.data, status=200)
        
class CreateEmployee(generics.CreateAPIView):
    queryset = Employee.objects.all
    serializer_class = EmployeeSerializer

    def post(self, request, format=None):
        serializer = EmployeeSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

class DetailEmployee(generics.UpdateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def get(self, request, pk, format=None):
        try:
            item = Employee.objects.filter(archived=False).get(pk=pk)
            serializer = EmployeeSerializer(item)
            return Response(serializer.data)
        except Employee.DoesNotExist:
            return Response({
                "status": "failure",
                "message": "no such item with this id",
                }, status=404)

    def put(self, request, pk,format=None):
        employee = Employee.objects.get(pk=pk)
        serializer = EmployeeSerializer(employee, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=200)

        return Response(serializer.errors, status=400)

    def delete(self, request, *args, **kwargs):
        try:
            employee = Employee.objects.filter(archived=False).get(id=kwargs["pk"])
        except Employee.DoesNotExist:
            return Response({
                "status": "failure",
                "message": "no such item with this id",
                }, status=404)
        employee.archived=True
        employee.save()
        return Response({"message": "deleted"},status=204)


