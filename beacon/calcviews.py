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
from .entitycalc import EntityCalc, CFCCalc, USSHCalc

@api_view(['POST'])
def calculate(request):

    '''
    Request -> 

    data ={
        "scn_id":1,
        "scn_version": 1,
        "entities": [{"entity_name":"Ferry Group","pd_name": "CYE2022",}]
    }

}
    '''
    data = request.data

    e_list = extract_data(request)
    
    for e in e_list:
        e.calculate()


    return Response(status=status.HTTP_201_CREATED)


@api_view(['POST'])
def clear_db(request):
    Scenario.objects.all().delete()


@api_view(['POST'])
def clear_calc(request):
    print("234234234234",request.data)
    e_list = extract_data(request)
    for e in e_list:
        e.clear_calc()
    return Response(status=status.HTTP_202_ACCEPTED)

@api_view(['POST'])
def clear_data(request):
    print("234234234234234234234234",request.data)
    e_list = extract_data(request)
    for e in e_list:
        e.clear_data()

    return Response(status=status.HTTP_202_ACCEPTED)

@api_view(['POST'])
def clear_scenario(request):

    data = request.data
    scn_id = data["scn_id"]
    version = data["scn_version"]

    scn = Scenario.objects.get(
        scn_id = data["scn_id"],
        version = data["scn_version"]
    )[0]
    name = scn.name

    scn.delete()
    scn_new = Scenario(
        scn_id = scn_id,
        name = name,
        version = 1,
    )
    scn_new.save()

def extract_data(request):

    data = request.data
    scn_id = data["scn_id"]
    version = data["scn_version"]

    scn = Scenario.objects.filter(
        scn_id = data["scn_id"],
        version = data["scn_version"]
    )[0]
  
      
    relationships = Relationship.objects.filter(scenario = scn)
    entity_list = []
    if "entities" in data:
        for x in data["entities"]:

            entity = Entity.objects.filter(
                name = x["entity_name"],
                scenario = scn
            )[0]

            period = Period.objects.filter(
                period = x["pd_name"],
                scenario = scn
            )[0]

            # e is type CFC Calc
            
            e = create_entity_calc(entity,period)
            
            children_rel = relationships.filter(parent=entity)
            if children_rel.count() > 0:
                for r in children_rel:
                    c = create_entity_calc(r.child,period)
                    e.set_child(child=c,percent_owned=r.ownership_percentage)
                    if c not in entity_list:
                        entity_list.append(c)

            entity_list.append(e)
    elif "pd" in data:
        pd = Period.objects.get(scenario=scn,period=data["pd"])
        all_entities = Entity.objects.filter(scenario=scn)
        for x in all_entities:
            e = create_entity_calc(x,pd)
            entity_list.append(e)
    else:
        pass
        # exception handling
    return entity_list

def create_entity_calc(entity, period):
    if entity.entity_type == "CFC":
        e = CFCCalc(entity,period)
    elif entity.entity_type == "USSH":
        e = USSHCalc(entity,period)
    else:
        e = EntityCalc(entity,period)
    
    return e

        
    

