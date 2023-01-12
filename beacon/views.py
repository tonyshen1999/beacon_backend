from django.shortcuts import render
from rest_framework import generics

from .models import Period,Scenario,Entity
from .serializers import PeriodSerializer,ScenarioSerializer,EntitySerializer

class PeriodListCreateAPIView(generics.ListCreateAPIView):
    queryset = Period.objects.all()
    serializer_class = PeriodSerializer

class PeriodDetailAPIView(generics.RetrieveAPIView):
    queryset = Period.objects.all()
    serializer_class = PeriodSerializer
    lookup_field = 'period'

class ScenarioDetailAPIView(generics.RetrieveAPIView):
    queryset = Scenario.objects.all()
    serializer_class = ScenarioSerializer
    lookup_field = 'pk'

class ScenarioListCreateAPIView(generics.ListCreateAPIView):
    queryset = Scenario.objects.all()
    serializer_class = ScenarioSerializer
class EntityListCreateAPIView(generics.ListCreateAPIView):
    queryset = Entity.objects.all()
    serializer_class = EntitySerializer
    lookup_field = 'pk'