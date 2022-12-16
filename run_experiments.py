from run_optimizer import parse_instance, SELECTION_OPERATOR, \
                          CROSSOVER_OPERATOR, MUTATION_OPERATOR
from optimizer.optimizer import Optimizer
import argparse
import os

if __name__ == '__main__':
    DEFAULT_INSTANCE = "instances/wafer.log"

    parser = argparse.ArgumentParser(
      description="Runs genetic optimizer for a set of numerical configurations \
                   with different sets of hyperparameters"
    )
    parser.add_argument('--input', type=str, default=DEFAULT_INSTANCE,
                        help="The path of the input file, defaults to " +
                              str(DEFAULT_INSTANCE))
    args = parser.parse_args()
    args.instance = parse_instance(args.input)

    selection_operator = 'mfs'
    crossover_operators = ['ic','hc','ac','sac']
    mutation_operator = 'ram'
    fitness_function = 'sf'
    termination_check = 'st'

    selection_factors = [20, 50, 100]
    alpha = 0.5
    mutation_factors = [0.2, 0.5, 1.0]
    mutation_potencies = [0.4, 0.6, 0.8]
    minimum_epochs = 10
    maximum_epochs_list = [100, 1000, 10000]

    """Write instance specifications to experiments/[instance_name].expt.log"""
    if not os.path.exists('output/'):
        os.makedirs('output/')
        
    output_file_path = 'output/' + args.input.split('/')[-1].split('.')[-2] + '.expt.log'
    with open(output_file_path, 'w') as f:
        f.write("--- Instance Specifications ---" + '\n')
        for attr in args.instance.keys():
            f.write(attr + ": " + str(args.instance[attr]) + '\n')
    
    """Run optimizer with different sets of hyperparameters and save the results"""
    args.selection_operator = selection_operator
    args.mutation_operator = mutation_operator
    args.fitness_function = fitness_function
    args.termination_check = termination_check
    args.alpha = alpha
    args.mutation_factor = mutation_factors[1]
    args.mutation_potency = mutation_potencies[0]
    args.minimum_epochs = minimum_epochs
    args.selection_factor = selection_factors[1]
    args.maximum_epochs = maximum_epochs_list[1]

    for crossover_operator in crossover_operators:
        args.crossover_operator = crossover_operator

    for selection_factor in selection_factors:
        args.selection_factor = selection_factor

    for maximum_epochs in maximum_epochs_list:
        args.maximum_epochs = maximum_epochs


