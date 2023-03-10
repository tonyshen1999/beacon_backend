from django.shortcuts import render
from rest_framework import generics

from .models import Period,Scenario,Entity,Attribute, Country, Currency, Account, Adjustment, Relationship, DefaultAttribute
from .serializers import PeriodSerializer,ScenarioSerializer,EntitySerializer, AttributeSerializer, AccountSerializer,AdjustmentSerializer, RelationshipSerializer, ImportLogSerializer, DefaultAttributeSerializer
from django_filters import rest_framework as filters
from django_filters import ModelChoiceFilter
from TestModel import TestModel
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import json
from .models import Scenario,Entity,Account,Attribute,Adjustment,Period
from datetime import datetime
from .logmodel import ImportLog

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
    push_atr = request.data["PushAttributes"]
    


    ImportLog.objects.all().delete()
    data = request.data["data"]
    print("data keys:", data.keys())
    scn = Scenario.objects.filter(scn_id=scn_id,version=version)[0]
    # scn.modify_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    scn.save()

    if "Things" in data.keys():
        importEntities(data["Things"],scn)

    if "Relationships" in data.keys():
        importRelationships(data["Relationships"],scn)

    if "Accounts" in data.keys():
        importAccounts(data["Accounts"],scn)

    if "Attributes" in data.keys():
        importAttributes(data["Attributes"],scn)

    elif push_atr:
        atr_set = DefaultAttribute.objects.filter(scenario = "Default").all()
        pushDefaultAttributes(scn,atr_set)

    if "Adjustments" in data.keys():
        importAdjustments(data["Adjustments"],scn)

    return_data = {
        "Success": ImportLogSerializer(ImportLog.objects.filter(status=0),many=True).data,
        "Message": ImportLogSerializer(ImportLog.objects.filter(status=1),many=True).data,
        "Errors": ImportLogSerializer(ImportLog.objects.filter(status=2),many=True).data,
    }

    return Response(return_data,status=status.HTTP_201_CREATED)

def get_row(row,item):
    if item in row.keys():
        return row[item]
    return "[Blank]"

def importEntities(table_data,scn):
    Entity.objects.filter(scenario=scn).all().delete()
    '''
    NOT CURRENTLY USING COUNTRY, ISO CURRENCYY CODE, ETC.
    '''
    
    for row in table_data:
        entity_type = get_row(row,"Type")
        if entity_type == "[Blank]":
            entity_type == None
        data = {
            "name":get_row(row,"Thing"),
            "entity_type":entity_type,
            "scenario":scn.pk
        }
       
        # print(data)
        serializer = EntitySerializer(data=data)
        if serializer.is_valid():

            success_log = ImportLog(
                log_type = "Entity",
                name = row["Thing"],
                status = 0,
                scenario = scn
            )
            print(scn)
            print(data)
            success_log.save()
            serializer.save()
            # return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            
            error_log = ImportLog(
                log_type = "Entity",
                name = get_row(row,"Thing"),
                status = 2,
                scenario = scn,
                message = serializer.errors
            )
            error_log.save()
            # return Response(status=status.HTTP_400_BAD_REQUEST)
        # entity = Entity.objects.create(name=row["Thing"],entity_type=row["Type"],scenario=scn)
        # entity.save()

def importRelationships(table_data,scn):
    Relationship.objects.filter(scenario=scn).all().delete()

    for row in table_data:
        
        valid = True
        # print(row)
        try:
            parent = Entity.objects.filter(scenario=scn,name=get_row(row,"Parent").strip())[0]
        except:
            valid = False
            parent_row = get_row(row,"Parent")
            log = ImportLog(
                log_type = "Entity",
                name = parent_row,
                status = 2,
                scenario = scn,
                message = parent_row + " is not a defined entity for 'Parent' in Relationships Table"
            )
            log.save()
            # raise Exception(get_row(row,"Parent") + " is not a defined entity")
        try:
            child = Entity.objects.filter(scenario=scn,name=get_row(row,"Child").strip())[0]
            # print(child)
        except:
            valid = False
            child_row = get_row(row,"Child")

            log = ImportLog(
                log_type = "Entity",
                name = child_row,
                status = 2,
                scenario = scn,
                message = child_row + " is not a defined entity for 'Child' in Relationships Table"
            )
            log.save()



        own_row = get_row(row,"Ownership Percentage")
        
        try:
            own_row = float(own_row)
        except:
            valid = False
            log = ImportLog(
                log_type = "Relationship Ownership Percentage",
                name = str(own_row),
                status = 2,
                scenario = scn,
                message = str(own_row) + " must be a float type (format as decimal and NOT Percentage)"
            )
            log.save()

        if valid:
            relationship = Relationship.objects.create(
                parent=parent,
                child=child,
                ownership_percentage=float(row["Ownership Percentage"]),
                scenario=scn
            )
            success_log = ImportLog(
                log_type = "Relationships",
                name = "Parent:" + get_row(row,"Parent") + ", Child: " + get_row(row,"Child"),
                status = 0,
                scenario = scn,
            )
            success_log.save()
            relationship.save()

