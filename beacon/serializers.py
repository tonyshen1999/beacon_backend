from rest_framework import serializers
from .models import Period,Scenario,Entity

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