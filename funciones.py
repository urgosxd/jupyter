from sympy import *
from sympy.calculus.util import continuous_domain, function_range
import matplotlib.pyplot as plt
import numpy as np


def Funciones(variable, expresion):

    fig = plt.figure(1)
    ax = fig.add_subplot(111)
    ax.spines['left'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['bottom'].set_position('zero')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    xx = np.arange(-15, 15, 0.01)

    dominio = continuous_domain(expresion, variable, S.Reals)

    rango = function_range(expresion, variable, dominio)
    lamb_x = lambdify(variable, expresion, "numpy")
    yy = lamb_x(xx)
    yy[yy > 100.] = np.inf
    yy[yy < -100.] = -np.inf

    ax.plot(xx, yy, zorder=100, linewidth=2.5, color='red')
    plt.ylim([-10, 10])
    plt.margins(x=0)

    plt.yticks(range(-10, 11, 2))
    plt.xticks(range(-10, 11, 2))

    return dominio, rango, plt

def suma(tu,variable):
    dominio_0=continuous_domain(tu[0],variable,S.Reals)
    dominio_1=continuous_domain(tu[1],variable,S.Reals)
    dominio=Intersection(dominio_0,dominio_1)
    return tu[0]+tu[1],dominio
    
switcher={"suma":suma,
    "resta":resta,
    "multiplicacion":multiplicacion,
    "division":division
}
def funcionesOperaciones(tup,op,variable):
   fun= switcher[op](tup,variable)
   return fun