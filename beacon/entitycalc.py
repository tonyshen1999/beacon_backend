from .models import Period,Scenario,Entity,Attribute, Country, Currency, Account, Adjustment, Relationship, Calculation
from .logmodel import Log

class EntityCalc:

    '''
    ********** HELPER METHODS ***************
    '''

    def __init__(self, entity, period, calc_model = None):
        self.entity = entity
        self.period = period
        self.attributes = Attribute.objects.filter(entity = self.entity)
        self.scenario = self.entity.scenario
        self.accounts = self.get_accounts()
        self.calculated = False
        self.children = {}
        self.parents = {}
        self.calc_model = calc_model

        # print(self.accounts)
        
        

    def __str__(self):
        return self.entity.__str__() + ", " + self.period.__str__() + ", " + self.scenario.__str__() +", Num children:" + str(len(self.children.keys()))
    
    def __hash__(self):
        return hash(self.entity) ^ hash(self.period)

    def __eq__(self, other):
        return (self.entity,self.period) == (other.entity,other.period)

    # Create a log here and push to Front End during calc
    def create_account(self, 
        account_name,
        amount,
        collection = "", 
        acc_class = "", 
        currency = None,
        data_type = 0):

        # print(
        # account_name,
        # amount,
        # collection, 
        # acc_class, 
        # currency,
        # data_type)

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
        # print(a.scenario,a.entity,a)
        log = Log(account=a,status=0,calculation = self.calc_model)
        log.save()
    
    def set_child(self, child, percent_owned):
        if isinstance(child, EntityCalc):
            self.children[child] = percent_owned
            child.parents[self] = percent_owned
        else:
            raise Exception("child must be EntityCalc type")

    # Check Collection a little wonky
    def get(self,name, collection = "TBFC"):
        # print(name,self.contains_account(name))
        if self.contains_account(name, collection) == False:
            
            a = Account(
                account_name = name,
                entity=self.entity,
                period = self.period,
                collection = collection,
                amount = 0,
                scenario = self.scenario
            )
            a.save()
            log = Log(account=a,status=1,message="Account was not found, so new account was created with 0 as amount",calculation=self.calc_model)
            log.save()
            

        else:
            a = self.accounts.get(
                account_name = name,
                collection = collection
            )
        return a
    

    def get_accounts(self):
        # print(Account.objects.filter(entity=self.entity,period=self.period))
        return Account.objects.filter(entity = self.entity, period = self.period)

    def clear_calc(self):
        accounts = self.get_accounts()
        accounts.exclude(collection="TBFC").delete()

    
    def clear_data(self):
        accounts = self.get_accounts()
        accounts.delete()
    
    def apply_all_adjustments(self):
        accounts = self.get_accounts()
        self.clear_calc()
        for a in accounts:
            a.apply_adjustments()

    def get_amount(self, name):
        amt = 0
        accounts = self.accounts.filter(account_name = name).all()
        
        for a in accounts:
            amt += a.amount
        return amt

    # Collection filtering a little wonky
    def contains_account(self,account, collection = "TBFC"):
        
        try:
            accounts = self.accounts.filter(account_name = account, collection = collection)
            
        except models.DoesNotExist:
            # Log that it wasn't found here
            return False

        if accounts.count() >0:
            return True
        return False

    '''
    ********** CALC METHODS ***************
    '''


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
        if self.calculated == False:
            self.clear_calc()
            self.sec163j()
            self.calculated = True
        # print(self.entity,self.period)

