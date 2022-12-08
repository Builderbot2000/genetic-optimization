import termination_check

class StandardTermination(termination_check.TerminationCheck):
    def check(self, state) -> bool:
        """Terminate when profit reaches a certain number"""
        score = self.optimizer.fitness_function.evaluate(state)
        # print(score)
        if score['profit'] == 2000:
            return True
        else:
            return False