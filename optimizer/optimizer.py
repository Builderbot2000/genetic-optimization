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

class Optimizer:
    
    """Data"""
    instance = {}                              # problem specifications
    population = []                            # collection of states the optimizer currently holds
    state_id_counter = 0                       # current highest id held by any state
    calculator = None                          # used to estimate the profit

    """Operators"""
    selection_operator = None                  # the selection operator used by the optimizer
    crossover_operator = None                  # the crossover operator used by the optimizer
    mutation_operator = None                   # the mutation operator used by the optimizer
    fitness_function = None                    # the fitness function used by the optimizer
    termination_check = None                   # the function determining when to terminate
    
    """Hyperparameters"""
    selection_factor = None                    # number of states selected for the next generation
    branching_factor = None                    # number of states produced by two parents
    alpha = None                               # value of alpha in crossover operators
    mutation_factor = None                     # mutation probability
    mutation_potency = None                    # maximum of how much of a state can be mutated 
    minimum_epochs = None                      # minimum number of epochs the optimizer can run
    maximum_epochs = None                      # maximum number of epochs the optimizer can run

    """Statistics"""
    epochs = 0                                 # number of epochs this optimizer has run
    num_states_generated = 0                   # number of states generated by the optimizer 
    current_best_fit = None                    # the current most fit state by fitness score
    current_best_score = -inf                  # fitness score of the current most fit state
    terminate = False                          # whether the optimizer should terminate

    def __init__(self, args):
        self.__load(args.instance)

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

    def __load(self, instance):
        """Load problem specifications and initilize configurable parameters"""
        
        self.instance = deepcopy(instance)
        self.calculator = Calculator(self.instance)

        state = {}
        state['id'] = 0
        state['unit_price'] = instance['mean_unit_price'] + instance['unit_price_std']
        state['num_equipments'] = instance['market_size'] * instance['num_equipments_per_unit']
        state['equipment_grade'] = 1
        state['num_workers'] = instance['market_size'] * instance['num_workers_per_unit']
        state['worker_wage'] = instance['wage_of_best_workers']
        state['marketing_budget'] = instance['full_coverage_marketing_cost']
        state['RaD_spending'] = instance['RaD_cost_for_max_improvement']
        state['design_spending'] = instance['cost_of_best_architects']
        state['construction_spending'] = instance['cost_of_best_contractors']

        self.population.append(state)

    def run(self):
        """
        Run the genetic algorithm with the given parameters on current population and 
        output to path specified by output_path
        """
        detailed_results = []
        
        """Initialize Population"""
        for i in range(1, self.selection_factor):
            clone = deepcopy(self.population[0])
            clone['id'] = i
            self.population.append(clone)
            self.state_id_counter = i

        start = time()

        self.population = self.mutation_operator.run()
        self.population = self.selection_operator.run()

        self.population = self.crossover_operator.run()
        self.num_states_generated += len(self.population)
        
        self.population = self.mutation_operator.run()

        while (True):
            """Selection Phase"""
            self.population = self.selection_operator.run()

            running_time = time() - start

            self.epochs += 1
            if self.epochs % 100 == 0:
                detailed_results.append(
                    {'current_best_fit': self.current_best_fit,
                     'num_states_generated': self.num_states_generated,
                     'num_epochs': self.epochs,
                     'running_time': running_time}
                )
                
            if (self.terminate or self.epochs == self.maximum_epochs) and \
                self.epochs > self.minimum_epochs: \
                break

            """Crossover Phase"""
            self.population = self.crossover_operator.run()
            self.num_states_generated += len(self.population)

            """Mutation Phase"""
            self.population = self.mutation_operator.run()

            """Normalization"""
            for i in range(len(self.population)):
                equipment_grade = self.population[i]['equipment_grade']
                self.population[i]['equipment_grade'] = min(equipment_grade, 1.0)

        
        return self.current_best_fit, self.epochs, self.num_states_generated, \
               running_time, detailed_results
