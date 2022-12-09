from base_operator import MutationOperator
import random
import numbers

class RandomAddMutation(MutationOperator):
    def run(self) -> list:
        """Mutate input population by changing some state attribute values"""
        for state in self.optimizer.population:
            for attr in state:
                if attr != 'id' and str(state[attr]).isnumeric():
                    if random.randint(1,100) < self.optimizer.mutation_factor * 100:
                        potency = self.optimizer.mutation_potency
                        # print("potency: " + str(potency))
                        range = float(state[attr]) * potency
                        # print("range(" + str(-1*range/2) + ", " + str(range/2) + ")")
                        offset = random.uniform(-1*range/2, range/2)
                        # print("offset: " + str(offset))
                        while float(state[attr]) + offset < 0:
                            offset = random.uniform(-1*range/2, range/2)
                        # print("mutated by " + str(offset))
                        state[attr] = str(float(state[attr]) + offset)
        return self.optimizer.population