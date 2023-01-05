from abc import ABC, abstractmethod

from skillbench.data import Team, TeamPair
from skillbench.emulator import Emulator
from typing import Optional, Type, Union

class AcquisitionFunctionNotCompatible(TypeError):
    pass

# Abstract class representing an acquisition function.
# Subclasses should call super().__call__(emulator, teams) to ensure compatibility.
class AcquisitionFunction(ABC):
    @abstractmethod
    def __call__(self, emu: Emulator, teams: TeamPair) -> float:
        "The emulator's desire to know the outcome of this match. The emulator gets given the match it most wants to see"
        if not self.compatible_with(emu):
            raise AcquisitionFunctionNotCompatible(f"Acquisition function {self.name} is not compatible with emulator {emu.name} (compatible emulators: {self.compatible_emulators})")
        pass

    @property
    def name(self) -> str:
        return self.__class__.__name__
    
    @property
    def compatible_emulators(self) -> list[Type[Emulator]]:
        return self.__compatible_emulators__

    def compatible_with(self, emu: Union[Type[Emulator], Emulator]) -> bool:
        if not isinstance(emu, type):
            emu = emu.__class__
        return (not self.compatible_emulators) or (emu in self.compatible_emulators)

# Decorator allows one to specify which Emulators are compatible with this AcquisitionFunction.
def compatible_emulators(*emulators: Type[Emulator]):
    def decorator(cls):
        cls.__compatible_emulators__ = emulators
        return cls
    return decorator