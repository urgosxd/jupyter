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


def suma(tu, variable):
    dominio_0 = continuous_domain(tu[0], variable, S.Reals)
    dominio_1 = continuous_domain(tu[1], variable, S.Reals)
    dominio = Intersection(dominio_0, dominio_1)
    return tu[0]+tu[1], dominio


def resta(tu, variable):
    dominio_0 = continuous_domain(tu[0], variable, S.Reals)
    dominio_1 = continuous_domain(tu[1], variable, S.Reals)
    dominio = Intersection(dominio_0, dominio_1)
    return tu[0]-tu[1], dominio


def multiplicacion(tu, variable):
    dominio_0 = continuous_domain(tu[0], variable, S.Reals)
    dominio_1 = continuous_domain(tu[1], variable, S.Reals)
    dominio = Intersection(dominio_0, dominio_1)
    return tu[0]*tu[1], dominio


def division(tu, variable):
    dominio_0 = continuous_domain(tu[0], variable, S.Reals)
    dominio_1 = continuous_domain(tu[1], variable, S.Reals)
    dominio = Complement(Intersection(dominio_0, dominio_1),
                         solveset(tu[1], variable, domain=S.Reals))
    return tu[0]/tu[1], dominio


switcher = {"suma": suma,
            "resta": resta,
            "multiplicacion": multiplicacion,
            "division": division
            }


def funcionesOperaciones(tup, op, variable):
    fun = switcher[op](tup, variable)
    return fun


def funcionesCompo(tup, bool, variable, valor=None):
    if bool == True:
        if valor == None:

            return tup[1].subs(variable, tup[0])
        else:
            final = tup[1].subs(variable, tup[0])
            return final.subs(variable, valor)


def funcionesConjuntos(array1, array2, bool):
    newArray = []

    if bool == True:
        for i in array1:
            for ii in array2:
                if i[1] == ii[0]:
                    newArray.append([i[0], ii[1]])
        domainArray = [i[0] for i in newArray]
        return newArray, domainArray
    else:
        for i in array2:
            for ii in array1:
                if i[1] == ii[0]:
                    newArray.append([i[0], ii[1]])
        domainArray = [i[0] for i in newArray]
        return newArray[::-1], domainArray[::-1]


def suma2(arr1, arr2):

    dominio_0 = [i[0] for i in arr1]
    dominio_1 = [i[0] for i in arr2]
    dominio = [i for i in dominio_0 if i in dominio_1]
    finalArray = []

    def sumita(num):
        a = 0
        b = 0
        for i in arr1:
            if i[0] == num:
                a = i[1]

        for i in arr2:
            if i[0] == num:
                b = i[1]
        return a+b

    for i in dominio:
        finalArray.append([i, sumita(i)])

    return finalArray, dominio


def resta2(arr1, arr2):
    dominio_0 = [i[0] for i in arr1]
    dominio_1 = [i[0] for i in arr2]
    dominio = [i for i in dominio_0 if i in dominio_1]
    finalArray = []

    def sumita(num):
        a = [i[1] for i in arr1 if i == num]
        b = [i[1] for i in arr2 if i == num]
        return a-b
    for i in dominio:
        finalArray.append([i, sumita(i)])

    return finalArray, dominio


def multiplicacion2(arr1, arr2):
    dominio_0 = [i[0] for i in arr1]
    dominio_1 = [i[0] for i in arr2]
    dominio = [i for i in dominio_0 if i in dominio_1]
    finalArray = []

    def sumita(num):
        a = [i[1] for i in arr1 if i == num]
        b = [i[1] for i in arr2 if i == num]
        return a*b
    for i in dominio:
        finalArray.append([i, sumita(i)])

    return finalArray, dominio


switcher2 = {
    "suma": suma2,
    "resta": resta2,
    "multiplicacion": multiplicacion2,
}


def funcionesOperacionesConjuntos(tup, op):
    fun = switcher2[op](tup[0], tup[1])
    return fun
