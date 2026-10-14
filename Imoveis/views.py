from django.shortcuts import render
from .serializers import ImovelSerializer
from .models import Imovel
from rest_framework import generics


class ImovelListCreateView(generics.ListCreateAPIView):
    queryset = Imovel.objects.all()
    serializer_class = ImovelSerializer


class ImovelRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Imovel.objects.all()
    serializer_class = ImovelSerializer


