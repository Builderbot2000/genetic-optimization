from base_operator import MutationOperator

class RandomAddMutation(MutationOperator):
    def run(self) -> list:
        """Mutate input population by changing some state attribute values"""
        # Your implementation here
        return self.optimizer.population