from django.contrib import admin
from .models import Period,Scenario,Entity,Attribute,Country,Currency,Account, Adjustment, Relationship, Calculation, DefaultAttribute
from .logmodel import Log, ImportLog
admin.site.register(Period)
admin.site.register(Scenario)
admin.site.register(Entity)
admin.site.register(Attribute)
admin.site.register(Country)
admin.site.register(Currency)
admin.site.register(Account)
admin.site.register(Adjustment)
admin.site.register(Relationship)
admin.site.register(Log)
admin.site.register(ImportLog)
admin.site.register(Calculation)
admin.site.register(DefaultAttribute)