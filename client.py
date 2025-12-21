class client:
    def __init__(self,first_name,last_name,phone_number,email,CNP):
        self.first_name=first_name
        self.last_name=last_name
        self.phone_number=phone_number
        self.email=email
        self.CNP=CNP
        self.accounts=[]

    def show_accounts(self):
        if len(self.accounts)==0:
            print("You don't have any account.")
        else:
            for account in self.accounts:
                account.describe_account()