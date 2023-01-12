from django.db import models

class Period(models.Model):
    period = models.CharField(max_length=10)
    begin_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.period

class Scenario(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=500, blank=True, null=True)
    version = models.IntegerField()
    periods = models.ManyToManyField(Period)

    def __str__(self):
        return self.name

class Entity(models.Model):
    name = models.CharField(max_length=200)
    entity_type = models.CharField(max_length=50)
    scenario = models.ForeignKey(Scenario,on_delete=models.CASCADE)

    def __str__(self):
        return self.name