import termination_check

class StandardTermination(termination_check.TerminationCheck):
    def check(self, state) -> bool:
        score = self.optimizer.fitness_function.evaluate(state)
        # print(score)