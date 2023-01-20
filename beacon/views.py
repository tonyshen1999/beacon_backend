from django.shortcuts import render
from rest_framework import generics,viewsets

from .models import Period,Scenario,Entity,Attribute, Country, Currency, Account, Adjustment, Relationship
from .serializers import PeriodSerializer,ScenarioSerializer,EntitySerializer, AttributeSerializer, AccountSerializer,AdjustmentSerializer,RelationshipSerializer
from django_filters import rest_framework as filters
from django_filters import ModelChoiceFilter
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.http.response import JsonResponse
from rest_framework.response import Response
from rest_framework import status
text_filters = ['icontains','gt','gte','lt','lte','iexact']
date_filters = ['range','lt','lte','gt','gte']
float_filters = ['range','lt','lte','gt','gte','iexact']


'''
NON GENERIC TYPE VIEWS
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
            

        }
# @csrf_exempt
@api_view(['GET','POST'])
def scenariosAPI(request):
    if request.method == 'GET':
        if request.GET.get("scn_id") == None:
            scenarios = Scenario.objects.all()
            
        else:

            scenarios = Scenario.objects.filter(scn_id=request.GET.get("scn_id")).all()
        
        serializer = ScenarioSerializer(scenarios,many=True)
            
        return JsonResponse({"scenarios":serializer.data})

    if request.method == 'POST':
        
        serializer = ScenarioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST'])
def entityAPI(request):
    if request.method == 'GET':
        print(request.GET.get("scn_id"))
        print(request.GET.get("version"))
        scn = Scenario.objects.filter(scn_id=request.GET.get("scn_id"),version=request.GET.get("version"))[0]
        entities = Entity.objects.filter(scenario=scn).all()
        serializer = EntitySerializer(entities,many=True)
        
        return JsonResponse({"entities":serializer.data})
    if request.method == 'POST':
        
        serializer = EntitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET','POST'])
def periodAPI(request):
    print(request.method)
    if request.method == 'GET':
        print(request.data)
        scn = Scenario.objects.filter(scn_id=request.GET.get("scn_id"),version=request.GET.get("version"))[0]
        periods = Period.objects.filter(scenario=scn).all()
        serializer = PeriodSerializer(periods,many=True)
        
        return JsonResponse({"periods":serializer.data})
    if request.method == 'POST':
        print(request.data)
        scn = Scenario.objects.filter(scn_id=request.data["scn_id"],version=request.data["scn_version"])[0]
        data = {
            "period":request.data["period"],
            "begin_date":request.data["begin_date"].split("T")[0],
            "end_date":request.data["end_date"].split("T")[0],
            "scenario":scn.scn_id
        }
        serializer = PeriodSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','POST'])
def accountAPI(request):
    if request.method == 'GET':
        scn = Scenario.objects.filter(scn_id=request.GET.get("scn_id"),version=request.GET.get("version"))[0]

        accounts = Account.objects.filter(scenario=scn).all()
        serializer = AccountSerializer(accounts,many=True)
        
        return JsonResponse({"accounts":serializer.data})
    if request.method == 'POST':
        
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST'])
def adjustmentAPI(request):
    if request.method == 'GET':
        scn = Scenario.objects.filter(scn_id=request.GET.get("scn_id"),version=request.GET.get("version"))[0]
        
        adjustments = Adjustment.objects.filter(account__scenario=scn).all()
        serializer = AdjustmentSerializer(adjustments,many=True)
        
        return JsonResponse({"adjustments":serializer.data})
    if request.method == 'POST':
        
        serializer = AdjustmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET','POST'])
def attributeAPI(request):
    
    if request.method == 'GET':
       
        attributes = Attribute.objects.all()

        serializer = AttributeSerializer(attributes,many=True)
        # return JsonResponse(attributes, safe=False)

        return JsonResponse({"attributes":serializer.data})
    if request.method == 'POST':
        
        serializer = AttributeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST'])
def relationshipAPI(request):
    
    if request.method == 'GET':
        scn = Scenario.objects.filter(scn_id=request.GET.get("scn_id"),version=request.GET.get("version"))[0]
        relationships = Relationship.objects.filter(scenario_id=scn).all()
        serializer = RelationshipSerializer(relationships,many=True)
        
        return JsonResponse({"relationships":serializer.data})
    if request.method == 'POST':
        
        serializer = RelationshipSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

# class scenariosAPI(viewsets.ModelViewSet):
#     queryset = Scenario.objects.all()
#     serializer_class = ScenarioSerializer

#     def list(self,request,*args,**kwargs):
#         scenarios = Scenario.objects.all()
#         serlizer = ScenarioSerializer(Scenario,many=True)
#         return Response(serilizer.data)

'''
Period REST Views
'''

'''
TEST PERIOD VIEW
'''

class PeriodViewSet(viewsets.ModelViewSet):
    queryset = Period.objects.all()
    serializer_class = PeriodSerializer

    def list(self, request, *args, **kwargs):
        periods = Period.objects.all()
        serializer = PeriodSerializer
        return Response(serializer.data)

class PeriodFilter(filters.FilterSet):
    class Meta:
        model = Period
        fields = {
            'period':text_filters,
            'begin_date':date_filters,
            'begin_date':date_filters,
            'scenario':['lt','lte','gte','gt','exact'],

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



class ScenarioDetailAPIView(generics.RetrieveAPIView):
    queryset = Scenario.objects.all()
    serializer_class = ScenarioSerializer
    lookup_field = 'pk'

# # @csrf_exempt
# @api_view(['GET','POST'])
# def scenariosAPI(request):

#     scnearios = Scenario.objects.all()
    
#     serializer = ScenarioSerializer(scnearios,many=True)
    
#     scnearios_serializer = ScenarioSerializer
#     return JsonResponse({"scenarios":serializer.data})


class ScenarioListCreateAPIView(generics.ListCreateAPIView):
    queryset = Scenario.objects.all()
    serializer_class = ScenarioSerializer
    filterset_class = ScenarioFilter

'''
Entity REST Views
'''

# UPDATE FOR ABILITY TO FILTER BY FOREIGN KEY ATTRIBUTE
class EntityFilter(filters.FilterSet):
    period = ModelChoiceFilter(queryset=Period.objects.all())
    scenario = ModelChoiceFilter(queryset=Scenario.objects.all())
    class Meta:
        model = Entity

        fields = {
            'name':text_filters,
            'entity_type':text_filters,
            # 'scenario':['iexact'],
            # 'country':text_filters,
            # 'periods':['iexact']

        }

class EntityListCreateAPIView(generics.ListCreateAPIView):
    queryset = Entity.objects.all()
    serializer_class = EntitySerializer
    filterset_class = EntityFilter

class EntityDetailAPIView(generics.RetrieveAPIView):
    queryset = Entity.objects.all()
    serializer_class = EntitySerializer
    lookup_field = 'pk'

'''
Attribute REST Views
'''

class AttributeFilter(filters.FilterSet):
    scenario = ModelChoiceFilter(queryset=Scenario.objects.all())
    class Meta:
        model = Attribute

        fields = {
            'attribute_name':text_filters,
            'attribute_value':text_filters,
            'begin_date':date_filters,
            'end_date':date_filters,


        }

class AttributeListCreateAPIView(generics.ListCreateAPIView):
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializer
    filterset_class = AttributeFilter

class AttributeDetailAPIView(generics.RetrieveAPIView):
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializer
    lookup_field = 'pk'

'''
Acccount REST Views
'''

class AccountFilter(filters.FilterSet):
    scenario = ModelChoiceFilter(queryset=Scenario.objects.all())
    period = ModelChoiceFilter(queryset=Period.objects.all())
    currency = ModelChoiceFilter(queryset=Currency.objects.all())
    entity  = ModelChoiceFilter(queryset=Entity.objects.all())
    class Meta:
        model = Account

        fields = {
            'account_name':text_filters,
            'amount':text_filters,
            'collection':text_filters,
            'acc_class':text_filters,
            'data_type':float_filters
        }

class AccountListCreateAPIView(generics.ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    filterset_class = AccountFilter

class AccountDetailAPIView(generics.RetrieveAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    lookup_field = 'pk'

'''
Adjustment REST Views
'''

class AdjustmentFilter(filters.FilterSet):
    account = ModelChoiceFilter(queryset=Account.objects.all())
    
    class Meta:
        model = Adjustment

        fields = {
            'adj_type':text_filters,
            'adj_collection':text_filters,
            'adj_class':text_filters,
            'adj_percentage':float_filters,
            'adj_amount':float_filters
        }

class AdjustmentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Adjustment.objects.all()
    serializer_class = AdjustmentSerializer
    filterset_class = AdjustmentFilter

class AdjustmentDetailAPIView(generics.RetrieveAPIView):
    queryset = Adjustment.objects.all()
    serializer_class = AdjustmentSerializer
    lookup_field = 'pk'

