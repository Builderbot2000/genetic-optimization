import optimizer
import argparse

DEFAULT_INSTANCE = "instances/example_instance.txt"
DEFAULT_MODIFIERS = "modifiers/example_modifiers.txt"

DEFAULT_SELECTION_OPERATOR = "mfs"      # mfs - most fit selection
DEFAULT_CROSSOVER_OPERATOR = "lc"       # lc - linear crossover
DEFAULT_MUTATION_OPERATOR = "ram"       # ram - random add mutation
DEFAULT_FITNESS_FUNCTION = "sf"         # sf - standard fitness

DEFAULT_SELECTION_FACTOR = 5
DEFAULT_BRANCHING_FACTOR = 2
DEFAULT_MUTATION_FACTOR = 5
DEFAULT_MINIMUM_EPOCHS = 1

"""Input files should be put under instances/, modifiers files should be put under modifiers/"""

if __name__ == '__main__':
    
    """Run experiment here"""
    parser = argparse.ArgumentParser(description='Runs genetic optimizer for a set of product specifications')
    parser.add_argument('--inputs', type=str, default=DEFAULT_INSTANCE,
                        help='The name of the inputs file, defaults to ' + str(DEFAULT_INSTANCE))
    parser.add_argument('--modifiers', type=str, default=DEFAULT_MODIFIERS,
                        help='The name of the modifiers file, defaults to ' + str(DEFAULT_MODIFIERS))
    parser.add_argument('--output', type=str, default="outputs/output.txt",
                        help='The filepath of the optimizer output, defaults to outputs/output.txt')
    parser.add_argument('--selection_operator', type=str, default=DEFAULT_SELECTION_OPERATOR,
                        help='The selection operator to use, defaults to ' + str(DEFAULT_SELECTION_OPERATOR))
    parser.add_argument('--crossover_operator', type=str, default=DEFAULT_CROSSOVER_OPERATOR,
                        help='The crossover operator to use, defaults to ' + str(DEFAULT_CROSSOVER_OPERATOR))
    parser.add_argument('--mutation_operator', type=str, default=DEFAULT_MUTATION_OPERATOR,
                        help='The mutation operator to use, defaults to ' + str(DEFAULT_MUTATION_OPERATOR))
    parser.add_argument('--fitness_function', type=str, default=DEFAULT_FITNESS_FUNCTION,
                        help='The fitness function to use, defaults to ' + str(DEFAULT_FITNESS_FUNCTION))   
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
    args = parser.parse_args()

    op = optimizer.Optimizer()
    op.inputs_path = args.inputs
    op.modifiers_path = args.modifiers
    op.output_path = args.output
    op.selection_operator = args.selection_operator
    op.crossover_operator = args.crossover_operator
    op.mutation_operator = args.mutation_operator
    op.fitness_function = args.fitness_function
    op.selection_factor = args.selection_factor
    op.branching_factor = args.branching_factor
    op.mutation_factor = args.mutation_factor
    op.minimum_epochs = args.minimum_epochs
    op.load()
    op.run()