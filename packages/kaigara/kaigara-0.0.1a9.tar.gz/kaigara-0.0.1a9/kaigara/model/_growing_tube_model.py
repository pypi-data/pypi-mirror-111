"""Growing Tube model"""

# Author: Koji Noshita <noshita@morphometrics.jp>
# License: ISC

import numbers, copy

import numpy as np
import sympy as sym

from scipy.spatial.transform import Rotation
import scipy.integrate as solve_ivp

from ..base import GSGCModel, SimulatorMixin, EqnsMixin, BaseModelParameter

##
## Model parameters
## 
def __deco_func(func, wrap_func):
    if callable(func):
        def wrapper(*args, **kwargs):
            return wrap_func(func(*args, **kwargs))
        return wrapper
    else:
        return wrap_func(func)

def __logdeco(func):
    return __deco_func(func, np.log)
    

# Egt, Cgt, Tgtはそのうちまとめる（GTModelParameter）．
# descriptorによる実装．
#　Okamoto1988へのEgtの変換はGTモデル側で実装する方が良さそう．

class GTModelParameter(BaseModelParameter):
    __counter = 0
    def __init__(self, param_name = None):
        cls = self.__class__
        index = cls.__counter
        if param_name is None:
            prefix = cls.__name__
            self.param_name = '_{}#{}'.format(prefix, index)
        else:
            self.param_name = '_{}#{}'.format(param_name, index)
        cls.__counter += 1
#         self.param_name = {param_name}
        
    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            return getattr(instance, self.param_name)
    
    def __set__(self, instance, param_input):
        if callable(param_input):
            instance.__dict__[self.param_name] = copy.copy(param_input)
        elif isinstance(param_input,  (numbers.Real, list, tuple, np.ndarray)) and np.isfinite(param_input).all():
            instance.__dict__[self.param_name] = np.asarray(param_input)
        else:
            raise ValueError("{} is a real number (of numpy.ndarray) or function, in the range (-inf, inf).".format(self.param_name))



##
## Simulator
##
class GrowingTubeModelSimulator(GSGCModel, SimulatorMixin):
    """Growing Tube Model Simulator
    Parameters:
        E: float, array-like; shape (n,), or callable
        C: float, array-like; shape (n,), or callable
        T: float, array-like; shape (n,), or callable
        r0: float, optional
        p0: array-like; shape (3,), optional
        R0: array-like; shape (3,3), optional
    """
#     E = Egt()
#     C = Cgt()
#     T = Tgt()
    E = GTModelParameter("E")
    C = GTModelParameter("C")
    T = GTModelParameter("T")
    def __init__(self, E, C, T, 
                 r0 = 1, p0 = np.zeros(3), R0 = np.diag(np.ones(3))
                ):
        
        print(E)
        self.E = E
        self.C = C
        self.T = T
        self.r0 = r0
        self.__p0 = p0
        self.__R0 = R0
        
    def __normalize(self, vec):
        norm = np.linalg.norm(vec)
        return vec/norm
    
    @property
    def E_Okamoto1988(self):
        if callable(self.E):
            return __deco_func(self.E, np.exp)
        else:
            return np.exp(self.E)
        
    @E_Okamoto1988.setter
    def E_Okamoto1988(self, E_Okamoto1988):
        if callable(E_Okamoto1988):
            self.E = __deco_func(E_Okamoto1988, np.log)
        else:
            self.E = np.log(E_Okamoto1988)
     
    @property
    def r0(self):
        return self.__r0
    
    @r0.setter
    def r0(self, r0):
        if isinstance(r0, numbers.Real)  and r0 > 0:
            self.__r0 = r0
        else:
            raise ValueError("r0 is a finite positive real number.")

    @property
    def size(self):
        return self.__r0

    @size.setter
    def size(self, r0):
        self.r0 = r0

    @property
    def p0(self):
        return self.__p0

    @p0.setter
    def p0(self, p0):
        print(p0)
        p0_arr = p0
        if len(p0_arr) == 3 and np.all(np.isfinite(p0_arr)):
            self.__p0 = p0_arr
        else:
            raise ValueError("p0 is a positional vector (R^3)")

    @property
    def position(self):
        return self.__p0

    @position.setter
    def position(self, p0):
        self.p0 = p0
    
    @property
    def R0(self):
        return self.__R0
    
    @R0.setter
    def R0(self, R0):
        R0_arr = np.array(R0)
        
        if np.array_equal(np.linalg.inv(R0_arr), R0_arr.transpose()) & (np.linalg.det(R0_arr) == 1):
            self.__R0 = R0
        else:
            raise ValueError("R0 is a rotation matrix.")

    @property
    def orientation(self):
        return self.__R0

    @orientation.setter
    def orientation(self, R0):
        self.R0 = R0


    def _generate_generating_spiral(self, s):
        
        E_g = self.E
        C_g = self.C
        T_g = self.T


        if isinstance(E_g, numbers.Real) and callable(C_g) and callable(T_g):
            raise RuntimeError("!!Not Implimented Yet: E is const.!!")
            
        elif callable(E_g) | callable(C_g) | callable(T_g):
            raise RuntimeError("!!Not Implimented Yet!!: at least a parameter is callable.")

