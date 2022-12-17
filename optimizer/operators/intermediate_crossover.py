from .BaseClasses.base_operator import CrossoverOperator
from copy import deepcopy
import random

class IntermediateCrossover(CrossoverOperator):
    def run(self) -> list:
        """Produce a set of child states by crossover of input population"""
        
        offsprings = []
        for i in range(len(self.optimizer.population)):
            for j in range(i+1, len(self.optimizer.population)):
                parentA = self.optimizer.population[i]
                parentB = self.optimizer.population[j]
                offspring = {}
                alpha = self.optimizer.alpha
                for _ in range(self.optimizer.branching_factor):
                    for attr in parentA:
                        if attr != 'id':
                            rand = random.uniform(0, 1)
                            offspring[attr] = parentA[attr] + \
                                              alpha * rand * (parentB[attr] - parentA[attr])
                    self.optimizer.state_id_counter += 1
                    offspring['id'] = self.optimizer.state_id_counter
                    offsprings.append(deepcopy(offspring))
        return offsprings