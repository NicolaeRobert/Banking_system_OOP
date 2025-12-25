from .BCE import BCE
from .account import account
from .utils import get_connection
from decimal import Decimal
import requests
import os

#The class that defines the investment bank
class investment_bank(BCE):
    #The constructor
    def __init__(self,name,db_name):
        self.name=name
        self.db_name=db_name
        self.bank_capital=50000
        self.accounts=[]

        #Get the connection and the cursor to the database
        conn=get_connection(self.db_name)
        mycursor=conn.cursor()

        #Select all the accounts from the db
        mycursor.execute(
            "SELECT * FROM accounts"
        )

        accounts_info=mycursor.fetchall()

        #Create the accounts objects here
        if accounts_info!=None:
            for account_info in accounts_info:
                self.accounts.append(
                    account(account_info[0],account_info[1],account_info[2],account_info[3],account_info[4],account_info[5],account_info[6],self.name)
                )

        #Close the connection and the cursor to the db
        mycursor.close()
        conn.close()

    #The method that allows us to open an account
    def open_account(self,first_name,last_name,phone_number,email,CNP,balance):

        #Get the connection and the cursor
        conn=get_connection(self.db_name)
        mycursor=conn.cursor()

        #Insert into db the new account and commit
        mycursor.execute(
            "INSERT INTO accounts (first_name,last_name,phone_number,email,CNP,balance) VALUES (%s,%s,%s,%s,%s,%s)",
            (first_name,last_name,phone_number,email,CNP,balance)
        )
        conn.commit()

        id=mycursor.lastrowid

        #Close the connection and the cursor to the db
        mycursor.close()
        conn.close()

        #Create the account object and return it
        self.accounts.append(account(id,first_name,last_name,phone_number,email,CNP,balance,self.name))

        return self.accounts[-1]

    #The method that allows for closing an account
    def close_account(self,account):

        #A variable that we use when running the app, that sais if an account can be or not closed
        can_be_closed=True
        
        #Get the connection and the cursor
        conn=get_connection(self.db_name)
        mycursor=conn.cursor()

        #Get all the trades that aren't closed yet
        mycursor.execute(
            "SELECT * FROM TRADES WHERE user_id=%s",
            (account.id,)
        )

        result=mycursor.fetchall()

        #If there are any trades remained print an alert message
        if result:
            print("We can't close your account. Sell the rest of the stock in order to be able to close the account!")
            can_be_closed=False
        else:
            #Delete the account and commit
            mycursor.execute(
                "DELETE FROM ACCOUNTS WHERE id=%s",
                (account.id,)
            )

            conn.commit()

            #Save the changes made
            self.accounts=[acc for acc in self.accounts if acc.id != account.id]
            
        #Close the connection and the cursor
        mycursor.close()
        conn.close()

        #Return the variable that tells me if the account has been deleted or not
        return can_be_closed

    #The method that calculate if the bank has the minimum capital
    def calculateMinimumCapital(self):
        #Here I set that the minimum capital for a bank should be 50000
        if self.bank_capital>=50000:
            return True
        return False

    #The method that checks if a bank is solvent
    def checkSolvency(self):
        #Here I set that the minimum capital for a bank should be 50000
        if self.bank_capital>=50000:
            return True
        return False
    
    #The method that checks if the bank is regulated
    def isRegulationCompliant(self):
        #A bank is regulated if it has the minimum capital and if it is solvent
        if self.calculateMinimumCapital() and self.checkSolvency():
            return True
        return False

    #The method that allows us to invest
    def invest(self, account, quantity, price_per_stock, stock_name):

        #Get the connection and the cursor to the database
        conn=get_connection(self.db_name)
        mycursor=conn.cursor()

        #Calculate the final price for buying the quantity of the stock desired
        total=quantity*price_per_stock

        #If you don't have enough money you receive a warning message
        if account.balance<total:
            print("You don't have enough money.")
        else:
            #Insert into the database the investment
            mycursor.execute(
                "INSERT INTO TRADES (user_id,company,quantity, total) VALUES (%s,%s,%s,%s)",
                (account.id, stock_name, quantity, price_per_stock*quantity)
            )

            #Update the balance
            mycursor.execute(
                "UPDATE ACCOUNTS SET balance=%s WHERE id=%s",
                (account.balance-Decimal(str(total)),account.id)
            )

            #Commit and decrease the local balance
            conn.commit()

            account.balance-=Decimal(str(total))

        #Close the cursor and the connection
        mycursor.close()
        conn.close()

    #Here we have the method that allows us to sell a stock
    def sell(self, account, id, current_price):#The id of the stock
        
        #Get the connection and the cursor to the database
        conn=get_connection(self.db_name)
        mycursor=conn.cursor()

        #Select the quantity of that trade that you want to sell
        mycursor.execute(
            "SELECT quantity FROM TRADES WHERE id=%s",
            (id,)
        )

        #Calculate the total and add it to the local balance
        quantity=mycursor.fetchone()
        total=Decimal(str(quantity[0]*current_price))
        account.balance+=total

        #Update the balance in the database
        mycursor.execute(
            "UPDATE ACCOUNTS SET balance=%s WHERE id=%s",
            (account.balance,account.id)
        )

        #Delete the trade already sold
        mycursor.execute(
            "DELETE FROM TRADES WHERE id=%s",
            (id,)
        )

        #Commit the connection, close it along with the cursor
        conn.commit()

        mycursor.close()
        conn.close()

    #A method that shows the trades and return a list with the database id-s and the name of the company
    def show_investments_and_return_ids_and_company(self, account):

        #Get the connection and the cursor
        conn=get_connection(self.db_name)
        mycursor=conn.cursor()

        #Select all from the trades table that have the id of the user
        mycursor.execute(
            "SELECT * FROM trades WHERE user_id=%s",
            (account.id,)
        )

        investments=mycursor.fetchall()
        list_of_ids=[]

        #If there are investment print them
        if investments!=None:
            print("The stock that you own:")

        number=1
        for investment in investments:
            list_of_ids.append([investment[0],investment[2]])
            print(str(number)+'. '+f"ID:{investment[0]}  COMPANY:{investment[2]}  QUANTITY:{investment[3]}  TOTAL:{investment[4]}")
            number+=1
        
        #Return the list
        return list_of_ids
    
    #A method that return all the account of a user to an investment bank
    def return_accounts(self,CNP):
        accounts_to_return=[]

        for account in self.accounts:
            if account.CNP==CNP:
                accounts_to_return.append(account)
        
        if len(accounts_to_return)==0:
            return None
        return accounts_to_return
    
    #A method that describes the bank
    def describe_bank(self):
        print(f"The bank {self.name} is an investment bank.")

    #A class method that return the price of a stock
    @classmethod
    def show_investments_oportunities(cls,stock_name):
        #The url for the api call
        url=f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stock_name}&apikey={os.getenv('api_key')}"

        #Making the call and get a json response        
        response=requests.get(url).json()

        #Return the price of that stock
        return float(response['Global Quote']['05. price'])
