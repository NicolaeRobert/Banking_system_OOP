from BCE import BCE
from account import account
from utils import get_connection
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
            "INSER INTO accounts (first_name,last_name,phone_number,email,CNP,balance) VALUES (%s,%s,%s,%s,%s,%s)",
            (first_name,last_name,phone_number,email,CNP,balance)
        )
        conn.commit()

        id=mycursor.lastrowid

        mycursor.close()
        conn.close()

        self.accounts.append(account(id,first_name,last_name,phone_number,email,CNP,balance,self.name))

    def close_account(self,id):
        
        conn=get_connection(self.db_name)
        mycursor=conn.cursor()

        mycursor.execute(
            "SELECT * FROM TRADES WHERE user_id=%s",
            (id,)
        )

        result=mycursor.fetchall()

        if result!=None:
            print("We can't close your account. Sell the rest of the stock in order to be able to close the account!")
        else:
            mycursor.execute(
                "DELETE FROM ACCOUNTS WHERE id=%s",
                (id,)
            )

            conn.commit()

            for index in range(len(self.accounts)):
                if self.accounts[index].id==id:
                    self.accounts.pop(index)
                    break
            
        mycursor.close()
        conn.close()

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

    def show_invesments_oportunities(self, stock_name):
        url=f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stock_name}&apikey={os.getenv('api_key')}"
        response=requests.get(url).json()

        return response['Global Quote']['05. price']

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
                "UPDATE ON ACCOUNTS SET balance=%s WHERE id=%s",
                (account.balance-total,account.id)
            )

            conn.commit()

            account.balance-=total

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

        account.balace+=quantity[0]*current_price

        mycursor.execute(
            "UPDATE ON ACCOUNTS SET balance=%s WHERE id=%s",
            (quantity*current_price,account.id)
        )

        mycursor.execute(
            "DELETE FROM TRADES WHERE id=%s",
            (id,)
        )

        conn.commit()

        mycursor.close()
        conn.close()

    def show_invesments_and_return_ids(self, account):

        conn=get_connection(self.db_name)
        mycursor=conn.cursor()

        mycursor.execute(
            "SELECT * FROM trades WHERE user_id=%s",
            (account.id,)
        )

        investments=mycursor.fetchall()
        list_of_ids=[]

        for investment in investments:
            list_of_ids.append(investment[0])
            print(f"ID:{investment[0]}  COMPANY:{investment[2]}  QUANTITY:{investment[3]}  TOTAL:{investment[4]}")
        
        return list_of_ids
