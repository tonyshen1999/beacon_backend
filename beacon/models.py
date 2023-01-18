from django.db import models



class Scenario(models.Model):

    scn_id = models.IntegerField(default=1,primary_key=False)
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=500, blank=True, null=True)
    version = models.IntegerField(default=1)

    class Meta:
        unique_together = ("scn_id", "version")

    def __str__(self):
        return str(self.scn_id) + "." + str(self.version) + ": " + self.name

class Period(models.Model):
    period = models.CharField(max_length=10)
    begin_date = models.DateField()
    end_date = models.DateField()
    scenario = models.ForeignKey(Scenario,on_delete=models.CASCADE)

    def __str__(self):
        return self.period

# This should autopopulate when initialized
class Currency(models.Model):
    name = models.CharField(max_length=5)
    begin_date = models.DateField(null=True, blank =True)
    end_date = models.DateField(null=True, blank=True)
    avg_rate = models.FloatField(null=True, blank=True)
    end_spot_rate = models.FloatField(null=True, blank=True)
    def __str__(self):
        return self.name

# This should autopopulate when initialized
class Country(models.Model):
    name = models.CharField(max_length=100)
    currency = models.ForeignKey(Currency,on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Entity(models.Model):
    name = models.CharField(max_length=200)
    entity_type = models.CharField(max_length=50)
    scenario = models.ForeignKey(Scenario,on_delete=models.CASCADE)
    country = models.ForeignKey(Country,on_delete=models.CASCADE,blank=True,null=True)
    class Meta:
        unique_together = ('name', 'scenario')

    def __str__(self):
        return self.name

class Attribute(models.Model):
    attribute_name = models.CharField(max_length=100)
    attribute_value = models.CharField(max_length=50)
    begin_date = models.DateField()
    end_date = models.DateField(null=True, blank = True)
    # scenario = models.ForeignKey(Scenario,on_delete=models.CASCADE)
    entity = models.ForeignKey(Entity,on_delete=models.CASCADE)
    def __str__(self):
        return self.attribute_name



class Account(models.Model):

    account_name = models.CharField(max_length=100)
    amount = models.FloatField()
    period = models.ForeignKey(Period, on_delete=models.CASCADE)
    collection = models.CharField(max_length=100,null=True, blank=True)
    acc_class = models.CharField(max_length=100,null=True, blank=True)
    currency = models.ForeignKey(Currency,on_delete=models.CASCADE, null=True, blank=True)
    entity = models.ForeignKey(Entity,on_delete=models.CASCADE)
    data_type = models.IntegerField(null=True, blank=True)
    scenario = models.ForeignKey(Scenario,on_delete=models.CASCADE)

    class Meta:
        unique_together = ('account_name', 'scenario','entity')
    def __str__(self):
        return   self.account_name  + ", " + self.entity.__str__()

class Adjustment(models.Model):

    account = models.ForeignKey(Account,on_delete=models.CASCADE)
    adj_type = models.CharField(max_length=100)
    adj_collection = models.CharField(max_length=100,null=True,blank=True)
    adj_class = models.CharField(max_length=100,null=True,blank=True)
    adj_percentage = models.FloatField(null=True,blank=True)
    adj_amount = models.FloatField(null=True)    

    def __str__(self):
        return self.account.__str__() + ", " + self.adj_type

class Relationship(models.Model):

    parent = models.ForeignKey(Entity, related_name='parent', on_delete=models.CASCADE)
    child = models.ForeignKey(Entity, related_name='child', on_delete=models.CASCADE)
    ownership_percentage = models.FloatField()
    scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE)

    def __str__(self):
        return self.parent.__str__() + " owns " + self.child.__str__()
