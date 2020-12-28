from sympy import *
from sympy.calculus.util import continuous_domain, function_range
from sympy.plotting import plot


def Funciones(variable, expresion):
    dominio = continuous_domain(expresion, variable, S.Reals)
    rango = function_range(expresion, variable, dominio)
    p1 = plot(expresion, show=False)
    return dominio, rango, p1
