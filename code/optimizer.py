from most_profit_selection import *
from arithmetic_crossover import *
from random_add_mutation import *
from standard_fitness import *
from standard_termination import *
import os
import copy

class Optimizer:
    
    """Data"""
    population: list                            # collection of states the optimizer currently holds
    population = []   
    # Note: Each state is a dictionary holding a collection of attribute/value pairs""" 
    modifiers: list                             # collection of modifiers the optimizer currently has
    modifiers = []
    state_id_counter = 0                        # current highest id held by any state

    """File paths"""
    input_path = ""                             # the name of the inputs file
    modifiers_path = ""                         # the name of the modifiers file
    output_path = ""                            # the filepath of the optimizer output
    log_path = ""                               # the filepath of the stat log file

    """Operators"""
    selection_operator = None                   # the selection operator used by the optimizer
    crossover_operator = None                   # the crossover operator used by the optimizer
    mutation_operator = None                    # the mutation operator used by the optimizer
    fitness_function = None                     # the fitness function used by the optimizer
    termination_check = None                    # the function used to determine the terminating condition
    
    """Hyperparameters"""
    selection_factor = 0                        # how many states to select from top k most fitting states
    branching_factor = 0                        # how many child states are produced by two parents
    arithmetic_alpha = 0                        # value of the alpha parameter used in arithmetic crossover
    mutation_factor = 0                         # how likely a state attribute is mutated
    mutation_potency = 0                        # maximum of how much of a state can be mutated 
    minimum_epochs = 0                          # optimizer must run this many epochs before terminating
    maximum_epochs = 0                          # optimizer must terminate once it has run this many epochs

    """Statistics"""
    epochs = 0                                  # number of epochs this optimizer has run
    total_child_states_expanded = 0             # number of total child states expanded by the crossover operator
    current_best_fit = None                     # the current most fit state by fitness score
    terminate = False                           # whether the optimizer should terminate
    
    def load(self):
        """Load population and modifiers from paths specified by inputs_path and modifiers_path"""
        state = {}
        input_lines = open(self.input_path, 'r').readlines()
        for line in input_lines:
            item = line.split()
            state[item[0]] = item[1]
        # print(state)
        self.population.append(state)

        modifier_lines = open(self.modifiers_path, 'r').readlines()
        for line in modifier_lines:
            item = line.split('@')
            item[0] = item[0].strip()
            item[1] = item[1].strip()
            modifier = item[0].split()
            modifier.append(item[1])
            # print(modifier)
            self.modifiers.append(modifier)
    
    def run(self):
        """
        Run the genetic algorithm with the given parameters on current population and 
        output to path specified by output_path
        """
        
        """Initialize Population"""
        self.population[0]['id'] = 0
        for i in range(1, self.selection_factor * 4):
            clone = copy.deepcopy(self.population[0])
            clone['id'] = i
            self.population.append(clone)
            self.state_id_counter = i
        self.population = self.mutation_operator.run()

        while (not self.terminate or self.epochs < self.minimum_epochs) \
        and self.epochs < self.maximum_epochs:
            """Selection Phase"""
            self.population = self.selection_operator.run()
            # print("Post Selection:")
            # print(len(self.population))
            # print(self.population)

            """Crossover Phase"""
            self.population = self.crossover_operator.run()
            # print("Post Crossover:")
            # print(len(self.population))
            # print(self.population)

            """Mutation Phase"""
            self.population = self.mutation_operator.run()
            # print("Post Mutation:")
            # print(len(self.population))
            # print(self.population)

            """Check Phase"""
            for state in self.population:
                self.terminate = self.termination_check.check(state)
            self.epochs += 1
            # print(self.epochs)