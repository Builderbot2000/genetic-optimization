from base_operator import CrossoverOperator
import random

class IntermediateCrossover(CrossoverOperator):
    def isnumber(self, num):
        try:
            float(num)
            return True
        except ValueError:
            return False

    def run(self) -> list:
        """Produce a set of child states by crossover of input population"""
        configurables = self.optimizer.configurables
        offsprings = []
        for parentA in self.optimizer.population:
            for parentB in self.optimizer.population:
                offspringA = {}
                offspringB = {}
                alpha = self.optimizer.alpha
                for attr in parentA:
                    if attr != 'id' and self.isnumber(str(parentA[attr])) and attr in configurables:
                        rand = random.uniform(0, 1)
                        offspringA[attr] = float(parentA[attr]) + alpha * rand * (float(parentB[attr]) - float(parentA[attr]))
                    else:
                        offspringA[attr] = parentA[attr]
                for attr in parentB:
                    if attr != 'id' and self.isnumber(str(parentB[attr])) and attr in configurables:
                        rand = random.uniform(0, 1)
                        offspringB[attr] = float(parentA[attr]) + alpha * rand * (float(parentB[attr]) - float(parentA[attr]))
                    else:
                        offspringB[attr] = parentB[attr]
                self.optimizer.state_id_counter += 1
                offspringA['id'] = self.optimizer.state_id_counter
                offsprings.append(offspringA)
                self.optimizer.state_id_counter += 1
                offspringB['id'] = self.optimizer.state_id_counter
                offsprings.append(offspringB)
        return offsprings