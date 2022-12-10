from base_operator import CrossoverOperator

class SingleArithmeticCrossover(CrossoverOperator):
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
                    if attr != 'id' and self.isnumber(str(parentA[attr])) and attr in configurables and mutated == False:
                        offspringA[attr] = alpha * float(parentA[attr]) + (1-alpha) * float(parentB[attr])
                        mutated = True
                    else:
                        offspringA[attr] = parentA[attr]
                mutated = False
                for attr in parentB:
                    if attr != 'id' and self.isnumber(str(parentB[attr])) and attr in configurables and mutated == False:
                        offspringB[attr] = alpha * float(parentA[attr]) + (1-alpha) * float(parentB[attr])
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