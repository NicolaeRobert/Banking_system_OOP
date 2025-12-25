from abc import ABC, abstractmethod

#The class that defines the mandatory methods for any type of bank(Abstract class)
class BCE(ABC):
    #The method to open an account
    @abstractmethod
    def open_account(self):
        pass

    #The method to close an account
    @abstractmethod
    def close_account(self):
        pass

    #The method to calculate if the bank has the minimum capital necessary
    @abstractmethod
    def calculateMinimumCapital(self):
        pass

    #The method to check if the bank is solvent
    @abstractmethod
    def checkSolvency(self):
        pass
    
    #The method to see if the bank is compliant with all the regulations
    @abstractmethod
    def isRegulationCompliant(self):
        pass