'''
NOT CURRENTLY USING CURRENCY, ACCOUNT CLASS, DATA TYPE
'''
def importAccounts(table_data,scn):

    print("importing accounts...")
    Account.objects.filter(scenario=scn).all().delete()
    for row in table_data:
        
        try:
            pd_pk = Period.objects.filter(period=get_row(row,"Period").strip(),scenario=scn)[0].pk
        except:

            
            if get_row(row,"Period") is not None and ("FYE" in get_row(row,"Period") or "CYE" in get_row(row,"Period")):
                pd_pk = Period.objects.filter(scenario=scn)[0].new_period(period=get_row(row,"Period")).pk
                message_log = ImportLog(
                    log_type = "Period in Accounts Table",
                    name = get_row(row,"Period"),
                    status = 1,
                    scenario = scn,
                    message = get_row(row,"Period") + " was not a defined period, so a new period was created. (This could be due\
                        to finding a PY Carryforward, which won't impact period being calculated)"
                )
                message_log.save()

            else:
                pd_row = get_row(row,"Period")

                error_log = ImportLog(
                    log_type = "Period in Accounts Table",
                    name = pd_row,
                    status = 2,
                    scenario = scn,
                    message = "Invaid Period Definition"
                )

                error_log.save()
                pd_pk = get_row(row,"Period")
            
            # raise Exception(row["Period"] + " is not a defined period") #this is still allowed. We would just create a new period
        try:
            entity_pk = Entity.objects.filter(name = get_row(row,"Entity").strip(), scenario=scn)[0].pk
            
        except:
            entity_pk = get_row(row,"Entity")
        try:
            amt = float(get_row(row,"Amount"))
        except:
            amt = get_row(row,"Amount")
        data = {
            "account_name":get_row(row,"Account Name"),
            "amount": amt,
            "period": pd_pk,
            "collection": get_row(row,"Collection"),
            "entity" : entity_pk,
            "scenario" : scn.pk
        }

        serializer = AccountSerializer(data=data)
        if serializer.is_valid():

            success_log = ImportLog(
                log_type = "Account",
                name = get_row(row,"Account Name") + " for entity " + get_row(row,"Entity"),
                status = 0,
                scenario = scn
            )
            success_log.save()
            serializer.save()
        else :
            acct_name = get_row(row,"Account Name")

            error_log = ImportLog(
                log_type = "Account",
                name = acct_name,
                status = 2,
                scenario = scn,
                message = serializer.errors
            )
            error_log.save()
        # account = Account.objects.create(
        #     account_name = row["Account Name"],
        #     amount = float(row["Amount"]),
        #     period = pd,
        #     collection = row["Collection"],
        #     entity = entity,
        #     scenario = scn
        # )
        # account.save()

def pushDefaultAttributes(scenario,atr_set):

    entities = Entity.objects.filter(scenario = scenario).all()

    for e in entities:

        if Attribute.objects.filter(entity=e).count() > 0:
            Attribute.objects.filter(entity=e).delete()

        def_atr = atr_set.filter(entity_type = "All").all()
        for d_a in def_atr:
            atr = d_a.pull_attribute()
            atr.entity = e
            atr.save()

        e_type = e.entity_type
        specific_atr = atr_set.filter(entity_type = e_type).all()

        for d_a in specific_atr:
            atr = d_a.pull_attribute()
            atr.entity = e
            atr.save()

@api_view(['POST'])
def customAttributes(request):

    data = request.data
    scn = Scenario.objects.get(scn_id=data["scn_id"],version=data["scn_version"])

    atrs = data["attributes"]
    DefaultAttribute.objects.all().delete()
    # print(atrs)
    for a in atrs:
        print(a)
        da = DefaultAttribute(
            entity_type = a['entity_type'],
            attribute_name = a['attribute_name'],
            attribute_value = a['attribute_value'],
            scenario = 'Default',
            begin_date = a['begin_date'],
            end_date = a['end_date']
        )
        da.save()
    
    atr_set = DefaultAttribute.objects.filter(scenario='Default')

    pushDefaultAttributes(scn,atr_set)

    return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
