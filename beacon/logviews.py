from django.shortcuts import render
from rest_framework import generics,viewsets

from .models import Period,Scenario,Entity,Attribute, Country, Currency, Account, Adjustment, Relationship, Calculation
from .logmodel import Log, ImportLog
from .serializers import PeriodSerializer,ScenarioSerializer,EntitySerializer, AttributeSerializer, AccountSerializer,AdjustmentSerializer,RelationshipSerializer, LogSerializer, ImportLogSerializer
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

@api_view(['GET'])
def calcLogListAPI(request):

    scn_id = request.GET.get("scn_id")
    scn_version = request.GET.get("scn_version")
    scn = Scenario.objects.get(scn_id=scn_id,version=scn_version)



    calc_logs = Calculation.objects.filter(scenario = scn).all()
    data = {}

    for c in calc_logs:
        return_data = {
            "Success":  LogSerializer(Log.objects.filter(calculation=c,status=0).all(),many=True).data,
            "Message":  LogSerializer(Log.objects.filter(calculation=c,status=1).all(),many=True).data,
            "Errors":  LogSerializer(Log.objects.filter(calculation=c,status=2).all(),many=True).data,
         }
        data[str(c.date_time)] = return_data#LogSerializer(Log.objects.filter(calculation=c).all(),many=True).data
    


    return JsonResponse(data)

@api_view(['GET'])
def importLogAPI(request):
    return_data = {
        "Success": ImportLogSerializer(ImportLog.objects.filter(status=0),many=True).data,
        "Message": ImportLogSerializer(ImportLog.objects.filter(status=1),many=True).data,
        "Errors": ImportLogSerializer(ImportLog.objects.filter(status=2),many=True).data,
    }
    return JsonResponse(return_data)
        