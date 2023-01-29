from django.shortcuts import render
from rest_framework import generics

from .models import Period,Scenario,Entity,Attribute, Country, Currency, Account, Adjustment, Relationship
from .serializers import PeriodSerializer,ScenarioSerializer,EntitySerializer, AttributeSerializer, AccountSerializer,AdjustmentSerializer, RelationshipSerializer
from django_filters import rest_framework as filters
from django_filters import ModelChoiceFilter
from TestModel import TestModel
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import json
from .models import Scenario,Entity,Account,Attribute,Adjustment,Period
from datetime import datetime
import copy



@api_view(['POST'])
def new_version(request):

    ''' Duplicate a scenario and increment the version.
    '''
    data = request.data
    current = Scenario.objects.filter(scn_id=data["scn_id"]).order_by('-version')[0]
    new_scenario = copy.deepcopy(current)
    new_scenario.pk=None
    new_scenario.version = current.version+1
    new_scenario.save()

    # create a private function to stop repetition
    entities = Entity.objects.filter(scenario=current)
    for e in entities:
        e.pk = None
        e.scenario = new_scenario
        e.save()
    accounts = Account.objects.filter(scenario=current)
    for a in accounts:
        adjustments = Adjustment.objects.filter(account = a)

        a.pk = None
        a.scenario = new_scenario
        a.save()
        for adj in adjustments:
            adj.pk = None
            adj.account = a
            adj.save()


    
    periods = Period.objects.filter(scenario=current)
    for p in periods:
        p.pk = None
        p.scenario = new_scenario
        p.save()

    relationships = Relationship.objects.filter(scenario=current)
    for r in relationships:
        r.pk = None
        r.scenario = new_scenario
        r.save()
    

    return Response(status=status.HTTP_201_CREATED)