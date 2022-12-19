from .BaseClasses.base_operator import CrossoverOperator
from random import randint
from copy import deepcopy

class SingleArithmeticCrossover(CrossoverOperator):
    def run(self) -> list:
        """Produce a set of child states by crossover of input population"""
        
        offsprings = []
        for i in range(len(self.optimizer.population)):
            for j in range(i+1, len(self.optimizer.population)):
                parentA = self.optimizer.population[i]
                parentB = self.optimizer.population[j]
                alpha = self.optimizer.alpha
                if alpha > 1:
                    exit("arithmetic_crossover does not allow alpha > 1")
                attrs = []
                for attr in parentA:
                    if attr != 'id' and attr != 'profit':
                        attrs.append(attr)
                for _ in range(int(self.optimizer.branching_factor/2)):
                    offspring1 = {}
                    offspring2 = {}
                    for attr in parentA:
                        if attr != 'id' and attr != 'profit':
                            offspring1[attr] = parentA[attr]
                            offspring2[attr] = parentA[attr]
                    mut_attr = attrs[randint(0, len(attrs)-1)]
                    offspring1[mut_attr] = parentB[mut_attr] + \
                                          alpha * (parentA[mut_attr] - parentB[mut_attr])
                    offspring1[mut_attr] = parentA[mut_attr] + \
                                          alpha * (parentB[mut_attr] - parentA[mut_attr])
                    self.optimizer.state_id_counter += 1
                    offspring1['id'] = self.optimizer.state_id_counter
                    self.optimizer.state_id_counter += 1
                    offspring2['id'] = self.optimizer.state_id_counter
                    offsprings.append(deepcopy(offspring1))
                    offsprings.append(deepcopy(offspring2))
        return offsprings