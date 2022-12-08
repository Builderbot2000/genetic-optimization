from base_operator import SelectionOperator

class MostFitSelection(SelectionOperator):
    def run(self) -> list:
        """
        Select a set of most fit individuals from input population, 
        multiple different fitness scores from the fitness vector 
        can be considered according to given priority
        """
        # Your implementation here
        return self.optimizer.population