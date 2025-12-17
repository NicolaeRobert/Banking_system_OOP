class account:
    def __init__(self,id,first_name,last_name,phone_number,email,CNP,balance,bank_name):
        self.id=id
        self.first_name=first_name
        self.last_name=last_name
        self.phone_number=phone_number
        self.email=email
        self.CNP=CNP
        self.money_borrowed=[]
        self.balance=balance
        self.bank_name=bank_name