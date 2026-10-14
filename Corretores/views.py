from django.shortcuts import render
from .serializers import CorretorSerializer
from .models import Corretor
from rest_framework import generics


class CorretorListCreateView(generics.ListCreateAPIView):
    queryset = Corretor.objects.all()
    serializer_class = CorretorSerializer


class CorretorRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Corretor.objects.all()
    serializer_class = CorretorSerializer


