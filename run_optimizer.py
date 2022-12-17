from optimizer.optimizer import Optimizer
from optimizer.calculator import Calculator
import argparse
import os

SEL_OPS = {'mfs': 'most_fit_selection'}
CROSS_OPS = {'ic':'intermediate_crossover',
             'ac':'arithmetic_crossover', 
             'sac':'single_arithmetic_crossover'}
MUT_OPS = {'ram':'random_add_mutation'}

def parse_instance(input_path):
    input_file = open(input_path, 'r')
    input_lines = input_file.readlines()

    instance = {}
    for line in input_lines:
        item = line.split()
        instance[item[0]] = float(item[1])
    return instance

if __name__ == '__main__':
    """Path to input file specifying the instance"""
    DEFAULT_INSTANCE = "instances/wafer.log"

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

    DEFAULT_SELECTION_FACTOR = 20
    DEFAULT_BRANCHING_FACTOR = 2
    DEFAULT_ALPHA = 0.5
    DEFAULT_MUTATION_FACTOR = 1.0
    DEFAULT_MUTATION_POTENCY = 0.4
    DEFAULT_MINIMUM_EPOCHS = 10
    DEFAULT_MAXIMUM_EPOCHS = 100

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
                        help='The crossover operator to use, defaults to ' + 
                              str(DEFAULT_CROSSOVER_OPERATOR))

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
                        help='How many child states are produced by two parents, defaults to ' + 
                        str(DEFAULT_BRANCHING_FACTOR))  

    parser.add_argument('--alpha', type=int, default=DEFAULT_ALPHA,
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
    args.instance = parse_instance(args.input)

    """Rum optimizer on the given instance"""
    op = Optimizer(args)
    best_fit, num_epochs_run, num_states_generated, running_time, _ = op.run()

    """Retrieve the results of best_fit""" 
    calculator = Calculator(args.instance)
    results, profit = calculator.run(best_fit, more_details=True)

    if not os.path.exists('output/'):
        os.makedirs('output/')

    """output_file_path: output/[instance_name].out.log"""
    output_file_path = 'output/' + args.input.split('/')[-1].split('.')[-2] + '.out.log'
    output_file = open(output_file_path, 'w')

    """Write instance specifications to output_file"""
    out = "--- Instance Specifications ---" + '\n'
    for attr in args.instance.keys():
        out += attr + ": " + str(args.instance[attr]) + '\n'
    
    """Write optimizer details to output_file"""
    out += "\n--- Optimizer Details ---\n"
    out += "selection factor: " + str(args.selection_factor) + '\n'
    out += "alpha: " + str(args.alpha) + '\n'
    out += "mutation_factor: " + str(args.mutation_factor) + '\n'
    out += "mutation_potency: " + str(args.mutation_potency) + '\n'
    out += "minimum_epochs: " + str(args.minimum_epochs) + '\n'
    out += "maximum_epochs: " + str(args.maximum_epochs) + '\n'
    out += "selection_operator: " + SEL_OPS[args.selection_operator] + '\n'
    out += "crossover_operator: " + CROSS_OPS[args.crossover_operator] + '\n'
    out += "mutation_operator: " + MUT_OPS[args.mutation_operator] + '\n'

    """Write best results to output_file"""
    out += "\n--- Final Configurations ---\n"
    for attr in best_fit.keys():
        out += attr + ": " + str(best_fit[attr]) + '\n'
    
    out += "\n--- Final Results ---\n"
    for attr in results.keys():
        out += attr + ": " + str(results[attr]) + '\n'
    out += "profit: " + str(profit) + '\n'

    """Write run's statistics to output_file"""
    out += "\n--- Statistics ---\n"
    out += "num_epochs_run: " + str(num_epochs_run) + '\n'
    out += "num_states_generated: " + str(num_states_generated) + '\n'
    out += "running_time: " + str(running_time) + '\n'

    output_file.write(out)
    output_file.close()
