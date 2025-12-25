from .comercial_bank import comercial_bank
from .investment_bank import investment_bank
from .client import client

class App:

    comercial_banks_db={
        'Banca Transilvania':'banca_comerciala1',
        'ING':'banca_comerciala2',
        'BCR':'banca_comerciala3'
    }
    investment_banks_db={
        'Investment Center':'investment_bank1',
        'Neo Invest':'investment_bank2',
        'Investment Group':'investment_bank3'
    }

    def __init__(self):
        print("Before we start you have to give us a few informations. Please fill out the next form:")
        first_name=input("Your first name: ")
        last_name=input("Your last name: ")
        phone_number=input("Your phone: ")
        email=input("Your email: ")
        CNP=input("Your CNP: ")

        self.client=client(first_name,last_name,phone_number,email,CNP)
        self.banks=[]

        for key,value in App.comercial_banks_db.items():
            self.banks.append(comercial_bank(key,value))

        for key,value in App.investment_banks_db.items():
            self.banks.append(investment_bank(key,value))

        for bank in self.banks:
            accounts=bank.return_accounts(self.client.CNP)
            if accounts!=None:
                self.client.accounts+=accounts
    
    def show_all_banks(self):
        for bank in self.banks:
            bank.describe_bank()

    def show_comercial(self):
        for bank in self.banks:
            if isinstance(bank,comercial_bank):
                bank.describe_bank()

    def show_investment(self):
        for bank in self.banks:
            if isinstance(bank,investment_bank):
                bank.describe_bank()

    def open_account(self,index,balance):
        new_account=self.banks[index].open_account(self.client.first_name,self.client.last_name,self.client.phone_number,self.client.email,self.client.CNP,balance)
        self.client.accounts.append(new_account)

    def close_account(self,index,account):
        return self.banks[index].close_account(account)

    def calculateMinimumCapitalOfBank(self,bank):
        if bank.calculateMinimumCapital()==True:
            print("The bank has the minimum capital required.")
        else:
            print("The bank doesn't have the minimum capital required.")

    def CheckSolvencyOfBank(self,bank):
        if bank.CheckSolvency()==True:
            print("The bank has the minimum capital required in order to be solvent.")
        else:
            print("The bank doesn't have the minimum capital required in order to be solvent.")

    def isRegulationCompliant(self,bank):
        if bank.isRegulationCompliant()==True:
            print("The bank is legal with all the regulations.")
        else:
            print("The bank is not legal with all the regulations.")

    def get_loan(self,bank,account,sum):
        bank.grant_loan(account,sum)

    def deposit_money(self,bank,account,sum):
        bank.deposit_money(account,sum)

    def take_money(self,bank,account,sum):
        bank.take_money(account,sum)

    def show_opportunities_of_investment(self,bank,stock_name):
        price=bank.show_invesments_oportunities(stock_name)

        return price

    def invest(self,bank,account,quantity,price_per_stock,stock_name):
        bank.invest(account,quantity,price_per_stock,stock_name)

    def sell(self,bank,account,id,current_price):
        bank.sell(account,id,current_price)

    def run(self):
        print("Now that you have completed we can start:")
        print()
        number=0
        while number!=16:
            print("1. Show all the banks.")
            print("2. Show comercial banks.")
            print("3. Show investment banks.")
            print("4. Open account.")
            print("5. Close account.")
            print("6. See if a certain bank has the minimum capital required.")
            print("7. See if a certain bank is solvent.")
            print("8. See if a certain bank respects the regulations.")
            print("9. Get a loan.")
            print("10. Deposit money.")
            print("11. Take out some money.")
            print("12. Choose a company and see it's stock price.")
            print("13. Invest in a stock.")
            print("14. Sell a stock.")
            print("15. Show your accounts.")
            print("16. Stop the app.")

            number=int(input("Your number is: "))

            while number<1 or number>16:
                print("The number has to be between 1 and 15. Introduce another number.")
                number=int(input("Your number is: "))

            if number==1:
                self.show_all_banks()
            elif number==2:
                self.show_comercial()
            elif number==3:
                self.show_investment()
            elif number==4:
                print("Introduce 1 for comercial and 2 for investment.")
                choose_type_of_bank=int(input("Your number is: "))

                while choose_type_of_bank<1 or choose_type_of_bank>2:
                    print("The number has to be either 1 or 2. Choose a goon number.")
                    choose_type_of_bank=int(input("Yout number is: "))
                
                if choose_type_of_bank==1:
                    comercial_banks_index=[]
                    for i in range(len(self.banks)):
                        if isinstance(self.banks[i],comercial_bank):
                            comercial_banks_index.append(i)
                            self.banks[i].describe_bank()
                    
                    print("Choose a number from 1 to 3 reprezenting the chosen bank.")

                    index=int(input("Your number is: "))

                    while index<1 or index>3:
                        print("The number choosen doesn't convine to the rules. It has to be a number from 1 to 3.")
                        index=int(input("Your number is: "))

                    balance=float(input("Your balance is:"))
                    
                    self.open_account(comercial_banks_index[index-1],balance)
                else:
                    investment_banks_index=[]
                    for i in range(len(self.banks)):
                        if isinstance(self.banks[i],investment_bank):
                            investment_banks_index.append(i)
                            self.banks[i].describe_bank()
                    
                    print("Choose a number from 1 to 3 reprezenting the chosen bank.")

                    index=int(input("Your number is: "))

                    while index<1 or index>3:
                        print("The number choosen doesn't convine to the rules. It has to be a number from 1 to 3.")
                        index=int(input("Your number is: "))

                    balance=float(input("Your balance is:"))
                    
                    self.open_account(investment_banks_index[index-1],balance)
            elif number==5:
                if len(self.client.accounts)==0:
                    print("You don't have any account.")
                else:
                    self.client.show_accounts()

                    print(f"Choose a number from 1 to {len(self.client.accounts)} that reprezents your account.")
                    index=int(input("Your number: "))

                    while index<1 or index>len(self.client.accounts):
                        print(f"The number choosen doesn't convine to the rules. It has to be a number from 1 to {len(self.client.accounts)}")
                        index=int(input("Your number: "))
                    
                    if self.client.accounts[index-1].bank_name=='Banca Transilvania':
                        can_be_closed=self.close_account(0,self.client.accounts[index-1])
                    elif self.client.accounts[index-1].bank_name=='ING':
                        can_be_closed=self.close_account(1,self.client.accounts[index-1])
                    elif self.client.accounts[index-1].bank_name=='BCR':
                        can_be_closed=self.close_account(2,self.client.accounts[index-1])
                    elif self.client.accounts[index-1].bank_name=='Investment Center':
                        can_be_closed=self.close_account(3,self.client.accounts[index-1])
                    elif self.client.accounts[index-1].bank_name=='Neo Invest':
                        can_be_closed=self.close_account(4,self.client.accounts[index-1])
                    elif self.client.accounts[index-1].bank_name=='Investment Group':
                        can_be_closed=self.close_account(5,self.client.accounts[index-1])

                    if can_be_closed==True:
                        self.client.accounts.pop(index-1)
            elif number==6:
                self.show_all_banks()

                print('\n',"Choose a number between 1 and 6 that reprezents the bank choosen.")

                index=int(input("Your number is: "))

                while index<1 or index>6:
                    print("Your number has to be between 1 and 6")
                    index=int(input("Your number is: "))
                
                if self.banks[index-1].calculateMinimumCapital()==True:
                    print("The bank has the minimum capital.")
                else:
                    print("The bank doesn't have the minimum capital.")
            elif number==7:
                self.show_all_banks()

                print('\n', "Choose a number between 1 and 6 that reprezents the bank choosen.")

                index=int(input("Your number is: "))

                while index<1 or index>6:
                    print("Your number has to be between 1 and 6")
                    index=int(input("Your number is: "))
                
                if self.banks[index-1].checkSolvency():
                    print("The bank is solvent.")
                else:
                    print("The bank is not solvent.")
            elif number==8:
                self.show_all_banks()

                print('\n', "Choose a number between 1 and 6 that reprezents the bank choosen.")

                index=int(input("Your number is: "))

                while index<1 or index>6:
                    print("Your number has to be between 1 and 6")
                    index=int(input("Your number is: "))
                
                if self.banks[index-1].isRegulationCompliant():
                    print("The bank is regulation compliant and can legally work.")
                else:
                    print("The bank is not regulation compliant, so choose carefully if you trust it.")
            elif number==9:
                account_index=[]
                for i in range(len(self.client.accounts)):
                    if self.client.accounts[i].bank_name=='Banca Transilvania' or self.client.accounts[i].bank_name=='ING' or self.client.accounts[i].bank_name=='BCR':
                        account_index.append(i)
                        self.client.accounts[i].describe_account()

                if len(account_index)==0:
                    print("You don't have any account to a comercial bank. Open one in order to get a loan.")
                else:
                    print(f"Choose a number from 1 to {len(account_index)} that represents the account to choose for the loan.")

                    index=int(input("Your number is: "))

                    while index<1 or index>len(account_index):
                        print(f"Your number has to be between 1 and {len(account_index)}")
                        index=int(input("Your number is: "))
                    
                    sum=float(input("The sum of money that you want to borrow is: "))

                    if self.client.accounts[account_index[index-1]].bank_name=='Banca Transilvania':
                        self.get_loan(self.banks[0],self.client.accounts[account_index[index-1]],sum)
                    elif self.client.accounts[account_index[index-1]].bank_name=='ING':
                        self.get_loan(self.banks[1],self.client.accounts[account_index[index-1]],sum)
                    elif self.client.accounts[account_index[index-1]].bank_name=='BCR':
                        self.get_loan(self.banks[2],self.client.accounts[account_index[index-1]],sum)
            elif number==10:
                account_index=[]
                for i in range(len(self.client.accounts)):
                    if self.client.accounts[i].bank_name=='Banca Transilvania' or self.client.accounts[i].bank_name=='ING' or self.client.accounts[i].bank_name=='BCR':
                        account_index.append(i)
                        self.client.accounts[i].describe_account()

                if len(account_index)==0:
                    print("You don't have any account to a comercial bank. Open one in order to deposit money.")
                else:
                    print(f"Choose a number from 1 to {len(account_index)} that represents the account to choose for depositing the money.")

                    index=int(input("Your number is: "))

                    while index<1 or index>len(account_index):
                        print(f"Your number has to be between 1 and {len(account_index)}")
                        index=int(input("Your number is: "))
                    
                    sum=float(input("The sum of money that you want to deposit is: "))

                    if self.client.accounts[account_index[index-1]].bank_name=='Banca Transilvania':
                        self.deposit_money(self.banks[0],self.client.accounts[account_index[index-1]],sum)
                    elif self.client.accounts[account_index[index-1]].bank_name=='ING':
                        self.deposit_money(self.banks[1],self.client.accounts[account_index[index-1]],sum)
                    elif self.client.accounts[account_index[index-1]].bank_name=='BCR':
                        self.deposit_money(self.banks[2],self.client.accounts[account_index[index-1]],sum)
            elif number==11:
                account_index=[]
                for i in range(len(self.client.accounts)):
                    if self.client.accounts[i].bank_name=='Banca Transilvania' or self.client.accounts[i].bank_name=='ING' or self.client.accounts[i].bank_name=='BCR':
                        account_index.append(i)
                        self.client.accounts[i].describe_account()

                if len(account_index)==0:
                    print("You don't have any account to a comercial bank.")
                else:
                    print(f"Choose a number from 1 to {len(account_index)} that represents the account to choose for taking out some money.")

                    index=int(input("Your number is: "))

                    while index<1 or index>len(account_index):
                        print(f"Your number has to be between 1 and {len(account_index)}")
                        index=int(input("Your number is: "))
                    
                    sum=float(input("The sum of money that you want to take out: "))

                    if self.client.accounts[account_index[index-1]].bank_name=='Banca Transilvania':
                        self.take_money(self.banks[0],self.client.accounts[account_index[index-1]],sum)
                    elif self.client.accounts[account_index[index-1]].bank_name=='ING':
                        self.take_money(self.banks[1],self.client.accounts[account_index[index-1]],sum)
                    elif self.client.accounts[account_index[index-1]].bank_name=='BCR':
                        self.take_money(self.banks[2],self.client.accounts[account_index[index-1]],sum)
            elif number==12:
                stock_map = {
                    "Apple": "AAPL",
                    "Microsoft": "MSFT",
                    "Google": "GOOGL",
                    "Amazon": "AMZN",
                    "Tesla": "TSLA",
                    "Meta": "META",
                    "Netflix": "NFLX",
                    "NVIDIA": "NVDA",
                    "Intel": "INTC",
                    "IBM": "IBM"
                }

                i=1
                for key in stock_map.keys():
                    print(str(i)+". "+key)
                    i+=1

                print("Choose the name that reprezents the stock where you want to see the price.")

                stock_name=input("The name is: ")

                while stock_name not in stock_map.keys():
                    print("The name introduces is not acurate. Introduce it again and do is as shown.")
                    stock_name=input("The name is: ")

                price=investment_bank.show_investments_oportunities(stock_map[stock_name])

                print(f"The price of the stock choosen if {price}")
            elif number==13:
                account_index=[]
                for i in range(len(self.client.accounts)):
                    if self.client.accounts[i].bank_name=='Investment Center' or self.client.accounts[i].bank_name=='Neo Invest' or self.client.accounts[i].bank_name=='Investment Group':
                        account_index.append(i)
                        self.client.accounts[i].describe_account()

                if len(account_index)==0:
                    print("You don't have any account to an investment bank.")
                else:
                    print(f"Choose a number from 1 to {len(account_index)} that represents the account to choose for buying stock.")

                    index=int(input("Your number is: "))

                    while index<1 or index>len(account_index):
                        print(f"Your number has to be between 1 and {len(account_index)}")
                        index=int(input("Your number is: "))

                    stock_map = {
                        "Apple": "AAPL",
                        "Microsoft": "MSFT",
                        "Google": "GOOGL",
                        "Amazon": "AMZN",
                        "Tesla": "TSLA",
                        "Meta": "META",
                        "Netflix": "NFLX",
                        "NVIDIA": "NVDA",
                        "Intel": "INTC",
                        "IBM": "IBM"
                    }

                    i=1
                    for key in stock_map.keys():
                        print(str(i)+". "+key)
                        i+=1

                    print("Choose the name that reprezents the stock that you want to buy.")

                    stock_name=input("The name is: ")

                    while stock_name not in stock_map.keys():
                        print("The name introduces is not acurate. Introduce it again and do is as shown.")
                        stock_name=input("The name is: ")

                    print("Choose the quantity")
                    quantity=int(input("Guantity: "))

                    price=investment_bank.show_investments_oportunities(stock_map[stock_name])

                    if self.client.accounts[account_index[index-1]].bank_name=='Investment Center':
                        self.invest(self.banks[3],self.client.accounts[account_index[index-1]],quantity,price,stock_name)
                    elif self.client.accounts[account_index[index-1]].bank_name=='Neo Invest':
                        self.invest(self.banks[4],self.client.accounts[account_index[index-1]],quantity,price,stock_name)
                    elif self.client.accounts[account_index[index-1]].bank_name=='Investment Group':
                        self.invest(self.banks[5],self.client.accounts[account_index[index-1]],quantity,price,stock_name)
            elif number==14:
                account_index=[]
                for i in range(len(self.client.accounts)):
                    if self.client.accounts[i].bank_name=='Investment Center' or self.client.accounts[i].bank_name=='Neo Invest' or self.client.accounts[i].bank_name=='Investment Group':
                        account_index.append(i)
                        self.client.accounts[i].describe_account()

                if len(account_index)==0:
                    print("You don't have any account to an investment bank.")
                else:
                    print(f"Choose a number from 1 to {len(account_index)} that represents the account to choose for buying stock.")

                    index=int(input("Your number is: "))

                    while index<1 or index>len(account_index):
                        print(f"Your number has to be between 1 and {len(account_index)}")
                        index=int(input("Your number is: "))

                    stock_map = {
                        "Apple": "AAPL",
                        "Microsoft": "MSFT",
                        "Google": "GOOGL",
                        "Amazon": "AMZN",
                        "Tesla": "TSLA",
                        "Meta": "META",
                        "Netflix": "NFLX",
                        "NVIDIA": "NVDA",
                        "Intel": "INTC",
                        "IBM": "IBM"
                    }

                    ids_and_company_name=None
                    if self.client.accounts[account_index[index-1]].bank_name=='Investment Center':
                        ids_and_company_name=self.banks[3].show_investments_and_return_ids_and_company(self.client.accounts[account_index[index-1]])
                    elif self.client.accounts[account_index[index-1]].bank_name=='Neo Invest':
                        ids_and_company_name=self.banks[4].show_investments_and_return_ids_and_company(self.client.accounts[account_index[index-1]])
                    elif self.client.accounts[account_index[index-1]].bank_name=='Investment Group':
                        ids_and_company_name=self.banks[5].show_investments_and_return_ids_and_company(self.client.accounts[account_index[index-1]])
                    
                    if len(ids_and_company_name)==0:
                        print("You don't have any stock on this account.")
                    else:
                        print(f"Choose a number from 1 to {len(ids_and_company_name)}.")
                        id_number=int(input("Your number is: "))

                        while id_number<1 or id_number>len(ids_and_company_name):
                            print(f"The number has to be between 1 and {len(ids_and_company_name)}")
                            id_number=int(input("Your number is: "))
                        
                        current_price=investment_bank.show_investments_oportunities(stock_map[ids_and_company_name[id_number-1][1]])

                        if self.client.accounts[account_index[index-1]].bank_name=='Investment Center':
                            self.sell(self.banks[3],self.client.accounts[account_index[index-1]],ids_and_company_name[id_number-1][0],current_price)
                        elif self.client.accounts[account_index[index-1]].bank_name=='Neo Invest':
                            self.sell(self.banks[4],self.client.accounts[account_index[index-1]],ids_and_company_name[id_number-1][0],current_price)
                        elif self.client.accounts[account_index[index-1]].bank_name=='Investment Group':
                            self.sell(self.banks[5],self.client.accounts[account_index[index-1]],ids_and_company_name[id_number-1][0],current_price)

            elif number==15:
                self.client.show_accounts()