#         elif isinstance(E_g, numbers.Real) & isinstance(C_g, numbers.Real) & isinstance(T_g, numbers.Real):
        elif (E_g.ndim == 0) & (C_g.ndim == 0) & (T_g.ndim == 0):
            PMat = self._generate_generating_spiral_const_ECT(s)
            
        else:
            raise ValueError("E_g, C_g, and T_g must be callable or constant values.")

        return PMat


    def _generate_generating_spiral_const_ECT(self, s):
        E_g = self.E
        C_g = self.C
        T_g = self.T
        r0 = self.r0
        p0 = self.p0
        R0 = self.R0

        r = r0*np.exp(E_g*s)
        D = np.sqrt(C_g**2+T_g**2)
        
        ED3E2pD2 = E_g*D**3*(E_g**2 + D**2)
        expEs = np.exp(E_g*s)
        sinDs = np.sin(D*s)
        cosDs = np.cos(D*s)
    

        P = r0*D*(((D**2) * (T_g**2) + (E_g**2) * (T_g**2) + C_g**2 * E_g**2 * cosDs 
                   + E_g*D*(C_g**2)*sinDs)*expEs - D**2 * (E_g**2 + T_g**2))/ED3E2pD2
        Q = r0*C_g*D*E_g*(-expEs*(C_g**2 + T_g**2)*cosDs 
                          + D*(D + expEs*E_g*sinDs))/ED3E2pD2
        R = r0*C_g*T_g*D*(((E_g**2) + (D**2) - (E_g**2) * cosDs - E_g*D*sinDs)*expEs - D**2)/ED3E2pD2

        PMat = p0 + np.transpose(np.dot(R0, np.array([P, Q, R])))
        
        return PMat

    def _generate_generating_spiral_const_E(self, s):

        E_g = self.E
        C_g = self.C
        T_g = self.T
        r0 = self.r0
        p0 = self.p0
        R0 = self.R0

        r = r0*np.exp(E_g*s)

        s_span = (0, s)
        
        def Frenet_frame(s):

            return xi_1, xi_2, xi_3

        xi_1, xi_2, xi_3 = solve_ivp(func, s_span, p0)

        coord = lambda s: r0*np.exp(E_g*s)*xi_1(s)

        px, py, pz = solve_ivp(coord, s_span, p0)

        return px, py, pz

    def _Frenet_frame(self):
        E_g = self.E
        C_g = self.C
        T_g = self.T

        D_g = np.sqrt(C_g**2+T_g**2)

        if isinstance(E_g, numbers.Real) and callable(C_g) and callable(T_g):
            raise RuntimeError("!!Not Implimented Yet: E is const.!!")
            
        elif callable(E_g) | callable(C_g) | callable(T_g):
            raise RuntimeError("!!Not Implimented Yet!!: at least a parameter is callable.")

        elif isinstance(E_g, numbers.Real) & isinstance(C_g, numbers.Real) & isinstance(T_g, numbers.Real):
            Xi = np.vectorize(
                lambda s: np.dot(
                    R0,
                    np.array([
                        [(T_g**2 + (C_g**2)*np.cos(D_g*s))/(D_g**2), -(C_g*np.sin(D_g*s))/D_g, C_g*T_g*(1-np.cos(D_g*s))/(D_g**2)],
                        [(C_g*np.sin(D_g*s))/D_g, np.cos(D_g*s)], -(C_g*np.sin(D_g*s))/D_g,
                        [C_g*T_g*(1-np.cos(D_g*s))/(D_g**2), (T_g*np.sin(D_g*s))/D_g,(C_g**2 + (T_g**2)*np.cos(D_g*s))/(D_g**2)]
                        ])
                    )
                )            
        else:
            raise ValueError("E_g, C_g, and T_g must be callable or constant values.")

        return Xi

    def _generate_generating_curve(self, s, phi):
        E_g = self.E
        C_g = self.C
        T_g = self.T

        if isinstance(E_g, numbers.Real) and callable(C_g) and callable(T_g):
            raise RuntimeError("!!Not Implimented Yet: E is const.!!")
            
        elif callable(E_g) | callable(C_g) | callable(T_g):
            raise RuntimeError("!!Not Implimented Yet!!: at least a parameter is callable.")

        elif isinstance(E_g, numbers.Real) & isinstance(C_g, numbers.Real) & isinstance(T_g, numbers.Real):
            QMat = self._generate_generating_curve_const_ECT(s, phi)
            
        else:
            raise ValueError("E_g, C_g, and T_g must be callable or constant values.")

        return QMat

    def _generate_generating_curve_const_ECT(self, s, phi):
        E_g = self.E
        C_g = self.C
        T_g = self.T

        Xi = self._Frenet_frame()
        XiMat = Xi(s)


        return QMat


    def compute(self, s, phi):
        
        E_g = self.E
        C_g = self.C
        T_g = self.T
        r0 = self.r0
        R0 = self.R0
        delta_g = 0
        gamma_g = 0
        PMat = self._generate_generating_spiral(s)
        
        r = r0*np.exp(E_g*s)
        D = np.sqrt(C_g**2+T_g**2)
        
        ED3E2pD2 = E_g*D**3*(E_g**2 + D**2)
        expEs = np.exp(E_g*s)
        sinDs = np.sin(D*s)
        cosDs = np.cos(D*s)
        
        ##
        ## Generating Curve
        ##
        xi1 = np.dot(
            R0,
            np.array([(T_g**2 + C_g**2*cosDs)/D**2, C_g*sinDs/D, C_g*T_g*(1 - cosDs)/D**2])
        ).transpose()
        xi2 = np.dot(
            R0,
            np.array([(-C_g*sinDs/D), cosDs, T_g*sinDs/D])
        ).transpose()
        xi3 = np.dot(
            R0,
            np.array([(C_g*T_g*(1 - cosDs))/D**2, (-T_g*sinDs)/D, (C_g**2+T_g**2*cosDs)/D**2])
        ).transpose()

        xi1 = np.apply_along_axis(self.__normalize, 1, xi1)
        xi2 = np.apply_along_axis(self.__normalize, 1, xi2)
        xi3 = np.apply_along_axis(self.__normalize, 1, xi3)

        rot2 = Rotation.from_rotvec(delta_g*xi2).as_matrix()
        rot3 = Rotation.from_rotvec(gamma_g*xi3).as_matrix()
        rot_g = np.array([np.dot(rot3[i], rot2[i]) for i in range(len(rot2))])

        xi1_i  = np.array([self.__normalize(np.dot(rot_g[i], xi1[i])) for i in range(len(xi1))])
        xi2_i  = np.array([self.__normalize(np.dot(rot_g[i], xi2[i])) for i in range(len(xi2))])
        xi3_i  = np.array([self.__normalize(np.dot(rot_g[i], xi3[i])) for i in range(len(xi3))])

        xi1_i = np.apply_along_axis(self.__normalize, 1, xi1_i)
        xi2_i = np.apply_along_axis(self.__normalize, 1, xi2_i)
        xi3_i = np.apply_along_axis(self.__normalize, 1, xi3_i)

        gencurves = []
        for i in range(len(xi1_i)):
            rot1i = Rotation.from_rotvec(np.tensordot(phi, xi1_i[i],axes=0)).as_matrix()
            gencurve = [r[i]*np.dot(rot1i[j], xi2_i[i]) for j in range(len(rot1i))]
            gencurves.append(gencurve)

        gencurves = np.array(gencurves)

        ##
        ## Surface
        ## 
        X, Y, Z = np.array([PMat[i] + gencurves[i] for i in range(len(gencurves))]).transpose()

        return(X.transpose(), Y.transpose(), Z.transpose())
    

