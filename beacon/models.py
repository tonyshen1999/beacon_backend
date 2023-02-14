from django.db import models
from datetime import datetime
import copy

class Scenario(models.Model):
    
    scn_id = models.IntegerField(default=1,primary_key=False)
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=500, blank=True, null=True)
    version = models.IntegerField(default=1)
    modify_date = models.DateTimeField(
        default = datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        null=True,
        blank=True
        )

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
        return str(self.scenario.scn_id) + "." + str(self.scenario.version) + "," + self.period
    def get_year(self, period = ""):
        if period == "":
            period = self.period
        return int(period.replace("CYE","").replace("FYE",""))
    def __add__(self,other):
        if isinstance(other,int):
            return self.period.replace(str(self.get_year()),"") + str(self.get_year()+other)
        else:
            raise Exception("Can only add integer value to period")

    def __sub__(self,other):
        if isinstance(other,int):
            return self.period.replace(str(self.get_year()),"") + str(self.get_year()-other)
        else:
            raise Exception("Can only subtract integer value to period")

    # class Meta:
    #     unique_together = ("period","scenario")

    def new_period(self, period):
        diff = self.get_year(period) - self.get_year()
        beg_year = self.begin_date.year + diff
        end_year = self.end_date.year + diff
        beg_day = self.begin_date.day
        end_day = self.end_date.day
        beg_month = self.begin_date.month
        end_month = self.end_date.month
        
        new_begin_date = str(beg_year)+"-"+str(beg_month)+"-"+str(beg_day)
        new_end_date = str(end_year)+"-"+str(end_month)+"-"+str(end_day)
        p = Period(period=period,begin_date=new_begin_date,end_date=new_begin_date,scenario=self.scenario)
        p.save()
        print(new_begin_date)

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
        return str(self.scenario.scn_id) + "." + str(self.scenario.version) + "," + self.name

class Attribute(models.Model):
    attribute_name = models.CharField(max_length=100)
    attribute_value = models.CharField(max_length=50)
    begin_date = models.DateField()
    end_date = models.DateField(null=True, blank = True)
    # scenario = models.ForeignKey(Scenario,on_delete=models.CASCADE)
    entity = models.ForeignKey(Entity,on_delete=models.CASCADE)

    class Meta:
        unique_together = ('entity','attribute_name')
    def __str__(self):
        return self.attribute_name
    @property
    def entity_name(self):
        return  self.entity.name
    
class DefaultAttribute(models.Model):
    entity_type = models.CharField(max_length=100)
    attribute_name = models.CharField(max_length=100)
    attribute_value = models.CharField(max_length=50)
    begin_date = models.DateField()
    end_date = models.DateField(null=True, blank = True)

    class Meta:
        unique_together = ('entity_type','attribute_name')

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
        unique_together = ('account_name', 'scenario','entity','collection')
    @property
    def entity_name(self):
        return self.entity.name
    @property
    def period_name(self):
        return self.period.period
    
    def __str__(self):
        return   self.account_name  + ", " + self.collection + "," + self.entity.__str__()
    
    def apply_adjustments(self):
       
        adjustments = Adjustment.objects.filter(account=self)
        for adj in adjustments:
            a = Account(
                account_name = self.account_name,
                amount = adj.adj_amount,
                period = self.period,
                collection = adj.adj_type,
                acc_class = self.acc_class,
                currency = self.currency,
                entity = self.entity,
                data_type = self.data_type,
                scenario = self.scenario
            )
            a.save()
        return adjustments





class Calculation(models.Model):
    date_time = models.DateTimeField(auto_now=True, blank=True, null = True)
    scenario = models.ForeignKey(Scenario,on_delete=models.CASCADE)
    
class Adjustment(models.Model):

    account = models.ForeignKey(Account,on_delete=models.CASCADE)
    adj_type = models.CharField(max_length=100)
    adj_collection = models.CharField(max_length=100,null=True,blank=True)
    adj_class = models.CharField(max_length=100,null=True,blank=True)
    adj_percentage = models.FloatField(null=True,blank=True)
    adj_amount = models.FloatField(null=True)    

    def __str__(self):
        return self.account.__str__() + ", " + self.adj_type
    @property
    def account_name(self):
        return self.account.account_name
    @property
    def entity(self):
        return self.account.entity.name
    @property
    def period(self):
        return self.account.period.period

class Relationship(models.Model):

    parent = models.ForeignKey(Entity, related_name='parent', on_delete=models.CASCADE)
    child = models.ForeignKey(Entity, related_name='child', on_delete=models.CASCADE)
    ownership_percentage = models.FloatField()
    scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE)
    period = models.ForeignKey(Period, on_delete=models.CASCADE, null=True,blank=True)  # Questionable

    def __str__(self):
        return self.parent.__str__() + " owns " + self.child.__str__()
    @property
    def parent_name(self):
        return self.parent.name
    @property
    def child_name(self):
        return self.child.name

class CalcAction(models.Model):

    entity = models.ForeignKey(Entity,on_delete=models.CASCADE)
    period = models.ForeignKey(Period, on_delete=models.CASCADE)
    action = models.CharField(max_length=50)

    @property
    def entity_name(self):
        return self.entity.name

    @property
    def pd_name(self):
        return self.period.period


