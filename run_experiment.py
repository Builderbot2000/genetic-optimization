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
    calculator = Calculator(args.instance)

    if not os.path.exists('output/'):
        os.makedirs('output/')
    
    """output_file_path: output/[instance_name].expt.csv"""
    output_file_path = 'output/' + args.input.split('/')[-1].split('.')[-2] + '.expt.csv'
        
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
    args.maximum_epochs = 1000

    df = pandas.DataFrame(
        columns=['crossover_operator', 'selection_factor', 'mutation_factor', \
                 'mutation_potency', 'maximum_epochs', 'minimum_profit', \
                 'maximum_profit', 'average_profit', 'running_time']
    )

    num_data_points = args.maximum_epochs / 100
    experiment_id = 0

    for crossover_operator in crossover_operators:
        args.crossover_operator = crossover_operator

        for mutation_factor in mutation_factors:
            args.mutation_factor = mutation_factor

            for mutation_potency in mutation_potencies:
                args.mutation_potency = mutation_potency

                for i in range(3):
                    args.selection_factor = selection_factors[i]
                    args.branching_factor = branching_factors[i]

                    min_profit = [inf] * 10
                    max_profit = [-inf] * 10
                    sum_profit = [0] * 10

                    num_epochs_run = [None]
                    num_states_generated = [None]
                    total_running_time = []

                    for _ in tqdm(range(100)):
                        op = Optimizer(args)
                        if num_states_generated == None:
                            _, _, _, _, results = op.run()
                        else:
                            _, _, _, _, results = op.run()

                        for j in range(10):
                            total_running_time[j] += results['running_time']
                            num_states_generated[j] = results['num_states_generated']
                            num_epochs_run[j] = results['num_epochs']

                            _, profit = calculator.run(results['current_best_fit'],
                                                       more_details=True)
                            sum_profit[j] += profit
                            if profit > max_profit[j]:
                                max_profit[j] = profit
                            if profit < min_profit[j]:
                                min_profit[j] = profit

                    """Add row containing 100-run statistics to dataframe"""
                    for j in range(10):
                        avg_profit = sum_profit[j] / num_data_points
                        avg_running_time = total_running_time[j] / num_data_points
                        df.loc[experiment_id] = [args.crossover_operator, args.selection_factor, \
                            args.mutation_factor, args.mutation_potency, args.num_epochs[j], \
                            min_profit, max_profit, avg_profit]
                    
                        experiment_id += 1

    df.to_csv(output_file_path, index=False)
