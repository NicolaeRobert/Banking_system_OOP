from .BCE import BCE
from .account import account
from .utils import get_connection
import os
from decimal import Decimal

class comercial_bank(BCE):
    def __init__(self,name,db_name):
        self.name=name
        self.db_name=db_name
        self.total_balance=Decimal("1000000")
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
                self.total_balance+=account_info[6]
                self.deposited_money+=account_info[6]
        
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

        self.total_balance+=Decimal(str(balance))
        self.deposited_money+=Decimal(str(balance))

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
            "SELECT * FROM loans WHERE user_id=%s",
            (account.id,)
        )
        still_has_loans=mycursor.fetchone()

        if still_has_loans!=None:
            print("Can't close the account! You still have loans active!")
            can_be_closed=False
        else:
            mycursor.execute(
                "SELECT balance FROM accounts WHERE id=%s",
                (account.id,)
            )
            balance=mycursor.fetchone()

            mycursor.execute(
                "DELETE FROM accounts WHERE id=%s",
                (account.id,)
            )
            conn.commit()

            self.total_balance-=balance[0]
            self.deposited_money-=balance[0]

            self.accounts=[acc for acc in self.accounts if acc.id != account.id]
        
        mycursor.close()
        conn.close()

        return can_be_closed

    def calculateMinimumCapital(self):
        if self.total_balance>=100000:
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

    def grant_loan(self, account, sum):
        if sum<=50000:

            conn=get_connection(self.db_name)
            mycursor=conn.cursor()

            mycursor.execute(
                "INSERT INTO loans (user_id,sum) VALUES (%s,%s)",
                (account.id,sum)
            )

            account.balance+=Decimal(str(sum))

            mycursor.execute(
                "UPDATE ACCOUNTS SET BALANCE=%s WHERE id=%s",
                (account.balance,account.id)
            )
            
            conn.commit()

            mycursor.close()
            conn.close()
            
        else:
            print("Can't provide such a big loan")

    def deposit_money(self, account, sum):
        account.balance+=Decimal(str(sum))
        self.total_balance+=Decimal(str(sum))
        self.deposited_money+=Decimal(str(sum))

        conn=get_connection(self.db_name)
        mycursor=conn.cursor()

        mycursor.execute(
            "UPDATE ACCOUNTS SET BALANCE=%s WHERE id=%s",
            (account.balance,account.id)
        )
        
        conn.commit()

        mycursor.close()
        conn.close()

    def take_money(self, account, sum):
        if account.balance>=sum:
            self.total_balance-=Decimal(str(sum))
            self.deposited_money-=Decimal(str(sum))

            account.balance-=Decimal(str(sum))

            conn=get_connection(self.db_name)
            mycursor=conn.cursor()

            mycursor.execute(
                "UPDATE ACCOUNTS SET BALANCE=%s WHERE id=%s",
                (account.balance,account.id)
            )
            
            conn.commit()

            mycursor.close()
            conn.close()

        else:
            print("Insuficient fonds")
    
    def return_accounts(self,CNP):
        accounts_to_return=[]

        for account in self.accounts:
            if account.CNP==CNP:
                accounts_to_return.append(account)
        
        if len(accounts_to_return)==0:
            return None
        return accounts_to_return
    
    def describe_bank(self):
        print(f"The bank {self.name} is a comercial bank.")