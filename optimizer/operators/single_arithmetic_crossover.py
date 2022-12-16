from .BaseClasses.base_operator import CrossoverOperator

class SingleArithmeticCrossover(CrossoverOperator):
    def run(self) -> list:
        """Produce a set of child states by crossover of input population"""
        
        offsprings = []
        for stateA in self.optimizer.population:
            for stateB in self.optimizer.population:
                scoreA = self.optimizer.fitness_function.evaluate(stateA)
                scoreB = self.optimizer.fitness_function.evaluate(stateB)
                if scoreA[self.optimizer.objective] >= scoreB[self.optimizer.objective]:
                    parentA = stateA
                    parentB = stateB
                else:
                    parentA = stateB
                    parentB = stateA
                
                offspringA = {}
                offspringB = {}
                alpha = self.optimizer.alpha
                mutated = False
                for attr in parentA:
                    if attr != 'id' and mutated == False:
                        offspringA[attr] = alpha * parentA[attr] + (1-alpha) * parentB[attr]
                        mutated = True
                    else:
                        offspringA[attr] = parentA[attr]
                mutated = False
                for attr in parentB:
                    if attr != 'id' and mutated == False:
                        offspringB[attr] = alpha * parentA[attr] + (1-alpha) * parentB[attr]
                        mutated = True
                    else:
                        offspringB[attr] = parentB[attr]
                self.optimizer.state_id_counter += 1
                offspringA['id'] = self.optimizer.state_id_counter
                offsprings.append(offspringA)
                self.optimizer.state_id_counter += 1
                offspringB['id'] = self.optimizer.state_id_counter
                offsprings.append(offspringB)
        return offsprings