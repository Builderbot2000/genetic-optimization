import termination_check

class StandardTermination(termination_check.TerminationCheck):
    def check(self, state) -> bool:
        """Terminate when profit reaches a certain number"""
        score = self.optimizer.fitness_function.evaluate(state)
        if score[self.optimizer.objective] >= 2400 or self.optimizer.epochs == self.optimizer.maximum_epochs - 1:
            self.optimizer.current_best_fit = state
            return True
        else:
            return False