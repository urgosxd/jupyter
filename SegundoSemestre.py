from sympy import *
import re
init_printing(use_latex='mathjax')
s = "(3*x+5)/(2*x)"
asd= [x.strip("+") for x in re.findall(r".+?(?=[+-]|$)", s)]

def RestarSegundo(pos,neg,term1):
    finalTerm= list(map(lambda p:-1*p,pos)) +  list(map(lambda p:-1*p,neg))
    return Add(Add(*finalTerm),term1,evaluate=False),-1*Add(Add(*finalTerm),term1) if LC(Add(Add(*finalTerm),term1))<0 else Add(Add(*finalTerm),term1)
    
def SumaResta(expr):
   ispos=lambda x:x.as_coeff_Mul()[0].is_positive
   return sift(Add.make_args(expr),ispos,binary=True)
def ShowEquals(term1,term2=None):
   if term2 is None:
       return r'$%s$' %str(term1)
   else:
       return r'$%s = %s$' %(str(term1),str(term2))

def ShowDivision(num,deno):
   return r'\frac{%s}{%s}' %(str(latex(num)),str(latex(deno)))

def SimplificarHandle(num,deno):
   factores1= factor_list(num)
   factores2= factor_list(deno)
   factores1= list(map(lambda ele:{"facts":ele[0],"exp":ele[1]},factores1[1])) 
   factores2= list(map(lambda ele:{"facts":ele[0],"exp":ele[1]},factores2[1])) 
   expandFactores1=[]
   expandFactores2=[]

   for idx,i in enumerate(factores2):
       countFails=0
       for ii in factores1:
           if i["facts"] == ii["facts"]:
               contador = ii["exp"]-i["exp"]
               for iii in range(ii["exp"]):
                   expandFactores1.append({
                       "cross":True if iii>contador-1 else False,
                       "facts":ii["facts"],
                       })
               for iii2 in range(i["exp"]):
                   expandFactores2.append({
                       "cross": True if iii>contador*(-1)-1 else False,
                       "facts":i["facts"]
                       })
           else:
               countFails+=1
               if idx == len(factores2)-1:
                   expandFactores1.append({
                       "cross":False,
                       "facts":ii["facts"]
                       })
                   
       if countFails == len(factores1):
           expandFactores2.append({
               "cross":False,
               "facts": i["facts"]
               })
               


   factores1= list(map(lambda ele: r'\cancel{(%s)}' %str(latex(ele["facts"])) if ele["cross"]==True else "(%s)" %str(latex(ele["facts"])),expandFactores1))
   factores2= list(map(lambda ele: r'\cancel{(%s)}' %str(latex(ele["facts"])) if ele["cross"]==True else "(%s)" %str(latex(ele["facts"])),expandFactores2))
   factores1=r''.join(factores1)
   factores2=r''.join(factores2)
   return r'\frac{%s}{%s}' %(factores1,factores2)

