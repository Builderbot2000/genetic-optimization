from base_operator import SelectionOperator

class MostFitSelection(SelectionOperator):
    def run(self) -> list:
        """
        Select a set of most fit individuals from input population, 
        multiple different fitness scores from the fitness vector 
        can be considered according to given priority
        """
        scores = {}
        for state in self.optimizer.population:
            scores[state['id']] = self.optimizer.fitness_function.evaluate(state)
        self.optimizer.population.sort(key=lambda state: scores[state['id']][self.optimizer.objective], reverse=True)
        return self.optimizer.population[:self.optimizer.selection_factor]