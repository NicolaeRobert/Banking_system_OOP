from .BCE import BCE
from .account import account
from .utils import get_connection
from decimal import Decimal
import requests
import os

class investment_bank(BCE):
    def __init__(self,name,db_name):
        self.name=name
        self.db_name=db_name
        self.bank_capital=50000
        self.accounts=[]

        conn=get_connection(self.db_name)
        mycursor=conn.cursor()

        mycursor.execute(
            "SELECT * FROM accounts"
        )

        accounts_info=mycursor.fetchall()

        if accounts_info!=None:
            for account_info in accounts_info:
                self.accounts.append(
                    account(account_info[0],account_info[1],account_info[2],account_info[3],account_info[4],account_info[5],account_info[6],self.name)
                )

        mycursor.close()
        conn.close()


    def open_account(self,first_name,last_name,phone_number,email,CNP,balance):
        conn=get_connection(self.db_name)

        mycursor=conn.cursor()

        mycursor.execute(
            "INSERT INTO accounts (first_name,last_name,phone_number,email,CNP,balance) VALUES (%s,%s,%s,%s,%s,%s)",
            (first_name,last_name,phone_number,email,CNP,balance)
        )
        conn.commit()

        id=mycursor.lastrowid

        mycursor.close()
        conn.close()

        self.accounts.append(account(id,first_name,last_name,phone_number,email,CNP,balance,self.name))

        return self.accounts[-1]

    def close_account(self,account):

        can_be_closed=True
        
        conn=get_connection(self.db_name)
        mycursor=conn.cursor()

        mycursor.execute(
            "SELECT * FROM TRADES WHERE user_id=%s",
            (account.id,)
        )

        result=mycursor.fetchall()

        if result:
            print("We can't close your account. Sell the rest of the stock in order to be able to close the account!")
            can_be_closed=False
        else:
            mycursor.execute(
                "DELETE FROM ACCOUNTS WHERE id=%s",
                (account.id,)
            )

            conn.commit()

            self.accounts=[acc for acc in self.accounts if acc.id != account.id]
            
        mycursor.close()
        conn.close()

        return can_be_closed

    def calculateMinimumCapital(self):
        if self.bank_capital>=50000:
            return True
        return False

    def checkSolvency(self):
        if self.bank_capital>=50000:
            return True
        return False
    
    def isRegulationCompliant(self):
        if self.calculateMinimumCapital() and self.checkSolvency():
            return True
        return False

    def invest(self, account, quantity, price_per_stock, stock_name):

        conn=get_connection(self.db_name)
        mycursor=conn.cursor()

        total=quantity*price_per_stock

        if account.balance<total:
            print("You don't have enough money.")
        else:
            mycursor.execute(
                "INSERT INTO TRADES (user_id,company,quantity, total) VALUES (%s,%s,%s,%s)",
                (account.id, stock_name, quantity, price_per_stock*quantity)
            )

            mycursor.execute(
                "UPDATE ACCOUNTS SET balance=%s WHERE id=%s",
                (account.balance-Decimal(str(total)),account.id)
            )

            conn.commit()

            account.balance-=Decimal(str(total))

        mycursor.close()
        conn.close()

    def sell(self, account, id, current_price):#The id of the stock
        
        conn=get_connection(self.db_name)
        mycursor=conn.cursor()

        mycursor.execute(
            "SELECT quantity FROM TRADES WHERE id=%s",
            (id,)
        )

        quantity=mycursor.fetchone()
        total=Decimal(str(quantity[0]*current_price))
        account.balance+=total

        mycursor.execute(
            "UPDATE ACCOUNTS SET balance=%s WHERE id=%s",
            (account.balance,account.id)
        )

        mycursor.execute(
            "DELETE FROM TRADES WHERE id=%s",
            (id,)
        )

        conn.commit()

        mycursor.close()
        conn.close()

    def show_investments_and_return_ids_and_company(self, account):

        conn=get_connection(self.db_name)
        mycursor=conn.cursor()

        mycursor.execute(
            "SELECT * FROM trades WHERE user_id=%s",
            (account.id,)
        )

        investments=mycursor.fetchall()
        list_of_ids=[]

        if investments!=None:
            print("The stock that you own:")

        number=1
        for investment in investments:
            list_of_ids.append([investment[0],investment[2]])
            print(str(number)+'. '+f"ID:{investment[0]}  COMPANY:{investment[2]}  QUANTITY:{investment[3]}  TOTAL:{investment[4]}")
            number+=1
        
        return list_of_ids
    
    def return_accounts(self,CNP):
        accounts_to_return=[]

        for account in self.accounts:
            if account.CNP==CNP:
                accounts_to_return.append(account)
        
        if len(accounts_to_return)==0:
            return None
        return accounts_to_return
    
    def describe_bank(self):
        print(f"The bank {self.name} is an investment bank.")

    @classmethod
    def show_investments_oportunities(cls,stock_name):
        url=f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stock_name}&apikey={os.getenv('api_key')}"
        response=requests.get(url).json()

        return float(response['Global Quote']['05. price'])
