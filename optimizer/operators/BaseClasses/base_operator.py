import abc

class BaseOperator(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'run') and 
        callable(subclass.run) or NotImplemented)

    @abc.abstractmethod
    def run(self, population: list) -> list:
        """Input population, output selected/generated/mutated population"""
        raise NotImplementedError

"""Select a set of fit individuals from input population"""
class SelectionOperator(BaseOperator):
    def __init__(self, optimizer):
        self.optimizer = optimizer

"""Produce a set of child states by crossover of input population"""
class CrossoverOperator(BaseOperator):
    def __init__(self, optimizer):
        self.optimizer = optimizer

"""Mutate input population by changing some member values"""
class MutationOperator(BaseOperator):
    def __init__(self, optimizer):
        self.optimizer = optimizer