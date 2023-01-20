from rest_framework import serializers
from .models import Period,Scenario,Entity, Attribute, Account, Adjustment, Country,  Currency, Relationship

class PeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Period
        fields = [
            "period",
            "begin_date",
            "end_date",
            "scenario"
        ]
class ScenarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scenario
        fields = [
            "scn_id",
            "name",
            "description",
            "version",
            "modify_date",
        ]

class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = [
            "attribute_value",
            "attribute_name",
            "begin_date",
            "end_date",
            "entity_name",
        ]
class RelationshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relationship
        fields = [
            "parent_name",
            "child_name",
            "ownership_percentage",

        ]
class EntitySerializer(serializers.ModelSerializer):
    relationships = RelationshipSerializer
    attributes=AttributeSerializer
    class Meta:
        model = Entity
        fields = [
            "name",
            "entity_type",
            "country",
            "scenario"
        ]
class AdjustmentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Adjustment
        fields = [
            "account_name",
            "entity",
            "adj_type",
            "adj_collection",
            "adj_class",
            "adj_percentage",
            "adj_amount"
        ]
class AccountSerializer(serializers.ModelSerializer):
    adjustments = AdjustmentSerializer
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
            "data_type",
            "scenario",
        ]

class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = [
            "name",
            "begin_date",
            "end_date",
            "avg_rate",
            "end_spot_rate"
        ]
class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = [
            "name",
            "currency"
        ]
