import optimizer
import argparse
import most_fit_selection
import linear_crossover
import random_add_mutation
import standard_fitness
import standard_termination

DEFAULT_INSTANCE = "code/instances/example_instance.txt"
DEFAULT_MODIFIERS = "code/modifiers/example_modifiers.txt"

DEFAULT_SELECTION_OPERATOR = "mfs"      # mfs - most fit selection
DEFAULT_CROSSOVER_OPERATOR = "lc"       # lc - linear crossover
DEFAULT_MUTATION_OPERATOR = "ram"       # ram - random add mutation
DEFAULT_FITNESS_FUNCTION = "sf"         # sf - standard fitness
DEFAULT_TERMINATION_CHECK = "st"        # st - standard termination

DEFAULT_SELECTION_FACTOR = 5
DEFAULT_BRANCHING_FACTOR = 2
DEFAULT_MUTATION_FACTOR = 5
DEFAULT_MINIMUM_EPOCHS = 10
DEFAULT_MAXIMUM_EPOCHS = 20

"""Input files should be put under instances/, modifiers files should be put under modifiers/"""

if __name__ == '__main__':
    
    """Run experiment here"""
    parser = argparse.ArgumentParser(description='Runs genetic optimizer for a set of product specifications')
    parser.add_argument('--input', type=str, default=DEFAULT_INSTANCE,
                        help='The name of the input file, defaults to ' + str(DEFAULT_INSTANCE))
    parser.add_argument('--modifiers', type=str, default=DEFAULT_MODIFIERS,
                        help='The name of the modifiers file, defaults to ' + str(DEFAULT_MODIFIERS))
    parser.add_argument('--output', type=str, default="outputs/output.txt",
                        help='The filepath of the optimizer output, defaults to outputs/output.txt')
    parser.add_argument('--log', type=str, default="log/log.txt",
                        help='The filepath of the optimizer operations log, defaults to log/log.txt')
    parser.add_argument('--selection_operator', type=str, default=DEFAULT_SELECTION_OPERATOR,
                        help='The selection operator to use, defaults to ' + str(DEFAULT_SELECTION_OPERATOR))
    parser.add_argument('--crossover_operator', type=str, default=DEFAULT_CROSSOVER_OPERATOR,
                        help='The crossover operator to use, defaults to ' + str(DEFAULT_CROSSOVER_OPERATOR))
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
    parser.add_argument('--mutation_factor', type=int, default=DEFAULT_MUTATION_FACTOR,
                        help='How much of a state is mutated, defaults to ' + 
                        str(DEFAULT_MUTATION_FACTOR))  
    parser.add_argument('--minimum_epochs', type=int, default=DEFAULT_MINIMUM_EPOCHS,
                        help='Optimizer must run this many epochs before terminating, defaults to ' + 
                        str(DEFAULT_MINIMUM_EPOCHS))        
    parser.add_argument('--maximum_epochs', type=int, default=DEFAULT_MAXIMUM_EPOCHS,
                        help='Optimizer must terminate once it has run this many epochs, defaults to ' + 
                        str(DEFAULT_MAXIMUM_EPOCHS))         
    args = parser.parse_args()

    op = optimizer.Optimizer()
    op.input_path = args.input
    op.modifiers_path = args.modifiers
    op.output_path = args.output
    if args.crossover_operator == "lc":
        op.crossover_operator = linear_crossover.LinearCrossover(op)
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
    op.mutation_factor = args.mutation_factor
    op.minimum_epochs = args.minimum_epochs
    op.maximum_epochs = args.maximum_epochs
    op.load()
    op.run()