from .BCE import BCE
from .account import account
from .utils import get_connection
import os
from decimal import Decimal

#The class that defines the comercial bank
class comercial_bank(BCE):
    #The constrictor that receives the name of the bank and the name of the database
    def __init__(self,name,db_name):
        #Sets all the parameters accordingly
        self.name=name
        self.db_name=db_name
        self.total_balance=Decimal("1000000")
        self.deposited_money=0
        self.accounts=[]

        #Get the connection and the cursor for the database
        conn=get_connection(self.db_name)
        mycursor=conn.cursor()

        #Select all the accounts that the bank hold and store them in accounts_info
        mycursor.execute(
            "SELECT * FROM accounts"
        )

        accounts_info=mycursor.fetchall()

        #Check if the bank has any account, and if it has we also set them here, to also have them present here 
        if accounts_info!=None:
            for account_info in accounts_info:
                self.accounts.append(
                    account(account_info[0],account_info[1],account_info[2],account_info[3],account_info[4],account_info[5],account_info[6],self.name)
                )
                #As a comercial bank, we also use the client money for loans and other things, so increase the 2 variables from below
                self.total_balance+=account_info[6]
                self.deposited_money+=account_info[6]
        
        #Close the cursor and the connection
        mycursor.close()
        conn.close()

    #The method to open an account
    def open_account(self,first_name,last_name,phone_number,email,CNP,balance):
        #Get the conection and the cursor for the database
        conn=get_connection(self.db_name)
        mycursor=conn.cursor()

        #Create the account in the database
        mycursor.execute(
            "INSERT INTO accounts (first_name,last_name,phone_number,email,CNP,balance) VALUES (%s,%s,%s,%s,%s,%s)",
            (first_name,last_name,phone_number,email,CNP,balance)
        )
        conn.commit()

        #Increase the 2 variables with balance
        self.total_balance+=Decimal(str(balance))
        self.deposited_money+=Decimal(str(balance))

        #Get the id of the account created in the database, close the connection and cursor with the database and also create the account here, using the account class
        id=mycursor.lastrowid

        mycursor.close()
        conn.close()

        self.accounts.append(account(id,first_name,last_name,phone_number,email,CNP,balance,self.name))

        #Return the account created to add it to the client created
        return self.accounts[-1]

    #The method to close an account
    def close_account(self,account):
        
        #A variable that we use when running the app, that sais if an account can be or not closed
        can_be_closed=True

        #Get the connection and the cursor to the database
        conn=get_connection(self.db_name)
        mycursor=conn.cursor()

        #See if there still are loans in the database, otherwise the account can't be closed
        mycursor.execute(
            "SELECT * FROM loans WHERE user_id=%s",
            (account.id,)
        )
        still_has_loans=mycursor.fetchone()

        #Check if the account has loans, case in witch we can't close the account
        if still_has_loans!=None:
            #Print a message to warn the user and set the variable to False
            print("Can't close the account! You still have loans active!")
            can_be_closed=False
        else:
            #Close the account in the db
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

            #Decrease the balance of the account closed 
            self.total_balance-=balance[0]
            self.deposited_money-=balance[0]

            #Also delete it here locally
            self.accounts=[acc for acc in self.accounts if acc.id != account.id]
        
        #Close the connection and the cursor to the database
        mycursor.close()
        conn.close()

        #Return the variable that tells me if the account has been deleted or not
        return can_be_closed

    #The method that calculate if the bank has the minimum capital
    def calculateMinimumCapital(self):
        #Here I set that the minimum capital for a bank should be 100000
        if self.total_balance>=100000:
            return True
        return False

    #The method that checks if a bank is solvent
    def checkSolvency(self):
        #A bank is solvent if the total balance of the bank is more or equal with the money deposited
        if self.total_balance>=self.deposited_money:
            return True
        return False
    
    #The method that checks if the bank is regulated
    def isRegulationCompliant(self):
        #A bank is regulated if it has the minimum capital and if it is solvent
        if self.calculateMinimumCapital() and self.checkSolvency():
            return True
        return False

    #Here we have the methos that grants the loan
    def grant_loan(self, account, sum):
        #I set that the maximum loan that a person can have is 50000
        if sum<=50000:

            #Get the connection and the cursot to the database
            conn=get_connection(self.db_name)
            mycursor=conn.cursor()

            #Create a loan in the databse
            mycursor.execute(
                "INSERT INTO loans (user_id,sum) VALUES (%s,%s)",
                (account.id,sum)
            )

            #Update the balance locally
            account.balance+=Decimal(str(sum))

            #Update the balance in the database
            mycursor.execute(
                "UPDATE ACCOUNTS SET BALANCE=%s WHERE id=%s",
                (account.balance,account.id)
            )
            
            #Commit the connection and close the connection and the cursor
            conn.commit()

            mycursor.close()
            conn.close()

        #Print a message if the sum that the client wants to borrow is too big 
        else:
            print("Can't provide such a big loan")

    #The method that allows us to deposit money
    def deposit_money(self, account, sum):
        #Adds the sum to the balance of the account and to the bank 
        account.balance+=Decimal(str(sum))
        self.total_balance+=Decimal(str(sum))
        self.deposited_money+=Decimal(str(sum))

        #Get the connection and the cursor
        conn=get_connection(self.db_name)
        mycursor=conn.cursor()

        #Updates the database with the corect balance of the user
        mycursor.execute(
            "UPDATE ACCOUNTS SET BALANCE=%s WHERE id=%s",
            (account.balance,account.id)
        )
        
        #Commmits the connection and closes the connection and the cursor
        conn.commit()

        mycursor.close()
        conn.close()

    #The method to take out a sum of money
    def take_money(self, account, sum):
        #Test to see if the account has that sum available
        if account.balance>=sum:
            #Decrese the sum from everywhere
            self.total_balance-=Decimal(str(sum))
            self.deposited_money-=Decimal(str(sum))
            account.balance-=Decimal(str(sum))

            #Get the connection and the cursor
            conn=get_connection(self.db_name)
            mycursor=conn.cursor()

            #Update the database
            mycursor.execute(
                "UPDATE ACCOUNTS SET BALANCE=%s WHERE id=%s",
                (account.balance,account.id)
            )
            
            #Commmits the connection and closes the connection and the cursor
            conn.commit()

            mycursor.close()
            conn.close()

        #If the sum is bigger than the balance say a message of warning
        else:
            print("Insuficient fonds")
    
    #The method that helps us to get the accounts of the user from a comercial bank object
    def return_accounts(self,CNP):
        accounts_to_return=[]

        for account in self.accounts:
            if account.CNP==CNP:
                accounts_to_return.append(account)
        
        if len(accounts_to_return)==0:
            return None
        return accounts_to_return
    
    #The method that describes a comercial bank object
    def describe_bank(self):
        print(f"The bank {self.name} is a comercial bank.")