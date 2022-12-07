import abc

class FitnessFunction(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'evaluate') and 
        callable(subclass.run) or NotImplemented)

    @abc.abstractmethod
    def evaluate(self, state, modifiers: list) -> dict:
        """Input state, output fitness score vector"""
        raise NotImplementedError