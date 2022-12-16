from optimizer.optimizer import Optimizer
from optimizer.calculator import Calculator
import argparse

if __name__ == '__main__':
    """Input files should be put under instances/"""
    DEFAULT_INSTANCE = "instances/wafer.instance"
    DEFAULT_LOGFILE = "results/log.txt"

    DEFAULT_SELECTION_OPERATOR = "mfs"      # mps - most fit selection
    DEFAULT_CROSSOVER_OPERATOR = "ic"       # lc - linear crossover
    DEFAULT_MUTATION_OPERATOR = "ram"       # ram - random add mutation
    DEFAULT_FITNESS_FUNCTION = "sf"         # sf - standard fitness
    DEFAULT_TERMINATION_CHECK = "st"        # st - standard termination

    DEFAULT_SELECTION_FACTOR = 50
    DEFAULT_BRANCHING_FACTOR = 2
    DEFAULT_ALPHA = 0.5
    DEFAULT_MUTATION_FACTOR = 1.0
    DEFAULT_MUTATION_POTENCY = 0.4
    DEFAULT_MINIMUM_EPOCHS = 10
    DEFAULT_MAXIMUM_EPOCHS = 100

    """Run experiment here"""
    parser = argparse.ArgumentParser(description='Runs genetic optimizer for a set of numerical configurations')
    parser.add_argument('--input', type=str, default=DEFAULT_INSTANCE,
                        help="The path of the input file, defaults to " +
                              str(DEFAULT_INSTANCE))
    parser.add_argument('--log', type=str, default=DEFAULT_LOGFILE,
                        help="The path of the log file, defaults to " +
                              str(DEFAULT_INSTANCE))
    parser.add_argument('--selection_operator', type=str, default=DEFAULT_SELECTION_OPERATOR,
                        help='The selection operator to use, defaults to ' +
                              str(DEFAULT_SELECTION_OPERATOR))
    parser.add_argument('--crossover_operator', type=str, default=DEFAULT_CROSSOVER_OPERATOR,
                        help='The crossover operator to use, should be within interval [0, 1], \
                              defaults to ' + str(DEFAULT_CROSSOVER_OPERATOR))
    parser.add_argument('--mutation_operator', type=str, default=DEFAULT_MUTATION_OPERATOR,
                        help='The mutation operator to use, defaults to ' +
                              str(DEFAULT_MUTATION_OPERATOR))
    parser.add_argument('--fitness_function', type=str, default=DEFAULT_FITNESS_FUNCTION,
                        help='The fitness function to use, defaults to ' +
                              str(DEFAULT_FITNESS_FUNCTION))   
    parser.add_argument('--termination_check', type=str, default=DEFAULT_TERMINATION_CHECK,
                        help='The function used to determine the terminating condition, \
                              defaults   to ' + str(DEFAULT_TERMINATION_CHECK)) 
    parser.add_argument('--selection_factor', type=int, default=DEFAULT_SELECTION_FACTOR,
                        help='How many states to select from top k most fitting states, \
                              defaults to ' + str(DEFAULT_SELECTION_FACTOR))     
    parser.add_argument('--branching_factor', type=int, default=DEFAULT_BRANCHING_FACTOR,
                        help='How many child states are produced by two parents, defaults to ' +
                              str(DEFAULT_BRANCHING_FACTOR))
    parser.add_argument('--alpha', type=int, default=DEFAULT_MUTATION_FACTOR,
                        help='Value of the alpha parameter used in crossover operators, \
                              defaults to ' + str(DEFAULT_ALPHA))  
    parser.add_argument('--mutation_factor', type=float, default=DEFAULT_MUTATION_FACTOR,
                        help='How likely a state attribute is mutated, defaults to ' + 
                              str(DEFAULT_MUTATION_FACTOR))  
    parser.add_argument('--mutation_potency', type=float, default=DEFAULT_MUTATION_POTENCY,
                        help='Maximum of how much of a state can be mutated , defaults to ' + 
                              str(DEFAULT_MUTATION_POTENCY))  
    parser.add_argument('--minimum_epochs', type=int, default=DEFAULT_MINIMUM_EPOCHS,
                        help='Optimizer must run this many epochs before terminating, \
                              defaults to ' + str(DEFAULT_MINIMUM_EPOCHS))        
    parser.add_argument('--maximum_epochs', type=int, default=DEFAULT_MAXIMUM_EPOCHS,
                        help='Optimizer must terminate once it has run this many epochs, \
                              defaults to ' + str(DEFAULT_MAXIMUM_EPOCHS))         
                    
    args = parser.parse_args()

    op = Optimizer(args)
    op.load()
    instance, best_fit, num_states_generated,running_time = op.run()

    """Log the results"""
    log_file = open(args.log, 'w')
    log = "--- Nonconfigurables  ---\n"
    for attr in instance:
        log += attr + ": " + str(round(instance[attr], 2)) + '\n'

    log += "\n--- Final Configurables --\n"
    for attr in best_fit:
        log += attr + ": " + str(round(best_fit[attr], 2)) + '\n'

    log += "\n--- Final results ---\n"
    calculator = Calculator(instance)
    (workforce_skill_level, product_improvement, product_quality, marketing_coverage, \
     percentage_satisfied), (quantity_produced, revenue, equipment_cost, worker_cost, \
                             environmental_cost), profit = calculator.run(best_fit, details=True)
    log += "workforce_skill_level: " + str(round(workforce_skill_level, 2)) + '\n'
    log += "product_improvement: " + str(round(product_improvement, 2)) + '\n'
    log += "product_quality: " + str(round(product_quality, 2)) + '\n'
    log += "market_coverage: " + str(round(marketing_coverage, 2)) + '\n'
    log += "percentage_satisfied_with_price_quality: " + \
           str(round(percentage_satisfied, 2)) + '\n'
    log += "quantity_produced: " + str(round(quantity_produced, 2)) + '\n'
    log += "revenue: " + str(round(revenue, 2)) + '\n'
    log += "equipment_cost: " + str(round(equipment_cost, 2)) + '\n'
    log += "worker_cost: " + str(round(worker_cost, 2)) + '\n'
    log += "environmental_cost: " + str(round(environmental_cost, 2)) + '\n'
    log += "profit: " + str(round(profit, 2)) + '\n'

    log += "\n--- Execution Details ---\n"
    log += "epochs ran: " + str(args.maximum_epochs) + "\n"
    log += "running_time: " + str(round(running_time, 2)) + '\n'
    log += "total states generated: " + str(num_states_generated) + "\n"

    log += "\n--- Optimizer Info ---\n"
    log += "selection factor: " + str(args.selection_factor) + "\n"
    log += "alpha: " + str(args.alpha) + "\n"
    log += "mutation factor: " + str(args.mutation_factor) + "\n"
    log += "mutation potency: " + str(args.mutation_potency) + "\n"
    log += "minimum epochs: " + str(args.minimum_epochs) + "\n"
    log += "maximum epochs: " + str(args.maximum_epochs) + "\n"
    log += "selection operator: " + args.selection_operator + "\n"
    log += "crossover operator: " + args.crossover_operator + "\n"
    log += "mutation operator: " + args.mutation_operator + "\n"

    log_file.write(log)
    log_file.close()
