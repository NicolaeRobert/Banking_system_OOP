from BCE import BCE
from account import account
from loan import loan
from datetime import datetime
from utils import get_connection
import os

class comercial_bank(BCE):
    def __init__(self,name,db_name):
        self.name=name
        self.db_name=db_name
        self.total_balance=1000000
        self.deposited_money=0
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
            "DELETE FROM accounts WHERE id=%s",
            (id,)
        )
        conn.commit()

        mycursor.close()
        conn.close()

        for index in range(self.accounts):
            if self.accounts[index].id==id:
                self.accounts.pop(index)

    def calculateMinimumCapital(self):
        if self.total_balance==100000:
            return True
        return False

    def checkSolvency(self):
        if self.total_balance>=self.deposited_money:
            return True
        return False
    
    def isRegulationCompliant(self):
        if self.calculateMinimumCapital() and self.checkSolvency():
            return True
        return False

    def grant_loan(self, account, sum, years):
        if sum<=50000:
            account.money_borrowed.append(loan(self.name, sum, datetime.today().date(), years))
        else:
            print("Can't provide such a big loan")

    def deposit_money(self, account, sum):
        account.balace+=sum

    def take_money(self, account, sum):
        if account.balance>=sum:
            account.balance-=sum
        else:
            print("Insuficient fonds")