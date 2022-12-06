from selection_operators import *
from crossover_operators import *
from mutation_operators import *
from fitness import evaluate_fitness

class Optimizer:
    
    """States"""
    population: list 
    population = []
    modifiers: dict
    modifiers = {}

    """Operators"""
    selection_operator = most_fit_selection     # the selection operator used by the optimizer
    crossover_operator = linear_crossover       # the crossover operator used by the optimizer
    mutation_operator = random_add_mutation     # the mutation operator used by the optimizer
    
    """Default hyperparameters"""
    selection_factor = 5                        # how many states to select from top k most fitting states
    branching_factor = 2                        # how many child states are produced by two parents
    mutation_factor = 5                         # how much of a state is mutated
    minimum_epochs = 1                          # optimizer must run this many epochs before terminating

    def load(self, filepath):
        """Load input from file specified by filepath"""
        # Your implementation here

        pass

    def reset(self):
        """Reset states and hyperparameters"""
        # Your implementation here

        pass

    def run(self):
        """Run a set of optimization cycles on current population"""
        # Your implementation here

        pass

