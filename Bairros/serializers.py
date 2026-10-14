from .models import Bairro
from rest_framework import serializers


class BairroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bairro
        fields = '__all__'