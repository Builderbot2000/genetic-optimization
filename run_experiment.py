from run_optimizer import parse_instance, CROSS_OPS
from optimizer.optimizer import Optimizer
from optimizer.optimizer import Calculator
from numpy import inf
from tqdm import tqdm
import pandas as pd
import argparse
import os

def experiment1(args):
    calculator = Calculator(args.instance)

    if not os.path.exists('output/'):
        os.makedirs('output/')
    
    """Run optimizer with different hyperparameters and write the results to output_file"""
    crossover_operators = ['ic', 'hc', 'sac']
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
    args.maximum_epochs = 1000

    num_data_points_per_run = int(args.maximum_epochs / 100)
    num_runs_per_configuration = 10

    for crossover_operator in crossover_operators:
        args.crossover_operator = crossover_operator

        df = pd.DataFrame(
            columns=['crossover_operator', 'selection_factor', 'branching_factor',
                     'mutation_factor', 'mutation_potency', 'maximum_epochs', 
                     'minimum_profit', 'maximum_profit', 'average_profit', 
                     'num_states_generated', 'avg_running_time']
        )

        for mutation_factor in mutation_factors:
            args.mutation_factor = mutation_factor

            for mutation_potency in mutation_potencies:
                args.mutation_potency = mutation_potency

                for i in range(len(selection_factors)):
                    args.selection_factor = selection_factors[i]
                    args.branching_factor = branching_factors[i]

                    min_profit = [inf] * num_data_points_per_run
                    max_profit = [-inf] * num_data_points_per_run
                    sum_profit = [0] * num_data_points_per_run

                    num_epochs_run = [None] * num_data_points_per_run
                    num_states_generated = [None] * num_data_points_per_run
                    total_running_time = [0] * num_data_points_per_run

                    for _ in tqdm(range(num_runs_per_configuration)):
                        op = Optimizer(args)
                        if num_states_generated == None:
                            _, _, _, _, results = op.run()
                        else:
                            _, _, _, _, results = op.run()

                        for j in range(num_data_points_per_run):
                            total_running_time[j] += results[j]['running_time']
                            num_states_generated[j] = results[j]['num_states_generated']
                            num_epochs_run[j] = results[j]['num_epochs']

                            profit = results[j]['current_best_fit']['profit']

                            sum_profit[j] += profit
                            if profit > max_profit[j]:
                                max_profit[j] = profit
                            if profit < min_profit[j]:
                                min_profit[j] = profit

                    """Add row containing statistics of 100 runs to dataframe"""
                    for j in range(num_data_points_per_run):
                        avg_profit = sum_profit[j] / num_runs_per_configuration
                        avg_running_time = total_running_time[j] / num_runs_per_configuration

                        df.loc[len(df)] = [CROSS_OPS[args.crossover_operator],
                            args.selection_factor, args.branching_factor, args.mutation_factor,
                            args.mutation_potency, num_epochs_run[j], min_profit[j], max_profit[j], avg_profit, num_states_generated[j], avg_running_time]
                    
        """output_file_path: output/[instance_name].expt1.log"""
        output_file_path = 'output/' + args.input.split('/')[-1].split('.')[-2] + '.expt1.' + \
            args.crossover_operator + '.csv'
        df.to_csv(output_file_path)


if __name__ == '__main__':
    DEFAULT_INSTANCE = "instances/wafer.log"
    DEFAULT_EXPERIMENT = 1

    parser = argparse.ArgumentParser(
      description="Runs genetic optimizer for a set of numerical configurations \
                   with different sets of hyperparameters"
    )

    parser.add_argument('--input', type=str, default=DEFAULT_INSTANCE,
                        help="The path of the input file, defaults to " +
                              str(DEFAULT_INSTANCE))

    parser.add_argument('--experiment', type=str, default=DEFAULT_EXPERIMENT)

    args = parser.parse_args()
    args.instance = parse_instance(args.input)
    if args.experiment == 1:
        experiment1(args)
