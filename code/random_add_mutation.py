from base_operator import MutationOperator
import random

class RandomAddMutation(MutationOperator):
    def isnumber(self, num):
        try:
            float(num)
            return True
        except ValueError:
            return False
    
    def run(self) -> list:
        """Mutate input population by changing some state attribute values"""
        configurables = self.optimizer.configurables
        for state in self.optimizer.population:
            for attr in state:
                if attr != 'id' and self.isnumber(str(state[attr])) and attr in configurables:
                    if random.randint(1,100) <= self.optimizer.mutation_factor * 100:
                        potency = self.optimizer.mutation_potency
                        range = float(state[attr]) * potency
                        offset = random.uniform(-1*range/2, range/2)
                        while float(state[attr]) + offset < 0:
                            offset = random.uniform(-1*range/2, range/2)
                        state[attr] = str(float(state[attr]) + offset)
        return self.optimizer.population