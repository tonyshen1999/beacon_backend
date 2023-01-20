from django.shortcuts import render
from rest_framework import generics

from .models import Period,Scenario,Entity,Attribute, Country, Currency, Account, Adjustment
from .serializers import PeriodSerializer,ScenarioSerializer,EntitySerializer, AttributeSerializer, AccountSerializer,AdjustmentSerializer
from django_filters import rest_framework as filters
from django_filters import ModelChoiceFilter
from TestModel import TestModel
from rest_framework.decorators import api_view


@api_view(['POST'])
def calculate(request):
    
    t = TestModel(2,1)
    p = Period.objects.get(period="CYE2018")
    s = Scenario.objects.get(name="Test")
    e = Entity.objects.get(name="USSH 1")
    a = Account(account_name="test",amount = t.calc(),period = p,scenario=s,entity=e)
    a.save()

