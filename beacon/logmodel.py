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
    Status: [
        0 -> success,
        1 -> general message,
        2 -> error
    ]
    '''

    account = models.ForeignKey(Account,on_delete = models.CASCADE,blank = True, null = True)
    status = models.IntegerField(default=0,primary_key=False)
    message = models.TextField(null=True,blank=True)

    @property
    def log_text(self):

        acct_str = self.account.__str__()
        if self.status == 0:
            return  "Successfully created <" + acct_str + ">"

        elif self.status == 1:
            return "<" + acct_str + "> Message: " + message
        else:
            return "Error <" + acct_str + "> with Exception:" + message 


    def __str__(self):
        return self.log_text