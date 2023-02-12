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
    print(data)
    current = Scenario.objects.filter(scn_id=data["scn_id"]).order_by('-version')[0]
    new_scenario = copy.deepcopy(current)
    new_scenario.pk = None
    new_scenario.version = current.version+1
    new_scenario.description = data["description"]
    new_scenario.save()
    accounts = Account.objects.filter(scenario=current)

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
    # create a private function to stop repetition
    entities = Entity.objects.filter(scenario=current)
    for e in entities:
        atrs = Attribute.objects.filter(entity=e).all()
        entity_accounts = accounts.filter(entity=e)
        relationship_parent = Relationship.objects.filter(parent=e)



        relationship_child = Relationship.objects.filter(child=e)


        e.pk = None
        e.scenario = new_scenario
        e.save()
        if relationship_parent.count() > 0:
            relationship_parent[0].parent = e
        if relationship_child.count() > 0:
            relationship_child[0].child = e
        # print(e)
        for atr in atrs:
            atr.pk = None
            atr.entity = e
            atr.save()

        

        for a in entity_accounts:
            adjustments = Adjustment.objects.filter(account = a)
            old_period = a.period
            new_period = Period.objects.get(period=old_period.period,scenario=new_scenario)
            a.pk = None
            a.entity = e
            a.scenario = new_scenario
            a.period=new_period
            a.save()
            # print(a.entity)
            for adj in adjustments:
                adj.pk = None
                adj.account = a
                adj.save()


    


    return Response(status=status.HTTP_201_CREATED)