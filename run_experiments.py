from run_optimizer import run_optimizer, SELECTION_OPERATOR, \
                          CROSSOVER_OPERATOR, MUTATION_OPERATOR

if __name__ == '__main__':
    selection_operator = 'mfs'
    crossover_operator = ['ic','hc','ac','sac']
    mutation_operator = 'ram'
    fitness_function = 'sf'
    termination_check = 'st'

    selection_factors = {20, 50, 100}
    branching_factor = {2, 4, 6}
    alpha = 0.5
    mutation_factor = {0.2, 0.5, 1.0}
    mutation_potency = {0.4, 0.6, 0.8}
    minimum_epochs = 10
    maximum_epochs = {100, 500, 1000}


