from django.shortcuts import render
from rest_framework import generics

from .models import Period,Scenario,Entity,Attribute, Country, Currency, Account, Adjustment
from .serializers import PeriodSerializer,ScenarioSerializer,EntitySerializer, AttributeSerializer, AccountSerializer,AdjustmentSerializer
from django_filters import rest_framework as filters
from django_filters import ModelChoiceFilter
from TestModel import TestModel
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['POST'])
def calculate(request):
    '''
    Request -> {
        Entity Name, entity_name
        Period Name, pd_name
        Scenario ID, scn_id
        Scenario Verion, scn_version
    }
    '''
    data = request.data
    
    scn = Scenario.objects.filter(
        scn_id = data["scn_id"],
        version = data["scn_version"]
    )[0]

    entity = Entity.objects.filter(
        name = data["entity_name"],
        scenario = scn
    )[0]

    period = Period.objects.filter(
        period = data["pd_name"],
        scenario = scn
    )[0]

    if entity.entity_type == "CFC":
        CFCCalc(entity,period).calculate()


    return Response(status=status.HTTP_201_CREATED)


class EntityCalc:
    def __init__(self, entity, period):
        self.entity = entity
        self.period = period
        self.attributes = Attribute.objects.filter(entity = self.entity)
        self.scenario = self.entity.scenario

    # Create a log here and push to Front End during calc
    def create_account(self, 
        account_name,
        amount,
        collection = "", 
        acc_class = "", 
        currency = None,
        data_type = 0):

        a = Account(
            account_name = account_name,
            amount = amount,
            period = self.period,
            collection = collection,
            acc_class = acc_class,
            currency = currency,
            entity = self.entity,
            scenario = self.entity.scenario, # redundancy, remove scenario from Account since Entity already has scenario field
            data_type = data_type

        )
        a.save()
    # Check Collection a little wonky
    def get(self,name, collection = "TBFC"):
        # print(name,self.contains_account(name))
        if self.contains_account(name) == False:
            a = Account(
                account_name = name,
                entity=self.entity,
                period = self.period,
                collection = collection,
                amount = 0,
                scenario = self.scenario
            )
            a.save()
            # Log that nothing was found
        else:
            a = Account.objects.get(
                account_name = name,
                entity = self.entity,
                period = self.period,
                collection = collection
            )
        # print(a)
        return a
    def get_accounts(self):
        return Account.objects.filter(entity = self.entity, period = self.period)
    def clear_calc(self):
        accounts = self.get_accounts()
        accounts.exclude(collection="TBFC").delete()
    def apply_all_adjustments(self):
        accounts = self.get_accounts()
        self.clear_calc()
        for a in accounts:
            a.apply_adjustments()

    def get_amount(self, name):
        amt = 0
        accounts = Account.objects.filter(account_name = name, period = self.period, entity= self.entity).all()
        
        for a in accounts:
            amt += a.amount
        return amt

    def contains_account(self,account):
        
        try:
            accounts = Account.objects.filter(entity=self.entity, account_name = account, period = self.period)
            
        except models.DoesNotExist:
            # Log that it wasn't found here
            return False

        if accounts.count() >0:
            return True
        return False
    def EBIT(self):
        if self.contains_account("EBIT") == False:
            ebit_amt = 0
            accounts = self.get_accounts().filter(collection="TBFC")
            for a in accounts:
                if a.account_name != "QBAI":
                    ebit_amt += a.amount
            
            self.create_account(account_name="EBIT",amount=ebit_amt,collection="EBIT")
        else:
            ebit_amt = self.get("EBIT").amount
        return ebit_amt
    def get_attribute(self, name):
        atr_value = self.attributes.get(attribute_name=name).attribute_value
        try:
            atr_value = float(atr_value)
            return atr_value
        except ValueError:
            return atr_value
    
    def EBIT_TI(self):
        if self.contains_account("EBIT_TI") == False:
            self.apply_all_adjustments()

            ebit_ti_amt = self.EBIT()
            m1_accounts = self.get_accounts().filter(collection__icontains="SchM-1Adj")

            for m in m1_accounts:
                ebit_ti_amt += m.amount
            
            self.create_account(account_name="EBIT_TI",amount=ebit_ti_amt,collection="EBIT_TI")
        else:
            ebit_ti_amt = self.get("EBIT_TI").amount
        return ebit_ti_amt
    def sec163j(self):
        self.clear_calc()
        if self.contains_account("EBIT_TI") == False:
            collect = "Sec163j"
            ebit_ti_amt = self.EBIT_TI()
            ati_amt = ebit_ti_amt + self.get("Depreciation").amount + self.get("Amortization").amount
            self.create_account(account_name="ATI",amount=ati_amt,collection=collect)

            sec163j_lim_amt = -1*(min(ati_amt*self.get_attribute("163jLimit_Perc"),0)+self.get("InterestIncomeThirdParty").amount+self.get("InterestIncomeIntercompany").amount)
            self.create_account(account_name="Section163jLimitation",amount=sec163j_lim_amt,collection=collect)

            py_disallowed_amt = 0
            py_pd = Period.objects.filter(scenario=self.scenario,period = (self.period-1))
            if py_pd.count() == 1:
                print(py_pd)
                py_disallowed = Account.objects.filter(account_name="Sec163DisallowedInterestExpense",period=py_pd[0])
                if py_disallowed.count() == 1:
                    py_disallowed_amt = py_disallowed[0].amount

            int_exp_util_amt = self.get("InterestExpenseThirdParty").amount + self.get("InterestExpenseIntercompany").amount + py_disallowed_amt
            int_exp_util_amt = min(int_exp_util_amt,sec163j_lim_amt)
            self.create_account(account_name="InterestExpenseUtilized",amount=int_exp_util_amt,collection=collect)
            # print(int_exp_util_amt)

            disallowed_int_exp_amt = self.get("InterestExpenseThirdParty").amount + self.get("InterestExpenseIntercompany").amount - int_exp_util_amt
            self.create_account(account_name="Sec163DisallowedInterestExpense",amount=disallowed_int_exp_amt,collection=collect)
            
        
    def calculate(self):
        self.sec163j()
        # print(self.entity,self.period)

