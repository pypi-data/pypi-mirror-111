"""Base classes for all models"""

# Author: Koji Noshita <noshita@morphometrics.jp>
# License: ISC

from abc import ABCMeta, abstractmethod

from . import __version__

##
## Theoretical morphological models
##

class BaseModel(metaclass=ABCMeta):
#     @abstractmethod
    def set_params(self):
        pass

#     @abstractmethod
    def get_params(self):
        pass
    
class GeneratingCurveModel(BaseModel):
    """Base class for all generating curve models in kaigara."""
    
    @abstractmethod
    def _generate_generating_spiral(self):
        """
        Call this function via `compute_generating_spiral` (in `Simulator`) 
        or `calculate_generating_spiral` (in `Eqns`).
        """
        pass

class GSGCModel(BaseModel):
    """Base class for all generating spiral and generating curve models in kaigara."""
    
    @abstractmethod
    def _generate_generating_spiral(self):
        """
        Call this function via `compute_generating_spiral` (in `Simulator`) 
        or `calculate_generating_spiral` (in `Eqns`).
        """
        pass    

    @abstractmethod
    def _generate_generating_curve(self):
        """
        Call this function via `compute_generating_curve` (in `Simulator`) 
        or `calculate_generating_curve` (in `Eqns`).
        """
        pass    

    @property
    @abstractmethod
    def position(self):
        """
        A position vector of the model in a global coordinate system (p_0)
        """
        pass

    @property
    @abstractmethod
    def orientation(self):
        """
        An orientation matrix of the model in a global coordinate system (xi_{1,0}, xi_{2,0}, xi_{3,0})
        """
        pass

    @property
    @abstractmethod
    def size(self):
        """
        Size of the model in a global coordinate system (r_0)
        """
        pass

class HSModel(BaseModel):
    """Base class for all generating helicospiral models in kaigara."""
    
    @abstractmethod
    def _generate_helico_spirals(self):
        """
        Call this function via `compute_generating_spiral` (in `Simulator`) 
        or `calculate_generating_spiral` (in `Eqns`).
        """
        pass     

    @property
    @abstractmethod
    def position(self):
        """
        A position vector of the model in a global coordinate system (p_0)
        """
        pass

    @property
    @abstractmethod
    def orientation(self):
        """
        An orientation matrix of the model in a global coordinate system (xi_{1,0}, xi_{2,0}, xi_{3,0})
        """
        pass

    @property
    @abstractmethod
    def size(self):
        """
        Size of the model in a global coordinate system (r_0)
        """
        pass

##
## Model Parameters
##
class BaseModelParameter(metaclass=ABCMeta):
    """
    Descriptor class for model parameters
    """
    @abstractmethod
    def __get__(self):
        pass

    @abstractmethod
    def __set__(self):
        pass

##
## Mixins
##

class SimulatorMixin:
    """Mixin class for all simulators in kaigara."""
    @abstractmethod
    def compute(self):
        pass

class EqnsMixin:
    """Mixin class for all equations in kaigara."""
    
    @property
    @abstractmethod
    def definition(self):
        """
        """
        pass
    
#     @abstractmethod
#     def solve(self):
#         pass
    
    @abstractmethod
    def to_tex(self):
        pass
