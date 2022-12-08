from base_operator import CrossoverOperator

class LinearCrossover(CrossoverOperator):
    def run(self) -> list:
        """Produce a set of child states by crossover of input population"""
        # Your implementation here
        return self.optimizer.population