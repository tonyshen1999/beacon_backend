from django.shortcuts import render
from rest_framework import generics

from .models import Period,Scenario,Entity,Attribute, Country, Currency, Account, Adjustment
from .serializers import PeriodSerializer,ScenarioSerializer,EntitySerializer, AttributeSerializer, AccountSerializer,AdjustmentSerializer
from django_filters import rest_framework as filters
from django_filters import ModelChoiceFilter

text_filters = ['icontains','gt','gte','lt','lte','iexact']
date_filters = ['range','lt','lte','gt','gte']
float_filters = ['range','lt','lte','gt','gte','iexact']

'''
Period REST Views
'''

class PeriodFilter(filters.FilterSet):
    class Meta:
        model = Period
        fields = {
            'period':text_filters,
            'begin_date':date_filters,
            'begin_date':date_filters,

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

class ScenarioFilter(filters.FilterSet):
    periods = ModelChoiceFilter(queryset=Period.objects.all())
    class Meta:
        model = Scenario

        fields = {
            'scn_id':float_filters,
            'name':text_filters,
            'description':text_filters,
            'version':float_filters,
            'periods':['iexact']

        }

class ScenarioDetailAPIView(generics.RetrieveAPIView):
    queryset = Scenario.objects.all()
    serializer_class = ScenarioSerializer
    lookup_field = 'pk'

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

