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

table_dict = {
    "things":Entity,
    "accounts":Account,
    "attributes":Attribute,
    "adjustments":Adjustment
}



'''
VERY IMPORTANT HANDLE SPACES AND NEW LINES IN INPUT DATA
'''

@api_view(['POST'])
def importTables(request):
    
    scn_id = request.data["Scenario"]
    version = request.data["Version"]

    data = request.data["data"]
    scn = Scenario.objects.filter(scn_id=scn_id,version=version)[0]
    if "Things" in data.keys():
        importEntities(data["Things"],scn)
    if "Relationships" in data.keys():
        importRelationships(data["Relationships"],scn)
    # print(Entity.objects.filter(name = "Braun, King and Barrows"))
    if "Accounts" in data.keys():
        importAccounts(data["Accounts"],scn)
    if "Attributes" in data.keys():
        importAttributes(data["Attributes"],scn)
    if "Adjustments" in data.keys():
        importAdjustments(data["Adjustments"],scn)
    
    return Response(request.data,status=status.HTTP_201_CREATED)

def importEntities(table_data,scn):
    Entity.objects.filter(scenario=scn).all().delete()
    '''
    NOT CURRENTLY USING COUNTRY, ISO CURRENCYY CODE, ETC.
    '''
    for row in table_data:
        # print(row["Thing"],row["Type"])
        entity = Entity.objects.create(name=row["Thing"],entity_type=row["Type"],scenario=scn)
        entity.save()
def importRelationships(table_data,scn):
    Relationship.objects.filter(scenario=scn).all().delete()

    for row in table_data:
        print(row)
        try:
            parent = Entity.objects.filter(scenario=scn,name=row["Parent"].strip())[0]
        except:
            raise Exception(row["Parent"] + " is not a defined entity")
        try:
            child = Entity.objects.filter(scenario=scn,name=row["Child"].strip())[0]
        except:
            raise Exception(row["Child"] + " is not a defined entity")
        relationship = Relationship.objects.create(
            parent=parent,
            child=child,
            ownership_percentage=float(row["Ownership Percentage"]),
            scenario=scn
            )
        relationship.save()

'''
NOT CURRENTLY USING CURRENCY, ACCOUNT CLASS, DATA TYPE
'''
def importAccounts(table_data,scn):

    Account.objects.filter(scenario=scn,collection="TBFC").all().delete()
    for row in table_data:
        # print(row['Entity'])
        try:
            pd = Period.objects.filter(period=row["Period"].strip(),scenario=scn)[0]
        except:
            raise Exception(row["Period"] + " is not a defined period")
        try:
            entity = Entity.objects.filter(name = row["Entity"].strip())[0]
        except:
            raise Exception(row["Entity"] + " is not a defined entity")
       
        account = Account.objects.create(
            account_name = row["Account Name"],
            amount = float(row["Amount"]),
            period = pd,
            collection = row["Collection"],
            entity = entity,
            scenario = scn
        )
        account.save()

# ISSUE WITH THE DATE.
# STACK TRACE REQUIRED
def importAttributes(table_data,scn):
    Attribute.objects.filter(entity__scenario=scn).all().delete()
    for row in table_data:
        # date = datetime.strptime(row["AttributeStartDate"],"yyyy-mm-dd hh:mm:ss")
        print(row["AttributeStartDate"].split("T")[0])
        
        try:
            entity = Entity.objects.filter(name = row["Entity"].strip())[0]
        except:
            raise Exception(row["Entity"] + " is not a defined entity")
        endDate = None
        if "AttributeEndDate" in row.keys():
            endDate = int(row["AttributeEndDate"])

        attribute = Attribute.objects.create(
            attribute_name = row["AttributeName"],
            attribute_value = (row["AttributeValue"]),
            begin_date = row["AttributeStartDate"].split("T")[0],
            end_date = endDate,
            entity = entity,
        )
        attribute.save()
'''
NEED TO INCLUDE ADJUSTMENT COLLECTION
'''
def importAdjustments(table_data,scn):
    
    Adjustment.objects.filter(account__scenario=scn).all().delete()
    for row in table_data:
        print(row)
        try:
            entity = Entity.objects.filter(name = row["Entity"].strip())[0]
        except:
            raise Exception(row["Entity"] + " is not a defined entity")
        try:
            acc = Account.objects.filter(
                account_name=row["Account Name"].strip(),
                scenario=scn,
                entity=entity)[0]
        except:
            raise Exception(row["Account Name"] + " is not a defined account")

            
       
        adj = Adjustment.objects.create(
            account = acc,
            adj_type = row["Adjustment Type"],
           
            adj_class = row["Adjustment Class"],
            adj_percentage = row["Adjustment Percentage"],
            adj_amount = row["Adjustment Amount"]
        )
        adj.save()
        