from django.shortcuts import render
from mobidevlending.modules.ussd.models import Users
from rest_framework import viewsets
from serializers import UssdUserSerializer


class UssdUserViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all().order_by('-created_date')
    serializer_class = UssdUserSerializer

