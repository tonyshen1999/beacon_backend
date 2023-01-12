from django.shortcuts import render
from rest_framework import generics

from .models import Period,Scenario,Entity,Attribute
from .serializers import PeriodSerializer,ScenarioSerializer,EntitySerializer, AttributeSerializer

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


class EntityDetailAPIView(generics.RetrieveAPIView):
    queryset = Entity.objects.all()
    serializer_class = EntitySerializer
    lookup_field = 'pk'

class AttributeListCreateAPIView(generics.ListCreateAPIView):
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializer


class AttributeDetailAPIView(generics.RetrieveAPIView):
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializer
    lookup_field = 'pk'