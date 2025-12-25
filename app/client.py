#The class client that creates the client and hold the informations about him/her and all the accounts that he holds
class client:
    #The constructor that sets all the parameters
    def __init__(self,first_name,last_name,phone_number,email,CNP):
        self.first_name=first_name
        self.last_name=last_name
        self.phone_number=phone_number
        self.email=email
        self.CNP=CNP
        self.accounts=[]

    #The method that shows the description for all the accounts
    def show_accounts(self):
        for account in self.accounts:
            account.describe_account()