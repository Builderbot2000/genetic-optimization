from .BaseClasses.base_operator import CrossoverOperator
from copy import deepcopy

class SingleArithmeticCrossover(CrossoverOperator):
    def run(self) -> list:
        """Produce a set of child states by crossover of input population"""
        
        offsprings = []
        for i in range(len(self.optimizer.population)):
            for j in range(i+1, len(self.optimizer.population)):
                stateA = self.optimizer.population[i]
                stateB = self.optimizer.population[j]
                scoreA = self.optimizer.fitness_function.evaluate(stateA)
                scoreB = self.optimizer.fitness_function.evaluate(stateB)
                if scoreA[self.optimizer.objective] >= scoreB[self.optimizer.objective]:
                    parentA = stateA
                    parentB = stateB
                else:
                    parentA = stateB
                    parentB = stateA
                offspring = {}
                alpha = self.optimizer.alpha
                mutated = False
                for _ in range(self.optimizer.branching_factor):
                    for attr in parentA:
                        if attr != 'id' and mutated == False:
                            offspring[attr] = parentB[attr] + \
                                              alpha * (parentA[attr] - parentB[attr])
                            mutated = True
                    self.optimizer.state_id_counter += 1
                    offspring['id'] = self.optimizer.state_id_counter
                    offsprings.append(deepcopy(offspring))
        return offsprings