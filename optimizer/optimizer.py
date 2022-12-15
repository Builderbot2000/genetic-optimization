from .operators.most_fit_selection import *
from .operators.arithmetic_crossover import *
from .operators.single_arithmetic_crossover import *
from .operators.heuristic_crossover import *
from .operators.intermediate_crossover import *
from .operators.random_add_mutation import *
from .operators.standard_fitness import *
from .operators.standard_termination import *
from .calculator import *
from time import time 
from copy import deepcopy
from numpy import inf
from random import uniform

class Optimizer:
    
    """Data"""
    instance = {}                              # problem specifications
    population = []                            # collection of states the optimizer currently holds
    state_id_counter = 0                       # current highest id held by any state
    calculator = None                          # used to estimate the profit

    """File paths"""
    input_path = ""                            # the name of the inputs file

    """Operators"""
    selection_operator = None                  # the selection operator used by the optimizer
    crossover_operator = None                  # the crossover operator used by the optimizer
    mutation_operator = None                   # the mutation operator used by the optimizer
    fitness_function = None                    # the fitness function used by the optimizer
    termination_check = None                   # the function determining when to terminate
    
    """Hyperparameters"""
    selection_factor = 0                       # number of states selected for the next generation
    branching_factor = 0                       # number of child states produced by two parents
    alpha = 0                                  # value of alpha in crossover operators
    mutation_factor = 0                        # mutation probability
    mutation_potency = 0                       # maximum of how much of a state can be mutated 
    minimum_epochs = 0                         # minimum number of epochs the optimizer can run
    maximum_epochs = 0                         # maximum number of epochs the optimizer can run

    """Statistics"""
    epochs = 0                                 # number of epochs this optimizer has run
    num_states_generated = 0                   # number of states generated by the optimizer 
    current_best_fit = None                    # the current most fit state by fitness score
    current_best_score = -inf                  # fitness score of the current most fit state
    terminate = False                          # whether the optimizer should terminate

    def __init__(self, args):
        self.input_path = args.input
        self.log_path = args.log

        if args.fitness_function == "sf":
            self.fitness_function = StandardFitness(self)
        if args.selection_operator == "mfs":
            self.selection_operator = MostFitSelection(self)
        if args.crossover_operator == "ac":
            self.crossover_operator = ArithmeticCrossover(self)
        elif args.crossover_operator == "sac":
            self.crossover_operator = SingleArithmeticCrossover(self)
        elif args.crossover_operator == "hc":
            self.crossover_operator = HeuristicCrossover(self)
        elif args.crossover_operator == "ic":
            self.crossover_operator = IntermediateCrossover(self)
        if args.mutation_operator == "ram":
            self.mutation_operator = RandomAddMutation(self)
        if args.termination_check == "st":
            self.termination_check = StandardTermination(self)

        self.selection_factor = args.selection_factor
        self.branching_factor = args.branching_factor
        self.alpha = args.alpha
        self.mutation_factor = args.mutation_factor
        self.mutation_potency = args.mutation_potency
        self.minimum_epochs = args.minimum_epochs
        self.maximum_epochs = args.maximum_epochs
    
    def load(self):
        """
        Load problem specifications and initilize configurable parameters
        """

        """Load problem specifications from input_path"""
        input_file = open(self.input_path, 'r')
        input_lines = input_file.readlines()
        for line in input_lines:
            item = line.split()
            self.instance[item[0]] = float(item[1])
        self.calculator = Calculator(self.instance)

        """Randomly configurable parameters"""
        state = {}
        state['id'] = 0
        # state['shelf_price'] = uniform(0, self.instance['mean_shelf_price'] * 2)
        # state['num_equipments'] = uniform(0, self.instance['market_size'] /
        #                                    self.instance['num_equipments_per_unit'])
        # state['equipment_grade'] = uniform(0, 1)
        # state['num_workers'] = uniform(0, self.instance['market_size'] /
        #                                   self.instance['num_workers_per_unit'])
        # state['worker_wage'] = uniform(0, self.instance['wage_for_best_workers'])
        # state['marketing_budget'] = uniform(0, self.instance['full_coverage_marketing_cost'])
        # state['RaD_spending'] = uniform(0, self.instance['RaD_cost_for_max_improvement'])
        # state['design_spending'] = uniform(0, self.instance['pay_for_best_facility_designers'])
        # state['construction_spending'] = uniform(0, self.instance['pay_for_best_contractors'])
        state['shelf_price'] = self.instance['mean_shelf_price']
        state['num_equipments'] = self.instance['market_size'] * \
                                  self.instance['num_equipments_per_unit']
        state['equipment_grade'] = 1
        state['num_workers'] = self.instance['market_size'] * \
                               self.instance['num_workers_per_unit']
        state['worker_wage'] = self.instance['wage_for_best_workers']
        state['marketing_budget'] = self.instance['full_coverage_marketing_cost']
        state['RaD_spending'] = self.instance['RaD_cost_for_max_improvement']
        state['design_spending'] = self.instance['pay_for_best_facility_designers']
        state['construction_spending'] = self.instance['pay_for_best_contractors']
        print(state)

        self.population.append(state)
        input_file.close()

    def run(self):
        """
        Run the genetic algorithm with the given parameters on current population and 
        output to path specified by output_path
        """
        
        """Initialize Population"""
        for i in range(1, self.selection_factor * 4):
            clone = deepcopy(self.population[0])
            clone['id'] = i
            self.population.append(clone)
            self.state_id_counter = i
        self.population = self.mutation_operator.run()
        self.num_states_generated += len(self.population)

        start = time()

        while (not self.terminate or self.epochs < self.minimum_epochs) \
        and self.epochs < self.maximum_epochs:
            """Selection Phase"""
            self.population = self.selection_operator.run()
            self.termination_check.check(self.population[0])

            """Crossover Phase"""
            self.population = self.crossover_operator.run()
            self.num_states_generated += len(self.population)

            """Mutation Phase"""
            self.population = self.mutation_operator.run()

            self.epochs += 1
        
        running_time = time() - start
        return self.instance, self.current_best_fit, self.num_states_generated, running_time 

        