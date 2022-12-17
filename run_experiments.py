from run_optimizer import parse_instance, SELECTION_OPERATOR, \
                          CROSSOVER_OPERATOR, MUTATION_OPERATOR
from optimizer.optimizer import Optimizer
from optimizer.optimizer import Calculator
from numpy import inf
import argparse
import pandas
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

    """Write instance specifications to experiments/[instance_name].expt.log"""
    if not os.path.exists('output/'):
        os.makedirs('output/')
        
    output_file_path = 'output/' + args.input.split('/')[-1].split('.')[-2] + '.expt.log'
    output_file = open(output_file_path, 'w')
    out = "--- Instance Specifications ---" + '\n'
    for attr in args.instance.keys():
        out += attr + ": " + str(args.instance[attr]) + '\n'
    
    """Run optimizer with different sets of hyperparameters and save the results"""
    args.selection_operator = 'mfs'
    args.mutation_operator = 'ram'
    args.fitness_function = 'sf'
    args.termination_check = 'st'
    args.selection_factor = 50
    args.alpha = 0.5
    args.mutation_factor = 0.5
    args.mutation_potency = 0.4
    args.minimum_epochs = 20
    args.maximum_epochs = 1000

    hyperparameters = {}
    hyperparameters['crossover_operator'] = None
    hyperparameters['selection_factor'] = args.selection_factor
    hyperparameters['mutation_factor'] = args.mutation_factor
    hyperparameters['mutation_potency'] = args.mutation_potency
    hyperparameters['maximum_epochs'] = args.maximum_epochs

    df = pandas.DataFrame(
        columns=['crossover_operator', 'selection_factor', 'mutation_factor', \
                 'mutation_potency', 'maximum_epochs', 'minimum_profit', \
                 'maximum_profit', 'average_profit']
    )

    min_profit = inf
    max_profit = -inf
    sum_profit = 0
    best_results = None

    num_epochs_run = None
    num_states_generated = None
    total_running_time = 0

    experiment_id = 0

    """Experiment 1: Find the best """
    for crossover_operator in ['ic', 'hc', 'ac', 'sac']:
        out += "\n########## Experiment " + str(experiment_id) + " ##########\n"
        args.crossover_operator = crossover_operator
        hyperparameters['crossover_operator'] = crossover_operator
        for _ in range(100):
            op = Optimizer(args)
            if num_states_generated == None:
                best_fit, num_epochs_run, num_states_generated, running_time = op.run()
            else:
                best_fit, _, _, running_time = op.run()
            total_running_time += running_time
            calculator = Calculator(args.instance)
            details, profit = calculator.run(best_fit, more_details=True)
            sum_profit += profit
            if best_results == None or profit > max_profit:
                max_profit = profit
                best_results = details
            if profit < min_profit:
                min_profit = profit

        """Add row containing 100-run statistics to dataframe"""
        avg_profit = sum_profit / 100
        avg_running_time = total_running_time / 100
        df.loc[experiment_id] = [args.crossover_operator, args.selection_factor, \
            args.mutation_factor, args.mutation_potency, args.maximum_epochs, \
            min_profit, max_profit, avg_profit]
        
        """Write 100-run statistics to output_file"""
        out += "\n--- Statistics ---\n"
        out += "num_epochs_run: " + str(num_epochs_run) + '\n'
        out += "num_states_generated: " + str(num_states_generated) + '\n'
        out += "average_running_time: " + str(avg_running_time) + '\n'
        out += "min_profit: " + str(min_profit) + '\n'
        out += "max_profit: " + str(max_profit) + '\n'
        out += "avg_profit: " + str(avg_profit) + '\n'

        out += "\n--- Final Results ---\n"
        for attr in best_results.keys():
            out += attr + ": " + str(best_results[attr]) + '\n'
        out += "profit: " + str(max_profit) + '\n'

    for selection_factor in selection_factors:
        args.selection_factor = selection_factor
        hyperparameters['selection_factor'] = selection_factor

    for maximum_epochs in maximum_epochs_list:
        args.maximum_epochs = maximum_epochs
        hyperparameters['maximum_epochs'] = maximum_epochs

