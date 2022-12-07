from most_fit_selection import *
from linear_crossover import *
from random_add_mutation import *
from standard_fitness import *

class Optimizer:
    
    """Data"""
    population: list                            # collection of states the optimizer currently holds
    population = []   
    # Note: Each state is a dictionary holding a collection of attribute/value pairs""" 
    modifiers: list                             # collection of modifiers the optimizer currently has
    modifiers = []

    """File paths"""
    inputs_path = ""                            # the name of the inputs file
    modifiers_path = ""                         # the name of the modifiers file
    output_path = ""                            # the filepath of the optimizer output

    """Operators"""
    selection_operator = None                   # the selection operator used by the optimizer
    crossover_operator = None                   # the crossover operator used by the optimizer
    mutation_operator = None                    # the mutation operator used by the optimizer
    fitness_function = None                     # the fitness function used by the optimizer
    
    """Hyperparameters"""
    selection_factor = 0                        # how many states to select from top k most fitting states
    branching_factor = 0                        # how many child states are produced by two parents
    mutation_factor = 0                         # how much of a state is mutated
    minimum_epochs = 0                          # optimizer must run this many epochs before terminating
    
    def load(self):
        """Load population and modifiers from paths specified by inputs_path and modifiers_path"""
        # Your implementation here

        pass

    def run(self):
        """
        Run the genetic algorithm with the given parameters on current population and 
        output to path specified by output_path
        """
        # Your implementation here

        pass

