from .BaseClasses.base_operator import CrossoverOperator
from copy import deepcopy
import random

class IntermediateCrossover(CrossoverOperator):
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
                alpha = self.optimizer.alpha
                for _ in range(self.optimizer.branching_factor):
                    offspring = {}
                    for attr in parentA:
                        if attr != 'id' and attr != 'profit':
                            rand = random.uniform(0, 1)
                            offspring[attr] = parentA[attr] + \
                                              alpha * rand * (parentB[attr] - parentA[attr])
                            if offspring[attr] < 0:
                                offspring[attr] = parentA[attr]
                    self.optimizer.state_id_counter += 1
                    offspring['id'] = self.optimizer.state_id_counter
                    offsprings.append(deepcopy(offspring))
        return offsprings