__author__ = 'Lawrence'
from mobidevlending.modules.ussd.models import Users
from rest_framework import serializers

class UssdUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Users
        fields = ('name', 'phone', 'gender', 'email')
