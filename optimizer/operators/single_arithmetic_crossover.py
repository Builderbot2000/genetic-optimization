from .BaseClasses.base_operator import CrossoverOperator
from random import randint
from copy import deepcopy

class SingleArithmeticCrossover(CrossoverOperator):
    def run(self) -> list:
        """Produce a set of child states by crossover of input population"""
        
        offsprings = []
        for i in range(len(self.optimizer.population)):
            for j in range(i+1, len(self.optimizer.population)):
                stateA = self.optimizer.population[i]
                stateB = self.optimizer.population[j]
                if stateA['profit'] >= stateB['profit']:
                    parentA = stateA
                    parentB = stateB
                else:
                    parentA = stateB
                    parentB = stateA
                offspring = {}
                alpha = self.optimizer.alpha
                if alpha > 1:
                    exit("arithmetic_crossover does not allow alpha > 1")
                attrs = []
                for attr in parentA:
                    if attr != 'id' and attr != 'profit':
                        attrs.append(attr)
                for _ in range(self.optimizer.branching_factor):
                    for attr in parentA:
                        if attr != 'id' and attr != 'profit':
                            offspring[attr] = parentA[attr]
                    mut_attr = attrs[randint(0, len(attrs)-1)]
                    offspring[mut_attr] = parentB[mut_attr] + \
                                          alpha * (parentA[mut_attr] - parentB[mut_attr])
                    self.optimizer.state_id_counter += 1
                    offspring['id'] = self.optimizer.state_id_counter
                    offsprings.append(deepcopy(offspring))
        return offsprings