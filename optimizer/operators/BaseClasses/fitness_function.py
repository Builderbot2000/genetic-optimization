import abc

class FitnessFunction(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'evaluate') and 
        callable(subclass.evaluate) or NotImplemented)

    def __init__(self, optimizer):
        self.optimizer = optimizer

    @abc.abstractmethod
    def evaluate(self, state) -> dict:
        """Input state, output fitness score vector"""
        raise NotImplementedError