def attributeScenarioTypes(request):

    type_set = set()

    def_atr = DefaultAttribute.objects.all()

    for da in def_atr:
        type_set.add(da.scenario)
    
    type_set = list(type_set)
    print(type_set)

    data = {
        "types":[]
    }
    
    for t in type_set:
        data["types"].append({"type":t})

    return Response(data=data,status=status.HTTP_200_OK)

@api_view(['GET'])
def filterAttributes(request):


    print(request.GET.get("scn_id"),request.GET.get("version"))

    scn = Scenario.objects.get(
        scn_id = request.GET.get("scn_id"),
        version = request.GET.get("version")
    )

    type_filter = request.GET.get("scenario")

    if type_filter is None or type_filter == "":
        return Response(data=DefaultAttributeSerializer(DefaultAttribute.objects.filter(
            scenario="Default"
        ).all(),many=True).data,status=status.HTTP_200_OK)

    # print(type_filter)
    # print(len(DefaultAttribute.objects.all()))

    def_atr_unique = DefaultAttribute.objects.filter(scenario = type_filter)
    # print(def_atr_unique)
    def_atr_all = DefaultAttribute.objects.filter(scenario="Default").exclude(
        attribute_name = def_atr_unique[0].attribute_name).union(def_atr_unique)
    
        
    # print(len(def_atr_all))
    serializer = DefaultAttributeSerializer(def_atr_all,many=True)

    return Response(data=serializer.data,status=status.HTTP_200_OK)


def importAttributes(table_data,scn):
    Attribute.objects.filter(entity__scenario=scn).all().delete()
    for row in table_data:
        # date = datetime.strptime(row["AttributeStartDate"],"yyyy-mm-dd hh:mm:ss")
        # print(row["AttributeStartDate"].split("T")[0])
        
        try:
            entity = Entity.objects.filter(name = row["Entity"].strip(),scenario=scn)[0]
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
        valid = True
        # print(row)
        acc_name = get_row(row,"Account Name")
        entity_name = get_row(row,"Entity")
        adj_type = get_row(row,"Adjustment Type")
        adj_class = get_row(row,"Adjustment Class")
        try:
            entity = Entity.objects.filter(name = entity_name.strip(),scenario=scn)[0]
        except Exception as e:
            error_log = ImportLog(
                log_type = "Adjustment",
                name = "<" + adj_type + "> type adjustment for  " + acc_name + " account, entity <" + entity_name +">",
                status = 2,
                scenario = scn,
                message = str(e)
            )
            valid = False
            error_log.save()
        try:
            acc = Account.objects.filter(
                account_name=acc_name.strip(),
                scenario=scn,
                entity=entity)[0]
        except Exception as e:
            error_log = ImportLog(
                log_type = "Adjustment",
                name = "<" + adj_type + "> type adjustment for  " + acc_name + " account",
                status = 2,
                scenario = scn,
                message = str(e)
            )
            valid = False
            error_log.save()


        try:
            adj_percentage = float(get_row(row,"Adjustment Percentage"))
            adj_amount = float(get_row(row,"Adjustment Amount"))
        except Exception as e:
            error_log = ImportLog(
                log_type = "Adjustment",
                name = adj_type + " type adjustment for  " + acc_name + " account",
                status = 2,
                scenario = scn,
                message = str(e)
            )
            valid = False
            error_log.save()
        # data = {
        #     "account_id":acc.pk,
        #     "adj_type": adj_type,
        #     "adj_class": adj_class,
        #     "adj_percentage": adj_percentage,
        #     "adj_amount": adj_amount
        # }
        # print(data)
        # serializer = AdjustmentSerializer(data=data)
        # if serializer.is_valid():

        #     success_log = ImportLog(
        #         log_type = "Adjustment",
        #         name = "<" + adj_type + "> type adjustment for  " + acc_name + " account, " + "<" + entity_name + ">",
        #         status = 0,
        #         scenario = scn
        #     )
        #     success_log.save()
        #     serializer.save()
        # else :

        #     error_log = ImportLog(
        #         log_type = "Adjustment",
        #         name = "<" + adj_type + "> type adjustment for  " + acc_name + " account",
        #         status = 2,
        #         scenario = scn,
        #         message = serializer.errors
        #     )
        #     error_log.save()
        if valid:
            adj = Adjustment.objects.create(
                account = acc,
                adj_type = adj_type,
                adj_class = adj_class,
                adj_percentage = adj_percentage,
                adj_amount = adj_amount
            )
            success_log = ImportLog(
                log_type = "Adjustment",
                name = adj_type + " type adjustment for  " + acc_name + " account, " + "[" + entity_name + "]",
                status = 0,
                scenario = scn
            )
            success_log.save()

            adj.save()
        