class CFCCalc(EntityCalc):
    def __init__(self, entity, period):
        super().__init__(entity,period)
    def calculate(self):
        self.sec163j()
        self.CFC_tested_income()
    
    def CFC_tested_income(self):
        if self.contains_account("TentativeTestedIncomeBeforeTaxes") == False:
            collect = "TestedIncome"

            tent_tested_income_amt = self.get(name="EBIT_TI",collection="EBIT_TI").amount+self.get(name="InterestExpenseUtilized",collection="Sec163j").amount+self.get("InterestIncomeThirdParty").amount-self.get(name="SubpartFIncome",collection="SubpartF").amount

            self.create_account(account_name="TentativeTestedIncomeBeforeTaxes",amount=tent_tested_income_amt,collection=collect)

            tested_income_etr_amt = self.get(name="IncomeTaxes").amount/tent_tested_income_amt * -1
            hte = bool(self.get_attribute("Section951AHighTaxElection"))
            hte_met = (tested_income_etr_amt) > (self.get_attribute("HTETaxPercentage")*self.get_attribute("USTaxRate"))
            # print(hte_met)
            tested_loss_amt = 0
            tested_income_amt = 0

            if hte == False or hte_met == False:
                if tent_tested_income_amt > 0:
                    tested_loss_amt = tent_tested_income_amt
                    tested_income_amt = 0
                else:
                    tested_income_amt = tent_tested_income_amt
                    tested_loss_amt = 0
            
            self.create_account(account_name="TestedIncome",amount=tested_income_amt,collection=collect)
            self.create_account(account_name="TestedLoss",amount=tested_loss_amt,collection=collect)
            
            qbai_amount = 0
            if tested_income_amt < 0 and hte_met == False:
                qbai_amount = self.get("QBAI").amount
            self.create_account(account_name="TestedIncomeQBAI",amount=qbai_amount,collection=collect)
            
            

            tested_loss_qbai_amt = 0
            if tested_loss_amt>0:
                tested_loss_qbai_amt = self.get("QBAI").amount*self.get_attribute("TestedLossQBAIAmount")
            self.create_account(account_name="TestedLossQBAI",amount=tested_loss_qbai_amt,collection=collect)
            
            self.create_account(account_name="TestedIncome_ETR",amount=tested_income_etr_amt,collection=collect)

            
            tested_interest_expense_amt = self.get("InterestExpenseUtilized").amount
            tested_interest_income_amt = self.get("InterestIncomeThirdParty").amount
            # print(hte_met)
            if hte_met == True:
                
                tested_interest_expense_amt = 0
                tested_interest_income_amt = 0





            