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
    def __init__(self, selection_factor, fitness_function):
        self.selection_factor = selection_factor
        self.fitness_function = fitness_function

"""Produce a set of child states by crossover of input population"""
class CrossoverOperator(BaseOperator):
    def __init__(self, branching_factor):
        self.branching_factor = branching_factor

"""Mutate input population by changing some member values"""
class MutationOperator(BaseOperator):
    def __init__(self, mutation_factor):
        self.mutation_factor = mutation_factor