from optimizer.optimizer import Optimizer
from optimizer.calculator import Calculator
import argparse

SELECTION_OPERATOR = {'mfs': 'most_fit_selection'}
CROSSOVER_OPERATOR = {'ic':'intermediate_crossover', 'hc':'heuristic_crossover',
                       'ac':'arithmetic_crossover', 'sac':'single_arithmetic_crossover'}
MUTATION_OPERATOR = {'ram':'random_add_mutation'}

def run_optimizer(args):
    op = Optimizer(args)
    op.load()
    return op.run()

if __name__ == '__main__':
    """Path to input file specifying the instance"""
    DEFAULT_INSTANCE = "instances/wafer.instance"

    """
    Available values for each hyperparameter:
    selection operator: {'mfs': most_fit_selection}
    crossover operator: {'ic': intermediate_crossover, 'hc': heuristic_crossover,
                         'ac': arithmetic_crossover, 'sac': single_arithmetic_crossover}
    mutation operator: {'ram': random_add_mutation}
    fitness function: {'sf': standard_fitness}
    termination check: {'st': standard_termination}
    """
    DEFAULT_SELECTION_OPERATOR = 'mfs'
    DEFAULT_CROSSOVER_OPERATOR = 'ic'
    DEFAULT_MUTATION_OPERATOR = 'ram'
    DEFAULT_FITNESS_FUNCTION = 'sf'
    DEFAULT_TERMINATION_CHECK = 'st'

    DEFAULT_SELECTION_FACTOR = 50
    DEFAULT_BRANCHING_FACTOR = 2
    DEFAULT_ALPHA = 0.5
    DEFAULT_MUTATION_FACTOR = 1.0
    DEFAULT_MUTATION_POTENCY = 0.4
    DEFAULT_MINIMUM_EPOCHS = 10
    DEFAULT_MAXIMUM_EPOCHS = 100

    """Rum optimizer on the given instance"""
    parser = argparse.ArgumentParser(
      description="Runs genetic optimizer for a set of numerical configurations"
    )

    parser.add_argument('--input', type=str, default=DEFAULT_INSTANCE,
                        help="The path of the input file, defaults to " +
                              str(DEFAULT_INSTANCE))

    parser.add_argument('--selection_operator', type=str, default=DEFAULT_SELECTION_OPERATOR,
                        help="The selection operator to use, defaults to " +
                              str(DEFAULT_SELECTION_OPERATOR))

    parser.add_argument('--crossover_operator', type=str, default=DEFAULT_CROSSOVER_OPERATOR,
                        help="The crossover operator to use, should be within interval [0, 1], \
                              defaults to " + str(DEFAULT_CROSSOVER_OPERATOR))

    parser.add_argument('--mutation_operator', type=str, default=DEFAULT_MUTATION_OPERATOR,
                        help="The mutation operator to use, defaults to " +
                              str(DEFAULT_MUTATION_OPERATOR))

    parser.add_argument('--fitness_function', type=str, default=DEFAULT_FITNESS_FUNCTION,
                        help="The fitness function to use, defaults to " +
                              str(DEFAULT_FITNESS_FUNCTION))   

    parser.add_argument('--termination_check', type=str, default=DEFAULT_TERMINATION_CHECK,
                        help="The function used to determine the terminating condition, \
                              defaults to " + str(DEFAULT_TERMINATION_CHECK)) 

    parser.add_argument('--selection_factor', type=int, default=DEFAULT_SELECTION_FACTOR,
                        help="How many states to select from top k most fitting states, \
                              defaults to " + str(DEFAULT_SELECTION_FACTOR))     

    parser.add_argument('--branching_factor', type=int, default=DEFAULT_BRANCHING_FACTOR,
                        help="How many child states are produced by two parents, defaults to " +
                              str(DEFAULT_BRANCHING_FACTOR))

    parser.add_argument('--alpha', type=int, default=DEFAULT_MUTATION_FACTOR,
                        help="Value of the alpha parameter used in crossover operators, \
                              defaults to " + str(DEFAULT_ALPHA))  

    parser.add_argument('--mutation_factor', type=float, default=DEFAULT_MUTATION_FACTOR,
                        help="How likely a state attribute is mutated, defaults to " + 
                              str(DEFAULT_MUTATION_FACTOR))  
                              
    parser.add_argument('--mutation_potency', type=float, default=DEFAULT_MUTATION_POTENCY,
                        help="Maximum of how much of a state can be mutated , defaults to " + 
                              str(DEFAULT_MUTATION_POTENCY))  

    parser.add_argument('--minimum_epochs', type=int, default=DEFAULT_MINIMUM_EPOCHS,
                        help="Optimizer must run this many epochs before terminating, \
                              defaults to " + str(DEFAULT_MINIMUM_EPOCHS))        

    parser.add_argument('--maximum_epochs', type=int, default=DEFAULT_MAXIMUM_EPOCHS,
                        help="Optimizer must terminate once it has run this many epochs, \
                              defaults to " + str(DEFAULT_MAXIMUM_EPOCHS))         

    args = parser.parse_args()
    instance, best_fit, run_info = run_optimizer(args)

    calculator = Calculator(instance)
    details, profit = calculator.run(best_fit, more_details=True)

    output_file_path = 'outputs/' + args.input.split('/')[-1].split('.')[-2] + '.out'
    output_file = open(output_file_path, 'w')

    out = "--- Instance Specifications ---" + '\n'
    for attr in instance.keys():
        out += attr + ": " + str(instance[attr]) + '\n'
    
    out += "\n--- Final Configurations ---\n"
    for attr in best_fit.keys():
        out += attr + ": " + str(best_fit[attr]) + '\n'
    
    out += "\n--- Final Results ---\n"
    for attr in details.keys():
        out += attr + ": " + str(details[attr]) + '\n'
    out += "profit: " + str(profit) + '\n'

    out += "\n--- Run Info ---\n"
    out += "running_time: " + str(run_info[0]) + '\n'
    out += "num_states_generated: " + str(run_info[1]) + '\n'

    out += "\n--- Optimizer Info ---\n"
    out += "selection factor: " + str(args.selection_factor) + '\n'
    out += "alpha: " + str(args.alpha) + '\n'
    out += "mutation_factor: " + str(args.mutation_factor) + '\n'
    out += "mutation_potency: " + str(args.mutation_potency) + '\n'
    out += "minimum_epochs: " + str(args.minimum_epochs) + '\n'
    out += "maximum_epochs: " + str(args.maximum_epochs) + '\n'
    out += "selection_operator: " + SELECTION_OPERATOR[args.selection_operator] + '\n'
    out += "crossover_operator: " + CROSSOVER_OPERATOR[args.crossover_operator] + '\n'
    out += "mutation_operator: " + MUTATION_OPERATOR[args.mutation_operator] + '\n'

    output_file.write(out)
    output_file.close()