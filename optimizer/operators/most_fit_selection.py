from .BaseClasses.base_operator import SelectionOperator
from copy import deepcopy

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
        self.optimizer.population.sort(key=lambda state: scores[state['id']], reverse=True)
        best_state = self.optimizer.population[0]
        best_score = scores[best_state['id']]
        if best_score > self.optimizer.current_best_score:
            self.optimizer.current_best_fit = deepcopy(best_state)
            self.optimizer.current_best_score = best_score
        return self.optimizer.population[:self.optimizer.selection_factor]