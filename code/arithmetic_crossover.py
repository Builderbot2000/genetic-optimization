from base_operator import CrossoverOperator
import numbers
import copy

class ArithmeticCrossover(CrossoverOperator):
    def run(self) -> list:
        """Produce a set of child states by crossover of input population"""
        offsprings = []
        for stateA in self.optimizer.population:
            for stateB in self.optimizer.population:
                scoreA = self.optimizer.fitness_function.evaluate(stateA)
                scoreB = self.optimizer.fitness_function.evaluate(stateB)
                if scoreA['profit'] >= scoreB['profit']:
                    parentA = stateA
                    parentB = stateB
                else:
                    parentA = stateB
                    parentB = stateA
                
                offspring = {}
                alpha = self.optimizer.arithmetic_alpha
                for attr in parentA:
                    if attr != 'id' and str(parentA[attr]).isnumeric():
                        offspring[attr] = alpha * float(parentA[attr]) + (1-alpha) * float(parentB[attr])
                    else:
                        offspring[attr] = parentA[attr]
                for i in range(self.optimizer.branching_factor):
                    clone = copy.deepcopy(offspring)
                    self.optimizer.state_id_counter += 1
                    clone['id'] = self.optimizer.state_id_counter
                    offsprings.append(clone)
        return offsprings