from .BaseClasses.fitness_function import FitnessFunction

class StandardFitness(FitnessFunction):    
    def evaluate(self, state) -> dict:
        """Evaluate and return the fitness scores of a state"""
        
        profit = self.optimizer.calculator.run(state)
        return profit