'''
Future Deprecation:
To be replaced with Django websocket
'''


from django.db import models
from datetime import datetime
import copy
from .models import Account, Scenario, Period


class Log(models.Model):

    '''
    To change  to CalcLog
    Status: [
        0 -> success,
        1 -> general message,
        2 -> error
    ]
    '''

    account = models.ForeignKey(Account,on_delete = models.CASCADE,blank = True, null = True)
    status = models.IntegerField(default=0,primary_key=False)
    message = models.TextField(null=True,blank=True)
    date_time = models.DateTimeField(auto_now_add=True)
    @property
    def log_text(self):
        message = ""
        acct_str = self.account.__str__()
        if self.status == 0:
            message +=  "Successfully created <" + acct_str + ">"

        elif self.status == 1:
            message += "<" + acct_str + "> Message: " + message
        else:
            message += "Error <" + acct_str + "> with Exception:" + message 

        return message

    def __str__(self):
        return self.log_text

class ImportLog(models.Model):
    log_type = models.CharField(max_length=20)
    name = models.CharField(max_length=50)
    message  = models.TextField(null=True,blank=True)
    status = models.IntegerField(default=0,primary_key=False)
    date_time = models.DateTimeField(auto_now_add=True, blank=True, null = True)
    scenario = models.ForeignKey(Scenario,on_delete=models.CASCADE)
    
    @property
    def log_text(self):

        message = ""
        if self.status == 0:
            message +=  "<" + self.name + "> of '" + self.log_type + "' type was successfully imported"

        elif self.status == 1:
            message += "<" + self.name + "> of '" + self.log_type + "' type, Message: " + self.message
        else:
            message += "<" + self.name + "> of '" + self.log_type + "' type, with Exception:" + self.message 

        
        return message
    def __str__(self):
        return self.log_text