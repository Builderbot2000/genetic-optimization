from .BaseClasses.base_operator import MutationOperator
import random

class RandomAddMutation(MutationOperator):
    def run(self) -> list:
        """
        Mutate input population by changing some state attribute values
        """
        for state in self.optimizer.population:
            for attr in state:
                if attr != 'id':
                    if random.random() <= self.optimizer.mutation_factor:
                        potency = self.optimizer.mutation_potency
                        range = state[attr] * potency
                        offset = random.uniform(-range, range)
                        while state[attr] + offset < 0:
                            offset = random.uniform(-range, range)
                        state[attr] = state[attr] + offset
        return self.optimizer.population