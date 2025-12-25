from .comercial_bank import comercial_bank
from .investment_bank import investment_bank
from .client import client

#The class App that help us run the whole app
class App:

    #These are the class variables that hold the name of the bank and the db name(key:value)
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

    #The constructo of the App class
    def __init__(self):
        #Get the info from the user to create the client object
        print("Before we start you have to give us a few informations. Please fill out the next form:")
        first_name=input("Your first name: ")
        last_name=input("Your last name: ")
        phone_number=input("Your phone: ")
        email=input("Your email: ")
        CNP=input("Your CNP: ")

        #Create the client object
        self.client=client(first_name,last_name,phone_number,email,CNP)
        self.banks=[]

        #Take all the banks from the databases
        for key,value in App.comercial_banks_db.items():
            self.banks.append(comercial_bank(key,value))

        for key,value in App.investment_banks_db.items():
            self.banks.append(investment_bank(key,value))

        #Take all the account that the user has
        for bank in self.banks:
            accounts=bank.return_accounts(self.client.CNP)
            if accounts!=None:
                self.client.accounts+=accounts
    
    #An internal method that helps us describe all the banks 
    def show_all_banks(self):
        for bank in self.banks:
            bank.describe_bank()

    #An internal method that help us describe all the comercial banks
    def show_comercial(self):
        for bank in self.banks:
            if isinstance(bank,comercial_bank):
                bank.describe_bank()

    #An internal method that helps us describe all the investment banks
    def show_investment(self):
        for bank in self.banks:
            if isinstance(bank,investment_bank):
                bank.describe_bank()

    #An internal method that helps us to open an account
    def open_account(self,index,balance):
        new_account=self.banks[index].open_account(self.client.first_name,self.client.last_name,self.client.phone_number,self.client.email,self.client.CNP,balance)
        self.client.accounts.append(new_account)

    #An internal method that helps us to close an account
    def close_account(self,index,account):
        return self.banks[index].close_account(account)

    #An internal method that helps us show if the bank has the minimum necessary
    def calculateMinimumCapitalOfBank(self,bank):
        if bank.calculateMinimumCapital()==True:
            print("The bank has the minimum capital required.")
        else:
            print("The bank doesn't have the minimum capital required.")

    #An internal method that helps us to show if the bank is solvent
    def CheckSolvencyOfBank(self,bank):
        if bank.CheckSolvency()==True:
            print("The bank has the minimum capital required in order to be solvent.")
        else:
            print("The bank doesn't have the minimum capital required in order to be solvent.")

    #An internal method that helps us see if the bank is regulated
    def isRegulationCompliant(self,bank):
        if bank.isRegulationCompliant()==True:
            print("The bank is legal with all the regulations.")
        else:
            print("The bank is not legal with all the regulations.")

    #An internal method that helps us get a loan
    def get_loan(self,bank,account,sum):
        bank.grant_loan(account,sum)

    #An internal method that helps us deposit money
    def deposit_money(self,bank,account,sum):
        bank.deposit_money(account,sum)

    #An internal method that helps us take out some money
    def take_money(self,bank,account,sum):
        bank.take_money(account,sum)

    #An internal method that helps us invest in a stock
    def invest(self,bank,account,quantity,price_per_stock,stock_name):
        bank.invest(account,quantity,price_per_stock,stock_name)

    #An internal method that helps us sell a stock
    def sell(self,bank,account,id,current_price):
        bank.sell(account,id,current_price)

    #The method that runs out whole app
    def run(self):
        print("Now that you have completed we can start:")
        print()
        number=0
        
        #Run it untill the user wants to stop it. Print all the options every time.
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

            #Take the input
            number=int(input("Your number is: "))

            #Make sure that the input is corrent
            while number<1 or number>16:
                print("The number has to be between 1 and 15. Introduce another number.")
                number=int(input("Your number is: "))

            #If the input is 1 show all the banks
            if number==1:
                self.show_all_banks()
            #If the input is 2 show all the comercial banks
            elif number==2:
                self.show_comercial()
            #If the input is 3 show all the investment banks
            elif number==3:
                self.show_investment()
            #If the input is 4 open an account
            elif number==4:
                #Choose the type of bank where you want to open the account
                print("Introduce 1 for comercial and 2 for investment.")
                choose_type_of_bank=int(input("Your number is: "))

                #Make sure that the input is corect
                while choose_type_of_bank<1 or choose_type_of_bank>2:
                    print("The number has to be either 1 or 2. Choose a goon number.")
                    choose_type_of_bank=int(input("Yout number is: "))
                
                #Treats the case where the bank is comercial, where you choose the bank and introduce the balance
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
                #Treats the case where the bank is investment, where you choose the bank and introduce the balance
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
            #If the input is 5 close an account 
            elif number==5:
                #Check to see if the client has any account
                if len(self.client.accounts)==0:
                    print("You don't have any account.")
                else:
                    #Print all the accounts
                    self.client.show_accounts()

                    #Choose an account
                    print(f"Choose a number from 1 to {len(self.client.accounts)} that reprezents your account.")
                    index=int(input("Your number: "))

                    #Make sure that the input is corect
                    while index<1 or index>len(self.client.accounts):
                        print(f"The number choosen doesn't convine to the rules. It has to be a number from 1 to {len(self.client.accounts)}")
                        index=int(input("Your number: "))
                    
                    #Delete the account depending on the bank
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

                    #Here we use that parameter that show us if the account was deleted, and if it is True, then we also delete it locally
                    if can_be_closed==True:
                        self.client.accounts.pop(index-1)
            #If the input is 6 it prints if the bank has the minimum capital
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
            #If the input is 7 print if the bank is solvent
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
            #If the input is 8 print if the bank is regulation compliant
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
            #If the input is 9 get a loan
            elif number==9:
                #Print all the comercial banks and get their index
                account_index=[]
                for i in range(len(self.client.accounts)):
                    if self.client.accounts[i].bank_name=='Banca Transilvania' or self.client.accounts[i].bank_name=='ING' or self.client.accounts[i].bank_name=='BCR':
                        account_index.append(i)
                        self.client.accounts[i].describe_account()

                #Check the case where you don't have any account
                if len(account_index)==0:
                    print("You don't have any account to a comercial bank. Open one in order to get a loan.")
                else:
                    #Choose the account
                    print(f"Choose a number from 1 to {len(account_index)} that represents the account to choose for the loan.")

                    index=int(input("Your number is: "))

                    #Make sure that the input is corect
                    while index<1 or index>len(account_index):
                        print(f"Your number has to be between 1 and {len(account_index)}")
                        index=int(input("Your number is: "))
                    
                    sum=float(input("The sum of money that you want to borrow is: "))

                    #Call for the internal method
                    if self.client.accounts[account_index[index-1]].bank_name=='Banca Transilvania':
                        self.get_loan(self.banks[0],self.client.accounts[account_index[index-1]],sum)
                    elif self.client.accounts[account_index[index-1]].bank_name=='ING':
                        self.get_loan(self.banks[1],self.client.accounts[account_index[index-1]],sum)
                    elif self.client.accounts[account_index[index-1]].bank_name=='BCR':
                        self.get_loan(self.banks[2],self.client.accounts[account_index[index-1]],sum)
            #If the input is 10 deposit money
            elif number==10:
                #Print all the banks and get their index
                account_index=[]
                for i in range(len(self.client.accounts)):
                    if self.client.accounts[i].bank_name=='Banca Transilvania' or self.client.accounts[i].bank_name=='ING' or self.client.accounts[i].bank_name=='BCR':
                        account_index.append(i)
                        self.client.accounts[i].describe_account()

                #Check to see if you have any account
                if len(account_index)==0:
                    print("You don't have any account to a comercial bank. Open one in order to deposit money.")
                else:
                    #Choose an account
                    print(f"Choose a number from 1 to {len(account_index)} that represents the account to choose for depositing the money.")

                    index=int(input("Your number is: "))

                    #Make sure that the input is corect
                    while index<1 or index>len(account_index):
                        print(f"Your number has to be between 1 and {len(account_index)}")
                        index=int(input("Your number is: "))
                    
                    sum=float(input("The sum of money that you want to deposit is: "))

                    #Call for the internal method
                    if self.client.accounts[account_index[index-1]].bank_name=='Banca Transilvania':
                        self.deposit_money(self.banks[0],self.client.accounts[account_index[index-1]],sum)
                    elif self.client.accounts[account_index[index-1]].bank_name=='ING':
                        self.deposit_money(self.banks[1],self.client.accounts[account_index[index-1]],sum)
                    elif self.client.accounts[account_index[index-1]].bank_name=='BCR':
                        self.deposit_money(self.banks[2],self.client.accounts[account_index[index-1]],sum)
            #If the input is 11 take out some money
            elif number==11:
                #Print all the comercial banks and get their index
                account_index=[]
                for i in range(len(self.client.accounts)):
                    if self.client.accounts[i].bank_name=='Banca Transilvania' or self.client.accounts[i].bank_name=='ING' or self.client.accounts[i].bank_name=='BCR':
                        account_index.append(i)
                        self.client.accounts[i].describe_account()

                #Check to see if there the client has any account
                if len(account_index)==0:
                    print("You don't have any account to a comercial bank.")
                else:
                    #Choose an account
                    print(f"Choose a number from 1 to {len(account_index)} that represents the account to choose for taking out some money.")

                    index=int(input("Your number is: "))

                    #Make sure that the input is corent
                    while index<1 or index>len(account_index):
                        print(f"Your number has to be between 1 and {len(account_index)}")
                        index=int(input("Your number is: "))
                    
                    sum=float(input("The sum of money that you want to take out: "))

                    #Call for the internal method
                    if self.client.accounts[account_index[index-1]].bank_name=='Banca Transilvania':
                        self.take_money(self.banks[0],self.client.accounts[account_index[index-1]],sum)
                    elif self.client.accounts[account_index[index-1]].bank_name=='ING':
                        self.take_money(self.banks[1],self.client.accounts[account_index[index-1]],sum)
                    elif self.client.accounts[account_index[index-1]].bank_name=='BCR':
                        self.take_money(self.banks[2],self.client.accounts[account_index[index-1]],sum)
            #If the input is 12 show the price of a stock
            elif number==12:
                #The stock available
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

                #Print all the choices and choose one
                i=1
                for key in stock_map.keys():
                    print(str(i)+". "+key)
                    i+=1

                print("Choose the name that reprezents the stock where you want to see the price.")

                stock_name=input("The name is: ")

                #Make sure that the input is corect
                while stock_name not in stock_map.keys():
                    print("The name introduces is not acurate. Introduce it again and do is as shown.")
                    stock_name=input("The name is: ")

                #Get the price and print it
                price=investment_bank.show_investments_oportunities(stock_map[stock_name])

                print(f"The price of the stock choosen if {price}")

            #If the input is 13 invest in a stock
            elif number==13:
                #Print all the investment banks and get their index
                account_index=[]
                for i in range(len(self.client.accounts)):
                    if self.client.accounts[i].bank_name=='Investment Center' or self.client.accounts[i].bank_name=='Neo Invest' or self.client.accounts[i].bank_name=='Investment Group':
                        account_index.append(i)
                        self.client.accounts[i].describe_account()

                #Treat the case where the client doesn't have any account
                if len(account_index)==0:
                    print("You don't have any account to an investment bank.")
                else:
                    #Choose an account
                    print(f"Choose a number from 1 to {len(account_index)} that represents the account to choose for buying stock.")

                    index=int(input("Your number is: "))

                    #Make sure that the input is corect
                    while index<1 or index>len(account_index):
                        print(f"Your number has to be between 1 and {len(account_index)}")
                        index=int(input("Your number is: "))

                    #The stock available
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

                    #Print the stock and choose one
                    i=1
                    for key in stock_map.keys():
                        print(str(i)+". "+key)
                        i+=1

                    print("Choose the name that reprezents the stock that you want to buy.")

                    stock_name=input("The name is: ")

                    #Make sure the input is corect
                    while stock_name not in stock_map.keys():
                        print("The name introduces is not acurate. Introduce it again and do is as shown.")
                        stock_name=input("The name is: ")

                    #Get the quantity(it has to be an int)
                    print("Choose the quantity")
                    quantity=int(input("Guantity: "))

                    #Get the current price of the stock
                    price=investment_bank.show_investments_oportunities(stock_map[stock_name])

                    #Call for the internal method
                    if self.client.accounts[account_index[index-1]].bank_name=='Investment Center':
                        self.invest(self.banks[3],self.client.accounts[account_index[index-1]],quantity,price,stock_name)
                    elif self.client.accounts[account_index[index-1]].bank_name=='Neo Invest':
                        self.invest(self.banks[4],self.client.accounts[account_index[index-1]],quantity,price,stock_name)
                    elif self.client.accounts[account_index[index-1]].bank_name=='Investment Group':
                        self.invest(self.banks[5],self.client.accounts[account_index[index-1]],quantity,price,stock_name)
            #If the input is 14 sell a stock
            elif number==14:
                #Print the investment banks and get their index
                account_index=[]
                for i in range(len(self.client.accounts)):
                    if self.client.accounts[i].bank_name=='Investment Center' or self.client.accounts[i].bank_name=='Neo Invest' or self.client.accounts[i].bank_name=='Investment Group':
                        account_index.append(i)
                        self.client.accounts[i].describe_account()

                #Treat the case where the clinet doesn't have an account
                if len(account_index)==0:
                    print("You don't have any account to an investment bank.")
                else:
                    #Choose an account
                    print(f"Choose a number from 1 to {len(account_index)} that represents the account to choose for buying stock.")

                    index=int(input("Your number is: "))

                    #Make sure that the input is corect
                    while index<1 or index>len(account_index):
                        print(f"Your number has to be between 1 and {len(account_index)}")
                        index=int(input("Your number is: "))

                    #The stocks available
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

                    #Get the ids and the name of the companies of the stocks from the db, that the client ows in the chosen account
                    ids_and_company_name=None
                    if self.client.accounts[account_index[index-1]].bank_name=='Investment Center':
                        ids_and_company_name=self.banks[3].show_investments_and_return_ids_and_company(self.client.accounts[account_index[index-1]])
                    elif self.client.accounts[account_index[index-1]].bank_name=='Neo Invest':
                        ids_and_company_name=self.banks[4].show_investments_and_return_ids_and_company(self.client.accounts[account_index[index-1]])
                    elif self.client.accounts[account_index[index-1]].bank_name=='Investment Group':
                        ids_and_company_name=self.banks[5].show_investments_and_return_ids_and_company(self.client.accounts[account_index[index-1]])
                    
                    #Check to see if there is any stock
                    if len(ids_and_company_name)==0:
                        print("You don't have any stock on this account.")
                    else:
                        #Choose the stock to sell
                        print(f"Choose a number from 1 to {len(ids_and_company_name)}.")
                        id_number=int(input("Your number is: "))

                        #Make sure that the input is corect
                        while id_number<1 or id_number>len(ids_and_company_name):
                            print(f"The number has to be between 1 and {len(ids_and_company_name)}")
                            id_number=int(input("Your number is: "))
                        
                        #Get the curent price 
                        current_price=investment_bank.show_investments_oportunities(stock_map[ids_and_company_name[id_number-1][1]])

                        #Call for the internal method
                        if self.client.accounts[account_index[index-1]].bank_name=='Investment Center':
                            self.sell(self.banks[3],self.client.accounts[account_index[index-1]],ids_and_company_name[id_number-1][0],current_price)
                        elif self.client.accounts[account_index[index-1]].bank_name=='Neo Invest':
                            self.sell(self.banks[4],self.client.accounts[account_index[index-1]],ids_and_company_name[id_number-1][0],current_price)
                        elif self.client.accounts[account_index[index-1]].bank_name=='Investment Group':
                            self.sell(self.banks[5],self.client.accounts[account_index[index-1]],ids_and_company_name[id_number-1][0],current_price)

            #If the input is 15, print all the account that the client owns
            elif number==15:
                self.client.show_accounts()