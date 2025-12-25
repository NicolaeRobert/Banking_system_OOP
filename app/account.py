from decimal import Decimal

#The class that defines an account
class account:
    #The constructor that takes all the necessary parameters and sets them
    def __init__(self,id,first_name,last_name,phone_number,email,CNP,balance,bank_name):
        self.id=id
        self.first_name=first_name
        self.last_name=last_name
        self.phone_number=phone_number
        self.email=email
        self.CNP=CNP
        self.balance=Decimal(str(balance))
        self.bank_name=bank_name

    #The method that describes an account
    def describe_account(self):
        print(f"ID:{self.id}  BALANCE:{self.balance}  BANK NAME:{self.bank_name}")