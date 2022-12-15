from .BaseClasses.termination_check import TerminationCheck

class StandardTermination(TerminationCheck):
    def check(self, state) -> bool:
        """
        Terminate when maximum number of epochs were run
        """
        if self.optimizer.epochs == self.optimizer.maximum_epochs - 1:
            return True
        return False