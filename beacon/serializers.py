from rest_framework import serializers
from .models import Period,Scenario,Entity, Attribute, Account, Adjustment, Country,  Currency

class PeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Period
        fields = [
            "period",
            "begin_date",
            "end_date" 
        ]
class ScenarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scenario
        fields = [
            "name",
            "description",
            "version",
            "periods"
        ]
class EntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entity
        fields = [
            "name",
            "entity_type",
            "scenario"
        ]
class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = [
            "attribute_value",
            "attribute_name",
            "begin_date",
            "end_date",
        ]

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            "account_name",
            "amount",
            "period",
            "collection",
            "acc_class",
            "currency",
            "entity",
            "data_type"
        ]
class AdjustmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adjustment
        fields = [
            "account",
            "adj_type",
            "adj_collection",
            "adj_class",
            "adj_percentage",
            "adj_amount"
        ]
class Currency(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = [
            "name",
            "begin_date",
            "end_date",
            "avg_rate",
            "end_spot_rate"
        ]
class Country(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = [
            "name",
            "currency"
        ]