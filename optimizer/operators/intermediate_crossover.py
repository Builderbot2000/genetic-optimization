from .BaseClasses.base_operator import CrossoverOperator
import random

class IntermediateCrossover(CrossoverOperator):
    def run(self) -> list:
        """Produce a set of child states by crossover of input population"""
        
        offsprings = []
        for parentA in self.optimizer.population:
            for parentB in self.optimizer.population:
                offspringA = {}
                offspringB = {}
                alpha = self.optimizer.alpha
                for attr in parentA:
                    if attr != 'id':
                        rand = random.uniform(0, 1)
                        offspringA[attr] = parentA[attr] + alpha * rand * (parentB[attr] - parentA[attr])
                    else:
                        offspringA[attr] = parentA[attr]
                for attr in parentB:
                    if attr != 'id':
                        rand = random.uniform(0, 1)
                        offspringB[attr] = parentA[attr] + alpha * rand * (parentB[attr] - parentA[attr])
                    else:
                        offspringB[attr] = parentB[attr]
                self.optimizer.state_id_counter += 1
                offspringA['id'] = self.optimizer.state_id_counter
                offsprings.append(offspringA)
                self.optimizer.state_id_counter += 1
                offspringB['id'] = self.optimizer.state_id_counter
                offsprings.append(offspringB)
        return offsprings