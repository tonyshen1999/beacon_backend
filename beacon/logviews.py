from django.shortcuts import render
from rest_framework import generics,viewsets

from .models import Period,Scenario,Entity,Attribute, Country, Currency, Account, Adjustment, Relationship
from .logmodel import Log
from .serializers import PeriodSerializer,ScenarioSerializer,EntitySerializer, AttributeSerializer, AccountSerializer,AdjustmentSerializer,RelationshipSerializer, LogSerializer
from django_filters import rest_framework as filters
from django_filters import ModelChoiceFilter
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.http.response import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Max

@api_view(['GET'])
def logAPI(request):
    '''
    request: {
        scn_id
        scn_version
        period
        entity
    }
    '''
    scn_id = request.GET.get("scn_id")

    scn_version = request.GET.get("scn_version")
    period_name = request.GET.get("period")
    entity_name = request.GET.get("entity")

    # print(scn_id,scn_version,period_name,entity_name)

    scn = Scenario.objects.get(scn_id=scn_id,version=scn_version)
    pd = Period.objects.get(period=period_name,scenario=scn)
    entity = Entity.objects.get(name=entity_name,scenario=scn)

    logs = Log.objects.filter(account__entity = entity, account__period = pd).all()
    
    serializer = LogSerializer(logs,many=True)

    return JsonResponse({"logs":serializer.data})
