from sympy import *
import re
init_printing(use_latex='mathjax')
s = "(3*x+5)/(2*x)"
asd= [x.strip("+") for x in re.findall(r".+?(?=[+-]|$)", s)]

def SimplificarHandle(num,deno):
   factores1= factor_list(num)
   factores2= factor_list(deno)
   factores1= list(map(lambda ele:{"cross": False,"facts":ele[0]},factores1[1])) 
   factores2= list(map(lambda ele:{"cross": False,"facts":ele[0]},factores2[1])) 
    
   for i in factores1:
       for ii in factores2:
           if i["facts"] == ii["facts"]:
               i["cross"]= True
               ii["cross"]=True
   factores1= list(map(lambda ele: r'\cancel{(%s)}' %str(ele["facts"]) if ele["cross"]==True else "(%s)" %str(ele["facts"]),factores1))
   factores2= list(map(lambda ele: r'\cancel{(%s)}' %str(ele["facts"]) if ele["cross"]==True else "(%s)" %str(ele["facts"]),factores2))
   factores1=r''.join(factores1)
   factores2=r''.join(factores2)
   return r'$\frac{%s}{%s}$' %(factores1,factores2)

def EquationHandle(tupleEq,tupleEq2=None):
   relation=0 
   estadios=[]
   relation=1 if tupleEq2 is None else 2
   if relation < 2:
       if len(tupleEq)<2:
           aaa= parse_expr(tupleEq[0])
           return factor(aaa)
       else:
           aaa= parse_expr(tupleEq[0])
           aaa2= parse_expr(tupleEq[1])
           estadios.append(aaa/aaa2)
           if cancel(expand(aaa)/expand(aaa2)) == expand(aaa)/expand(aaa2):
               return estadios
           else:
               aaa=factor(aaa)
               estadios.append(SimplificarHandle(aaa,aaa2))
               estadios.append(factor(aaa/aaa2))
           return estadios
   else:
       res=re.findall(r'\((.*?)\)',tupleEq[0])
       res2=re.findall(r'\((.*?)\)',tupleEq[1])