class CFCCalc(EntityCalc):

    def __init__(self, entity, period, calc_model=Calculation()):
        super().__init__(entity,period, calc_model)

    def calculate(self):
        if self.calculated == False:
            self.clear_calc()
            self.sec163j()
            self.CFC_tested_income()
            self.calculated = True
        
    
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

            
            tested_interest_expense_amt = self.get(name="InterestExpenseUtilized",collection="Sec163j").amount
            tested_interest_income_amt = self.get("InterestIncomeThirdParty").amount
            # print(hte_met)
            if hte_met == True:
                
                tested_interest_expense_amt = 0
                tested_interest_income_amt = 0

            tested_interest_expense_amt = max(tested_interest_expense_amt-tested_loss_qbai_amt,0)

            self.create_account(account_name="TestedInterestIncome",amount=tested_interest_income_amt,collection=collect)
            self.create_account(account_name="TestedInterestExpense",amount=tested_interest_expense_amt,collection=collect)

            tested_income_taxes_amt = self.get("IncomeTaxes").amount
            if hte_met:
                tested_income_taxes_amt = 0
            self.create_account(account_name="TestedIncomeTaxes",amount=tested_income_taxes_amt,collection=collect)

class USSHCalc(EntityCalc):
    
    def __init__(self, entity, period, calc_model = Calculation()):
        super().__init__(entity,period, calc_model)

    def calculate(self):
        if self.calculated == False:
            self.clear_calc()
            self.USSH951A()
            self.calculated = True
        
        
    def USSH951A(self):
        agg_cfc_tested_income_amt = 0
        agg_cfc_tested_loss_amt = 0
        qbai_amt = 0
        agg_tested_interest_inc_amt = 0
        agg_tested_interest_exp_amt = 0
        agg_tested_income_tax_amt = 0
        children = self.children
        collect = "USSH951A"
        qbai_perc = 0 # this is a little wonky
        print("----------------\n num children:",len(children))
        # x is type EntityCalc
        for x in children.keys():
            x.calculate()

            qbai_perc = x.get_attribute("QBAIPerc")
            
            agg_cfc_tested_income_amt += x.get("TestedIncome","TestedIncome").amount*children[x]
            agg_cfc_tested_loss_amt += x.get("TestedLoss","TestedIncome").amount*children[x]
            net_cfc_tested_income_amt = agg_cfc_tested_income_amt+agg_cfc_tested_loss_amt

            qbai_amt += x.get("TestedIncomeQBAI","TestedIncome").amount*children[x]
            agg_tested_interest_inc_amt += x.get("TestedInterestIncome","TestedIncome").amount*children[x]
            agg_tested_interest_exp_amt += x.get("TestedInterestExpense","TestedIncome").amount*children[x]
            agg_tested_income_tax_amt += x.get("TestedIncomeTaxes","TestedIncome").amount*children[x]


        specified_interest_exp_amt = max(agg_tested_interest_inc_amt+agg_tested_interest_exp_amt,0)
        dtir = max((qbai_amt*qbai_perc)-specified_interest_exp_amt,0)
        gilti_amt = (-1*net_cfc_tested_income_amt)-dtir

        
        self.create_account(account_name="AggregateCFCTestedIncome",amount=agg_cfc_tested_income_amt,collection=collect)
        self.create_account(account_name="AggregateCFCTestedLoss",amount=agg_cfc_tested_loss_amt,collection=collect)
        self.create_account(account_name="NetCFCTestedIncome",amount=net_cfc_tested_income_amt,collection=collect)
        self.create_account(account_name="AggregateQBAI",amount=qbai_amt,collection=collect)
        self.create_account(account_name="AggregateTestedInterestIncome",amount=agg_tested_interest_inc_amt,collection=collect)
        self.create_account(account_name="AggregateTestedInterestExpnese",amount=agg_tested_interest_exp_amt,collection=collect)
        self.create_account(account_name="AggregateTestedIncomeTax",amount=agg_tested_income_tax_amt,collection=collect)




        self.create_account(account_name="SpecifiedInterestExpense",amount=specified_interest_exp_amt,collection=collect)
        self.create_account(account_name="GILTI",amount=gilti_amt,collection=collect)
        self.create_account(
            account_name="Sec78GrossUpOnGILTI",
            amount= (gilti_amt/agg_cfc_tested_income_amt)*agg_tested_income_tax_amt,
            collection=collect)
        self.create_account(
            account_name="GILTIInclusionPercentage",
            amount= (gilti_amt/agg_cfc_tested_income_amt) ,
            collection=collect)

            
