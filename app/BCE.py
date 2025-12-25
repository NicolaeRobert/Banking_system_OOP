from abc import ABC, abstractmethod

class BCE(ABC):
    @abstractmethod
    def open_account(self):
        pass

    @abstractmethod
    def close_account(self):
        pass

    @abstractmethod
    def calculateMinimumCapital(self):
        pass

    @abstractmethod
    def checkSolvency(self):
        pass
    
    @abstractmethod
    def isRegulationCompliant(self):
        pass