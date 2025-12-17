from abc import ABC, abstractmethod

class BCE(ABC):
    @abstractmethod
    def open_account():
        pass

    @abstractmethod
    def close_account():
        pass

    @abstractmethod
    def calculateMinimumCapital():
        pass

    @abstractmethod
    def checkSolvency():
        pass
    
    @abstractmethod
    def isRegulationCompliant():
        pass