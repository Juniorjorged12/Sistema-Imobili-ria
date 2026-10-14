from django.shortcuts import render
from .serializers import BairroSerializer
from .models import Bairro
from rest_framework import generics


class BairroListCreateView(generics.ListCreateAPIView):
    queryset = Bairro.objects.all()
    serializer_class = BairroSerializer


class BairroRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bairro.objects.all()
    serializer_class = BairroSerializer


