from django.shortcuts import render
from rest_framework import generics

from .models import Period,Scenario,Entity,Attribute, Country, Currency, Account, Adjustment, Relationship, Calculation, CalcAction
from .serializers import PeriodSerializer,ScenarioSerializer,EntitySerializer, AttributeSerializer, AccountSerializer,AdjustmentSerializer, RelationshipSerializer, LogSerializer, CalcActionSerializer
from django_filters import rest_framework as filters
from django_filters import ModelChoiceFilter
from TestModel import TestModel
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .entitycalc import EntityCalc, CFCCalc, USSHCalc
from .logmodel import Log


'''
Create a function for pulling scenario lol
'''


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
    scn_id = data["scn_id"]
    version = data["scn_version"]
    # print(data)
    scn = Scenario.objects.filter(
        scn_id = data["scn_id"],
        version = data["scn_version"]
    )[0]
    print(scn)
    data = request.data
    calc_model = Calculation(scenario=scn,pk = None)
    calc_model.save()

    e_list = extract_data(request,calc_model)
    
    for e in e_list:
        e.calculate()

    return_data = {
        "Success": LogSerializer(Log.objects.filter(status=0,calculation=calc_model),many=True).data,
        "Message": LogSerializer(Log.objects.filter(status=1,calculation=calc_model),many=True).data,
        "Errors": LogSerializer(Log.objects.filter(status=2,calculation=calc_model),many=True).data,
    }

    # print(return_data)


    return Response(return_data,status=status.HTTP_201_CREATED)

# To sort by child and parent
@api_view(['GET'])
def calc_script(request):
    CalcAction.objects.all().delete()
    

    scn_id = request.GET.get("scn_id")
    version = request.GET.get("version")
    # print(data)
    scn = Scenario.objects.filter(
        scn_id = scn_id,
        version = version
    )[0]

    periods = Period.objects.filter(scenario=scn).all()
    print(periods)

    for p in periods:
        rels = Relationship.objects.filter(scenario=scn).all()
        children = set()
        parents = set()
        for e in rels:
            children.add(e.child)
            parents.add(e.parent)
        
        children = list(children)
        children.extend(list(parents))

        for c in children:
            ca = CalcAction(
                entity = c,
                period = p,
                action = get_entity_action(c)
                )

            ca.save()
    return Response({"calc_script":CalcActionSerializer(CalcAction.objects.all(),many=True).data})

def get_entity_action(entity):

    if entity.entity_type == "USSH":
        return "USSH951A"
    elif entity.entity_type == "CFC":
        return "Tested Income and EP"
    elif entity.entity_type == "DRE":
        return "EP"
    else:
        return ""



@api_view(['POST'])
def clear_db(request):
    Scenario.objects.all().delete()
    


@api_view(['POST'])
def clear_calc(request):

    data = request.data
    scn_id = data["scn_id"]
    version = data["scn_version"]

    scn = Scenario.objects.filter(
        scn_id = data["scn_id"],
        version = data["scn_version"]
    )[0]

    accounts = Account.objects.filter(entity__scenario = scn)
    accounts.exclude(collection="TBFC").delete()


    return Response(status=status.HTTP_202_ACCEPTED)

@api_view(['POST'])
def clear_data(request):
    
    data = request.data
    scn_id = data["scn_id"]
    version = data["scn_version"]

    scn = Scenario.objects.filter(
        scn_id = data["scn_id"],
        version = data["scn_version"]
    )[0]

    accounts = Account.objects.filter(entity__scenario = scn)
    accounts.delete()


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

def extract_data(request, calc_model):


    data = request.data
    # scn_id = data["scn_id"]
    # version = data["scn_version"]

    # scn = Scenario.objects.filter(
    #     scn_id = data["scn_id"],
    #     version = data["scn_version"]
    # )[0]
    scn = calc_model.scenario


      
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
            accounts = Account.objects.filter(entity=entity)
            # print(accounts)
            
            e = create_entity_calc(entity,period, calc_model)
            # print(e)
            children_rel = relationships.filter(parent=entity)
            if children_rel.count() > 0:
                print("--------------\n THIS MEANS THERE ARE CHILDREN")
                for r in children_rel:
                    c = create_entity_calc(r.child,period, calc_model)
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

def create_entity_calc(entity, period, calc_model=None):
    if entity.entity_type == "CFC":
        e = CFCCalc(entity,period, calc_model)
    elif entity.entity_type == "USSH":
        e = USSHCalc(entity,period, calc_model)
    else:
        e = EntityCalc(entity,period, calc_model)
    
    return e

        
    

