from django.shortcuts import render
from .serializers import CidadeSerializer
from .models import Cidade
from rest_framework import generics


class CidadeListCreateView(generics.ListCreateAPIView):
    queryset = Cidade.objects.all()
    serializer_class = CidadeSerializer


class CidadeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cidade.objects.all()
    serializer_class = CidadeSerializer
