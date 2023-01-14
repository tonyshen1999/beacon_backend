from django.shortcuts import render
from rest_framework import generics

from .models import Period,Scenario,Entity,Attribute
from .serializers import PeriodSerializer,ScenarioSerializer,EntitySerializer, AttributeSerializer
from django_filters import rest_framework as filters
from django_filters import ModelChoiceFilter

text_filters = ['icontains','gt','gte','lt','lte','iexact']
date_filters = ['range','lt','lte','gt','gte']
float_filters = ['range','lt','lte','gt','gte','iexact']

'''
Period REST Views
'''

class PeriodFilter(filters.FilterSet):
    class Meta:
        model = Period
        fields = {
            'period':text_filters,
            'begin_date':date_filters,
            'begin_date':date_filters,

        }

class PeriodListCreateAPIView(generics.ListCreateAPIView):
    queryset = Period.objects.all()
    serializer_class = PeriodSerializer
    filterset_class = PeriodFilter


class PeriodDetailAPIView(generics.RetrieveAPIView):
    queryset = Period.objects.all()
    serializer_class = PeriodSerializer
    lookup_field = 'period'

'''
Scenario REST Views
'''

class ScenarioFilter(filters.FilterSet):
    periods = ModelChoiceFilter(queryset=Period.objects.all())
    class Meta:
        model = Scenario

        fields = {
            'scn_id':float_filters,
            'name':text_filters,
            'description':text_filters,
            'version':float_filters,
            'periods':['iexact']

        }

class ScenarioDetailAPIView(generics.RetrieveAPIView):
    queryset = Scenario.objects.all()
    serializer_class = ScenarioSerializer
    lookup_field = 'pk'

class ScenarioListCreateAPIView(generics.ListCreateAPIView):
    queryset = Scenario.objects.all()
    serializer_class = ScenarioSerializer
    filterset_class = ScenarioFilter

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