import abc

class TerminationCheck(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'check') and 
        callable(subclass.check) or NotImplemented)

    def __init__(self, optimizer):
        self.optimizer = optimizer

    @abc.abstractmethod
    def check(self, state) -> bool:
        """Input state, output if state satisfies termination conditions"""
        raise NotImplementedError