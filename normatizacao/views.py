from django.shortcuts import render
from rest_framework import generics
from .models import Normatizador
from .serializers import NormatizadorSerializer

class NormatizadorList(generics.ListCreateAPIView):
    queryset = Normatizador.objects.all()
    serializer_class = NormatizadorSerializer

