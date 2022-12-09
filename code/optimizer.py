from most_profit_selection import *
from arithmetic_crossover import *
from random_add_mutation import *
from standard_fitness import *
from standard_termination import *
import os
import copy

class Optimizer:
    
    """Data"""
    experiment_id = 0                           # unique identifier for a particular experiment
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
        input_file = open(self.input_path, 'r')
        input_lines = input_file.readlines()
        for line in input_lines:
            item = line.split()
            state[item[0]] = item[1]
        # print(state)
        self.population.append(state)
        input_file.close()

        modifier_file = open(self.modifiers_path, 'r')
        modifier_lines = modifier_file.readlines()
        for line in modifier_lines:
            item = line.split('@')
            item[0] = item[0].strip()
            item[1] = item[1].strip()
            modifier = item[0].split()
            modifier.append(item[1])
            # print(modifier)
            self.modifiers.append(modifier)
        modifier_file.close()
    
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

            """Crossover Phase"""
            self.population = self.crossover_operator.run()

            """Mutation Phase"""
            self.population = self.mutation_operator.run()

            """Check Phase"""
            for state in self.population:
                self.terminate = self.termination_check.check(state)
            self.epochs += 1
        
        """Write to output"""
        best_score = self.fitness_function.evaluate(self.current_best_fit)
        output_file = open(self.output_path, 'a+')
        output = "\n=== Experiment " + str(self.experiment_id) + " ===\n"
        for attr in self.current_best_fit:
            output += attr + ": " + str(self.current_best_fit[attr]) + "\n"
        output += "--- scores ---\n"
        for sattr in best_score:
            output += sattr + ": " + str(best_score[sattr]) + "\n"
        output += "=== END ===\n"
        output_file.write(output)
        output_file.close()

        """Log Statistics"""
        if self.log_path != "":
            log_file = open(self.log_path, 'a+')
            log = "\n=== Experiment " + str(self.experiment_id) + " ===\n"
            log += "epochs ran: " + str(self.epochs) + "\n"
            log += "=== END ===\n"
            log_file.write(log)
            log_file.close()