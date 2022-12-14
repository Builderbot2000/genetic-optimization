import optimizer
import argparse
import most_fit_selection
import arithmetic_crossover, single_arithmetic_crossover, heuristic_crossover, intermediate_crossover
import random_add_mutation
import standard_fitness
import standard_termination

DEFAULT_EXPERIMENT_ID = "box 42"
DEFAULT_OBJECTIVE = "profit"
DEFAULT_OBJECTIVE_VAL = 1000000
DEFAULT_INSTANCE = "code/instances/example_instance.txt"
DEFAULT_MODIFIERS = "code/modifiers/example_modifiers.txt"
DEFAULT_OUTPUT = "code/output/output.txt"
DEFAULT_LOG = "code/log/log.txt"

DEFAULT_SELECTION_OPERATOR = "mfs"      # mps - most fit selection
DEFAULT_CROSSOVER_OPERATOR = "ic"       # lc - linear crossover
DEFAULT_MUTATION_OPERATOR = "ram"       # ram - random add mutation
DEFAULT_FITNESS_FUNCTION = "sf"         # sf - standard fitness
DEFAULT_TERMINATION_CHECK = "st"        # st - standard termination

DEFAULT_SELECTION_FACTOR = 5
DEFAULT_BRANCHING_FACTOR = 2
DEFAULT_ALPHA = 0.5
DEFAULT_MUTATION_FACTOR = 1.0
DEFAULT_MUTATION_POTENCY = 0.4
DEFAULT_MINIMUM_EPOCHS = 10
DEFAULT_MAXIMUM_EPOCHS = 100

"""Input files should be put under instances/, modifiers files should be put under modifiers/"""

if __name__ == '__main__':
    
    """Run experiment here"""
    parser = argparse.ArgumentParser(description='Runs genetic optimizer for a set of numerical configurations')
    parser.add_argument('--experiment_id', type=str, default=DEFAULT_EXPERIMENT_ID,
                        help='The unique identifier for this experiment, defaults to ' + str(DEFAULT_EXPERIMENT_ID))
    parser.add_argument('--objective', type=str, default=DEFAULT_OBJECTIVE,
                        help='The unique identifier for this experiment, defaults to ' + str(DEFAULT_OBJECTIVE))
    parser.add_argument('--objective_val', type=str, default=DEFAULT_OBJECTIVE_VAL,
                        help='The terminating value for the objective, defaults to ' + str(DEFAULT_OBJECTIVE_VAL))
    parser.add_argument('--input', type=str, default=DEFAULT_INSTANCE,
                        help='The name of the input file, defaults to ' + str(DEFAULT_INSTANCE))
    parser.add_argument('--modifiers', type=str, default=DEFAULT_MODIFIERS,
                        help='The name of the modifiers file, defaults to ' + str(DEFAULT_MODIFIERS))
    parser.add_argument('--output', type=str, default=DEFAULT_OUTPUT,
                        help='The filepath of the optimizer output, defaults to ' + str(DEFAULT_OUTPUT))
    parser.add_argument('--log', type=str, default=DEFAULT_LOG,
                        help='The filepath of the optimizer operations log, defaults to '+ str(DEFAULT_LOG) + \
                        ", if no log is needed, manually set this argument to \"\" ")
    parser.add_argument('--selection_operator', type=str, default=DEFAULT_SELECTION_OPERATOR,
                        help='The selection operator to use, defaults to ' + str(DEFAULT_SELECTION_OPERATOR))
    parser.add_argument('--crossover_operator', type=str, default=DEFAULT_CROSSOVER_OPERATOR,
                        help='The crossover operator to use, should be within interval [0, 1], defaults to ' + str(DEFAULT_CROSSOVER_OPERATOR))
    parser.add_argument('--mutation_operator', type=str, default=DEFAULT_MUTATION_OPERATOR,
                        help='The mutation operator to use, defaults to ' + str(DEFAULT_MUTATION_OPERATOR))
    parser.add_argument('--fitness_function', type=str, default=DEFAULT_FITNESS_FUNCTION,
                        help='The fitness function to use, defaults to ' + str(DEFAULT_FITNESS_FUNCTION))   
    parser.add_argument('--termination_check', type=str, default=DEFAULT_TERMINATION_CHECK,
                        help='The function used to determine the terminating condition, defaults to ' + str(DEFAULT_TERMINATION_CHECK))   
    parser.add_argument('--selection_factor', type=int, default=DEFAULT_SELECTION_FACTOR,
                        help='How many states to select from top k most fitting states, defaults to ' + 
                        str(DEFAULT_SELECTION_FACTOR))     
    parser.add_argument('--branching_factor', type=int, default=DEFAULT_BRANCHING_FACTOR,
                        help='How many child states are produced by two parents, defaults to ' + 
                        str(DEFAULT_BRANCHING_FACTOR))       
    parser.add_argument('--alpha', type=int, default=DEFAULT_MUTATION_FACTOR,
                        help='Value of the alpha parameter used in crossover operators, defaults to ' + 
                        str(DEFAULT_ALPHA))  
    parser.add_argument('--mutation_factor', type=float, default=DEFAULT_MUTATION_FACTOR,
                        help='How likely a state attribute is mutated, defaults to ' + 
                        str(DEFAULT_MUTATION_FACTOR))  
    parser.add_argument('--mutation_potency', type=float, default=DEFAULT_MUTATION_POTENCY,
                        help='Maximum of how much of a state can be mutated , defaults to ' + 
                        str(DEFAULT_MUTATION_POTENCY))  
    parser.add_argument('--minimum_epochs', type=int, default=DEFAULT_MINIMUM_EPOCHS,
                        help='Optimizer must run this many epochs before terminating, defaults to ' + 
                        str(DEFAULT_MINIMUM_EPOCHS))        
    parser.add_argument('--maximum_epochs', type=int, default=DEFAULT_MAXIMUM_EPOCHS,
                        help='Optimizer must terminate once it has run this many epochs, defaults to ' + 
                        str(DEFAULT_MAXIMUM_EPOCHS))         
    args = parser.parse_args()

    op = optimizer.Optimizer()
    op.experiment_id = args.experiment_id
    op.objective = args.objective
    op.input_path = args.input
    op.modifiers_path = args.modifiers
    op.output_path = args.output
    op.log_path = args.log
    if args.crossover_operator == "ac":
        op.crossover_operator = arithmetic_crossover.ArithmeticCrossover(op)
    if args.crossover_operator == "sac":
        op.crossover_operator = single_arithmetic_crossover.SingleArithmeticCrossover(op)
    if args.crossover_operator == "hc":
        op.crossover_operator = heuristic_crossover.HeuristicCrossover(op)
    if args.crossover_operator == "ic":
        op.crossover_operator = intermediate_crossover.IntermediateCrossover(op)
    if args.mutation_operator == "ram":
        op.mutation_operator = random_add_mutation.RandomAddMutation(op)
    if args.fitness_function == "sf":
        op.fitness_function = standard_fitness.StandardFitness(op)
    if args.termination_check == "st":
        op.termination_check = standard_termination.StandardTermination(op)
    if args.selection_operator == "mfs":
        op.selection_operator = most_fit_selection.MostFitSelection(op)
    op.selection_factor = args.selection_factor
    op.branching_factor = args.branching_factor
    op.alpha = args.alpha
    op.mutation_factor = args.mutation_factor
    op.mutation_potency = args.mutation_potency
    op.minimum_epochs = args.minimum_epochs
    op.maximum_epochs = args.maximum_epochs
    op.load()
    op.run()