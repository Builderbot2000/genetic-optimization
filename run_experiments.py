from run_optimizer import parse_instance, SEL_OPS, CROSS_OPS, MUT_OPS
from optimizer.optimizer import Optimizer
from optimizer.optimizer import Calculator
from numpy import inf
from tqdm import tqdm
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

    """Write instance specifications to output_file"""
    if not os.path.exists('output/'):
        os.makedirs('output/')
        
    """output_file path: output/[instance_name].expt.log"""
    output_file_path = 'output/' + args.input.split('/')[-1].split('.')[-2] + '.expt.log'
    output_file = open(output_file_path, 'w')
    out = "--- Instance Specifications ---" + '\n'
    for attr in args.instance.keys():
        out += attr + ": " + str(args.instance[attr]) + '\n'
    
    """Run optimizer with different hyperparameters and write the results to output_file"""
    crossover_operators = ['ic', 'hc', 'ac', 'sac']
    selection_factors = [15, 35, 85]
    branching_factors = [68, 12, 2]
    mutation_factors = [0.5, 1.0]
    mutation_potencies = [0.4, 0.8]

    args.selection_operator = 'mfs'
    args.mutation_operator = 'ram'
    args.fitness_function = 'sf'
    args.termination_check = 'st'
    args.alpha = 0.5
    args.minimum_epochs = 10
    args.maximum_epochs = 10000

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

    for crossover_operator in crossover_operators:
        args.crossover_operator = crossover_operator

        for mutation_factor in mutation_factors:
            for mutation_potency in mutation_potencies:
                for i in range(3):
                    args.selection_factor = selection_factors[i]
                    args.branching_factor = branching_factors[i]

                    out += "\n########## Experiment " + str(experiment_id) + " ##########\n"
                    for _ in tqdm(range(100)):
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
                    
                    """Write 100-run statistics to output_file"""
                    out += "\n--- Statistics ---\n"
                    out += "num_epochs_run: " + str(num_epochs_run) + '\n'
                    out += "num_states_generated: " + str(num_states_generated) + '\n'
                    out += "average_running_time: " + str(avg_running_time) + '\n'
                    out += "min_profit: " + str(min_profit) + '\n'
                    out += "max_profit: " + str(max_profit) + '\n'
                    out += "avg_profit: " + str(avg_profit) + '\n'

                    out += "\n--- Best Results ---\n"
                    for attr in best_results.keys():
                        out += attr + ": " + str(best_results[attr]) + '\n'
                    out += "profit: " + str(max_profit) + '\n'

                    out += "\n########## End" + str(experiment_id) + " ##########\n"

                    experiment_id += 1

    output_file.write(out)
    output_file.close()
    
    output_file_path = 'output/' + args.input.split('/')[-1].split('.')[-2] + '.expt.csv'
    df.to_csv(output_file_path)
