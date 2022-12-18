from .BaseClasses.base_operator import CrossoverOperator
from copy import deepcopy

class ArithmeticCrossover(CrossoverOperator):
    def run(self) -> list:
        """Produce a set of child states by crossover of input population"""
        
        offsprings = []
        for i in range(len(self.optimizer.population)):
            for j in range(i+1, len(self.optimizer.population)):
                stateA = self.optimizer.population[i]
                stateB = self.optimizer.population[j]
                scoreA = self.optimizer.fitness_function.evaluate(stateA)
                scoreB = self.optimizer.fitness_function.evaluate(stateB)
                if scoreA >= scoreB:
                    parentA = stateA
                    parentB = stateB
                else:
                    parentA = stateB
                    parentB = stateA
                offspring = {}
                alpha = self.optimizer.alpha
                for _ in range(self.optimizer.branching_factor):
                    for attr in parentA:
                        if attr != 'id':
                            offspring[attr] = alpha * parentA[attr] + \
                                              (1-alpha) * parentB[attr]
                    self.optimizer.state_id_counter += 1
                    offspring['id'] = self.optimizer.state_id_counter
                    offsprings.append(deepcopy(offspring))
        return offsprings