def EquationHandle(tupleEq,estadios=[],tupleEq2=None):
   relation=0 
   relation=1 if tupleEq2 is None else 2
   if relation < 2:
       if len(tupleEq)<2:
           aaa= tupleEq[0]
           return factor(aaa)
       else:
           aaa= tupleEq[0]
           aaa2= tupleEq[1]
           estadios.append(ShowDivision(aaa,aaa2))
           if cancel(expand(aaa)/expand(aaa2)) == expand(aaa)/expand(aaa2):
               return estadios
           else:
               estadios.append(ShowEquals(SimplificarHandle(aaa,aaa2)))
               estadios.append(factor(aaa/aaa2))
           return estadios
   else:
       fases=[[False,False]]
       if len(tupleEq)<2 and len(tupleEq2)==2:
           aaa= tupleEq[0]
           bbb= tupleEq2[0]
           bbb2= tupleEq2[1]
           estadios.append(ShowEquals(latex(aaa),ShowDivision(bbb,bbb2)))
           divi2=''
           if cancel(expand(bbb)/expand(bbb2)) == expand(bbb)/expand(bbb2):
               fases[0][1]= False
           else:
               divi2=SimplificarHandle(bbb/bbb2)
               fases[0][1]=True
           if fases[0][0]==False and fases[0][1]==True:
               estadios.append(ShowEquals(latex(aaa),divi2))
               estadios.append(ShowEquals(latex(aaa),latex(bbb/bbb2)))
           term1=fraction(aaa//1)
           term2=fraction(bbb/bbb2)
           estadios.append(ShowEquals(latex(UnevaluatedExpr(term1[0])*UnevaluatedExpr(term2[1])),latex(UnevaluatedExpr(term2[0])*UnevaluatedExpr(term1[1]))))
           newTerm1=term1[0]*term2[1]
           newTerm1=expand(newTerm1)
           newTerm2=term2[0]*term1[1]
           newTerm2=expand(newTerm2)
           estadios.append(ShowEquals(latex(newTerm1),latex(newTerm2)))
           pos,neg = SumaResta(newTerm2)
           one,two = RestarSegundo(pos,neg,newTerm1)
           estadios.append(ShowEquals(latex(one),latex(0)))
           estadios.append(ShowEquals(latex(two),latex(0)))


       if len(tupleEq)==2 and len(tupleEq2)<2:
           aaa= tupleEq[0]
           aaa2=tupleEq[1]
           bbb= tupleEq2[0]
           estadios.append(ShowEquals(ShowDivision(aaa,aaa2),latex(bbb)))
           divi=''
           if cancel(expand(aaa)/expand(aaa2)) == expand(aaa)/expand(aaa2):
               fases[0][0]= False
           else:
               divi=SimplificarHandle(aaa,aaa2)
               fases[0][0]=True
           if fases[0][0] == True and fases[0][1]==False:
               estadios.append(ShowEquals(divi,latex(bbb)))
               estadios.append(ShowEquals(latex(aaa/aaa2),latex(bbb)))

           term1=fraction(aaa/aaa2)
           term2=fraction(bbb//1)
           estadios.append(ShowEquals(latex(UnevaluatedExpr(term1[0])*UnevaluatedExpr(term2[1])),latex(UnevaluatedExpr(term2[0])*UnevaluatedExpr(term1[1]))))
           newTerm1=term1[0]*term2[1]
           newTerm1=expand(newTerm1)
           newTerm2=term2[0]*term1[1]
           newTerm2=expand(newTerm2)
           estadios.append(ShowEquals(latex(newTerm1),latex(newTerm2)))
           pos,neg = SumaResta(newTerm2)
           one,two = RestarSegundo(pos,neg,newTerm1)
           estadios.append(ShowEquals(latex(one),latex(0)))
           estadios.append(ShowEquals(latex(two),latex(0)))
       if len(tupleEq)==2 and len(tupleEq2)==2:
           aaa=tupleEq[0]
           aaa2=tupleEq[1]
           bbb= tupleEq2[0]
           bbb2= tupleEq2[1]
           estadios.append(ShowEquals(ShowDivision(aaa,aaa2),ShowDivision(bbb,bbb2)))
           divi= ""
           divi2= ""
           if cancel(expand(aaa)/expand(aaa2)) == expand(aaa)/expand(aaa2):
               fases[0][0] = False
           else:
               divi = SimplificarHandle(aaa,aaa2)
               fases[0][0] = True
           if cancel(expand(bbb)/expand(bbb2)) == expand(bbb)/expand(bbb2):
               fases[0][1] = False
           else:
               divi2 = SimplificarHandle(bbb,bbb2)
               fases[0][1] = True
            
           if fases[0][0] == True and fases[0][1] == True:
               estadios.append(ShowEquals(divi,divi2))
               estadios.append(ShowEquals(latex(aaa/aaa2),latex(bbb/bbb2)))
           if fases[0][0] == True and fases[0][1] == False:
               estadios.append(ShowEquals(divi,latex(bbb/bbb2)))
               estadios.append(ShowEquals(latex(aaa/aaa2),latex(bbb/bbb2)))
           if fases[0][0] == False and fases[0][1]== True:
               estadios.append(ShowEquals(latex(aaa/aaa2),divi2))
               estadios.append(ShowEquals(latex(aaa/aaa2),latex(bbb/bbb2)))

           term1=fraction(aaa/aaa2)
           term2=fraction(bbb/bbb2)
           estadios.append(ShowEquals(latex(UnevaluatedExpr(term1[0])*UnevaluatedExpr(term2[1])),latex(UnevaluatedExpr(term2[0])*UnevaluatedExpr(term1[1]))))
           newTerm1=term1[0]*term2[1]
           newTerm1=expand(newTerm1)
           newTerm2=term2[0]*term1[1]
           newTerm2=expand(newTerm2)
           estadios.append(ShowEquals(latex(newTerm1),latex(newTerm2)))
           pos,neg = SumaResta(newTerm2)
           one,two = RestarSegundo(pos,neg,newTerm1)
           estadios.append(ShowEquals(latex(one),latex(0)))
           estadios.append(ShowEquals(latex(two),latex(0)))


                
           

           
# def SumEqHandle(term1,term2):
#   newTerm1=simplify(term1)
#    term1 = radsimp(term1)
#    n,d = fraction(newTerm1)
#    estadios=[[(n,d),(n2,d2)]]
#    estadios.append(ShowEquals(latex(newTerm1),latex(newTerm2)))
#    return estadios

       
def Resolver(term1,term2=None):
    estadios=[[]]
    preFases=[[0,0]]
    if term2 is None:
        return estadios 
    else:
        try:
            radTerm1 = radsimp(term1)
            preFases[0][0]=True
        except:
            n,d=fraction(term1)
            if d==1:
                term1=(n,)
                estadios[0].append(term1)
            else:
                term1=(n,d)
                estadios[0].append(term1)
        else:
            newTerm1=simplify(term1)
            n,d = fraction(newTerm1)
            estadios[0].append((n,d))

        try:
            radTerm2 = radsimp(term2)
            preFases[0][1]=True
        except:
            n2,d2=fraction(term2)
            if d2==1:
                term2=(n2,)
                estadios[0].append(term2)
            else:
                term2=(n2,d2)
                estadios[0].append(term2)
        else:
            newTerm2=simplify(term2)
            n2,d2=fraction(newTerm2)
            estadios[0].append((n2,d2))
        if preFases[0][0]==False and preFases[0][1]==False:
            estadios.append(ShowEquals(latex(term1[0] if len(term1)<2 else term1[0]/term1[1]),latex(term2[0] if len(term2)<2 else term2[0]/term2[1])))
        if preFases[0][0]==True and preFases[0][1]==False:
            estadios.append(ShowEquals(latex(radTerm1),latex(term2[0] if len(term2)<2 else term2[0]/term2[1])))
        if preFases[0][0]==False and preFases[0][1]==True:
            estadios.append(ShowEquals(latex(term1[0] if len(term1)<2 else term1[0]/term1[1]),latex(radTerm2)))
        if preFases[0][0]==True and preFases[0][1]==True:
            estadios.append(ShowEquals(latex(radTerm1),latex(radTerm2)))
        EquationHandle(estadios[0][0],estadios,estadios[0][1])
    return estadios




