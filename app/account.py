from decimal import Decimal

class account:
    def __init__(self,id,first_name,last_name,phone_number,email,CNP,balance,bank_name):
        self.id=id
        self.first_name=first_name
        self.last_name=last_name
        self.phone_number=phone_number
        self.email=email
        self.CNP=CNP
        self.balance=Decimal(str(balance))
        self.bank_name=bank_name

    def describe_account(self):
        print(f"ID:{self.id}  BALANCE:{self.balance}  BANK NAME:{self.bank_name}")