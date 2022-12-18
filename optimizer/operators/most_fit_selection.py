from .BaseClasses.base_operator import SelectionOperator

class MostFitSelection(SelectionOperator):
    def run(self) -> list:
        """
        Select a set of most fit individuals from input population, 
        multiple different fitness scores from the fitness vector 
        can be considered according to given priority
        """

        population = []
        for state in self.optimizer.population:
            state['profit'] = self.optimizer.fitness_function.evaluate(state)
            population.append(state)
        population.sort(key=lambda state: state['profit'], reverse=True)

        best_state = population[0]
        if self.optimizer.current_best_fit == None:
            self.optimizer.current_best_fit = best_state
        elif best_state['profit'] > self.optimizer.current_best_fit['profit']:
            self.optimizer.current_best_fit = best_state
            
        return population[:self.optimizer.selection_factor]