##
## Equations
##   
class GrowingTubeModelEqns(GSGCModel, EqnsMixin):
    def __init__(self, 
                 E = sym.Function("E")(sym.Symbol("s")), 
                 C = sym.Function("C")(sym.Symbol("s")), 
                 T = sym.Function("T")(sym.Symbol("s")), 
                 r0 = sym.Symbol("r_0"), 
                 p0 = sym.Matrix.zeros(3), R0 = sym.Matrix.diag([1,1,1], unpack=True), 
                 s = sym.Symbol("s"), phi = sym.Symbol("phi")):
        
        self.E = E
        self.C = C
        self.T = T
        self.r0 = r0
        self.p0 = p0
        self.R0 = R0
        self.s = s
        self.phi = phi
        
        self.r = sym.Function("r")
        
        xi1 = sym.Function("xi_1")
        xi2 = sym.Function("xi_2")
        xi3 = sym.Function("xi_3")
        self.Xi = sym.Lambda(s, sym.Matrix([xi1(s), xi2(s), xi3(s)]))
        
    @property
    def E(self):
        return self.__E
    
    @E.setter
    def E(self, E):
        self.__E = E
        
    @property
    def C(self):
        return self.__C
    
    @C.setter
    def C(self, C):
        self.__C = C
            
    @property
    def T(self):
        return self.__T
    
    @T.setter
    def T(self, T):
        self.__T = T
     
    @property
    def r0(self):
        return self.__r0
    
    @r0.setter
    def r0(self, r0):
        self.__r0 = r0
        
    @property
    def p0(self):
        return self.__p0
    
    @r0.setter
    def p0(self, p0):
        self.__p0 = p0
    
        
    @property
    def R0(self):
        return self.__R0
    
    @R0.setter
    def R0(self, R0):
        self.__R0 = R0
        
    @property
    def size(self):
        return self.__r0

    @size.setter
    def size(self, r0):
        self.r0 = r0
        
    @property
    def position(self):
        return self.__p0

    @position.setter
    def position(self, p0):
        self.p0 = p0
        
    @property
    def orientation(self):
        return self.__R0

    @orientation.setter
    def orientation(self, R0):
        self.R0 = R0
    
    def _generate_generating_spiral(self, **params):
        E = self.E
        C = self.C
        T = self.T
        r0 = self.r0
        p0 = self.p0
        R0 = self.R0
        s = self.s
        
        r = r0*sym.exp(E*s)
        D = sym.sqrt(C**2+T**2)

        ED3E2pD2 = E*D**3 * (E**2 + D**2)
        expEs = sym.exp(E_g*s)
        sinDs = sym.sin(D*s)
        cosDs = stm.cos(D*s)

        ##
        ## Growth Trajectory
        ##
        P = r0*D*(((D**2) * (T**2) + (E**2) * (T**2) + C**2 * E**2 * cosDs 
                   + E*D*(C**2)*sinDs)*expEs - D**2 * (E**2 + T**2))/ED3E2pD2
        Q = r0*C*D*E_g*(-expEs*(C**2 + T**2)*cosDs 
                          + D*(D + expEs*E*sinDs))/ED3E2pD2
        R = r0*C*T*D*(((E**2) + (D**2) - (E**2) * cosDs - E*D*sinDs)*expEs - D**2)/ED3E2pD2

        p = sym.Lambda(s,p0 + R0*sym.Matrix([P, Q, R]))
        
        return p
        
    def calculate_generating_spiral(self, **params):
        """
        Args:
        """
        return self._generate_generating_spiral(**params)
        
    def _define(self):
        
        E = self.E
        C = self.C
        T = self.T
        r0 = self.r0
        p0 = self.p0
        R0 = self.R0
        s = self.s
        Xi = self.Xi
        
        #
        # Tube growth
        #
        eq_tb = sym.Eq(sym.Derivative(self.r(s), s), E*self.r(s))
        
        #
        # Frenet-Serret formulas
        #
        
        FSCoef = sym.Matrix([[0, C,0],
                             [-C, 0, T],
                             [0, -T,0]])

        eq_fsf_l = sym.Derivative(sym.UnevaluatedExpr(Xi(s)),s)
        eq_fsf_r = sym.UnevaluatedExpr(FSCoef)*sym.UnevaluatedExpr(Xi(s))
        
        return {"tube growth": eq_tb, 
                "Frenet-Serret formulas": sym.Eq(eq_fsf_l, eq_fsf_r)}
        
    @property
    def definition(self):
        
        return self._define()