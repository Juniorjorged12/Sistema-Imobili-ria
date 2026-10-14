from .models import Corretor
from rest_framework import serializers


class CorretorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Corretor
        fields = '__all__'