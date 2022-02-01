from z3 import * 

#import itertools 

g = [Bool('g%s' % (i)) for i in range(24)] 

# g[0 ]=y1, g[1 ]=y2, g[2 ]=y3, g[3 ]=y4, g[4 ]=y5, g[5 ]=y6, 
# g[6 ]=w1, g[7 ]=w2, g[8 ]=w3, g[9 ]=w4, g[10]=w5, g[11]=w6
# g[12]=y1, g[13]=y2, g[14]=y3, g[15]=y4, g[16]=y5, g[17]=y6, 
# g[18]=w1, g[19]=w2, g[20]=w3, g[21]=w4, g[22]=w5, g[23]=w6

s=Solver()

#supercurrent constraint- no psi mu chi
#s.add(Not(Xor(g[0],g[6])))
#s.add(Not(Xor(g[1],g[7])))
#s.add(Not(Xor(g[2],g[8])))
#s.add(Not(Xor(g[3],g[9])))
#s.add(Not(Xor(g[4],g[10])))
#s.add(Not(Xor(g[5],g[11])))

#supercurrent constraint- BOSONIC - no psi^mu
s.add(Not(Xor(g[0],g[6])))
s.add(Not(Xor(g[1],g[7])))
s.add(Not(Xor(g[2],g[8])))
s.add(Not(Xor(g[3],g[9])))
s.add(Not(Xor(g[4],g[10])))
s.add(Not(Xor(g[5],g[11])))

#groups from NAHE
b1L=[g[2],g[3],g[4],g[5]]
b1R=[g[14],g[15],g[16],g[17]]
b2L=[g[0],g[1],g[10],g[11]]
b2R=[g[12],g[13],g[22],g[23]]
b3L=[g[6],g[7],g[8],g[9]]
b3R=[g[18],g[19],g[20],g[21]]

#impose pairings
s.add(Or(Sum([If(b1L[i],1,0) for i in range(len(b1L))]) == 2,Sum([If(b1L[i],1,0) for i in range(len(b1L))]) == 0))
s.add(Or(Sum([If(b1R[i],1,0) for i in range(len(b1R))]) == 2,Sum([If(b1R[i],1,0) for i in range(len(b1R))]) == 0))
s.add(Or(Sum([If(b2L[i],1,0) for i in range(len(b2L))]) == 2,Sum([If(b2L[i],1,0) for i in range(len(b2L))]) == 0))
s.add(Or(Sum([If(b2R[i],1,0) for i in range(len(b2R))]) == 2,Sum([If(b2R[i],1,0) for i in range(len(b2R))]) == 0))
s.add(Or(Sum([If(b3L[i],1,0) for i in range(len(b3L))]) == 2,Sum([If(b3L[i],1,0) for i in range(len(b3L))]) == 0))
s.add(Or(Sum([If(b3R[i],1,0) for i in range(len(b3R))]) == 2,Sum([If(b3R[i],1,0) for i in range(len(b3R))]) == 0))

#not symmetric
s.add(Not(And(g[2]==g[14],g[3]==g[15],g[4]==g[16],g[5]==g[17],g[0]==g[12],g[1]==g[13],g[10]==g[22],g[11]==g[23],\
              g[6]==g[18],g[7]==g[19],g[8]==g[20],g[9]==g[21])))

#s.add(Not(And(g[2]==g[14],g[3]==g[15],g[4]==g[16],g[5]==g[17])))
#s.add(Not(And(g[0]==g[12],g[1]==g[13],g[10]==g[22],g[11]==g[23])))
#s.add(Not(And(g[6]==g[18],g[7]==g[19],g[8]==g[20],g[9]==g[21])))


print(s.check()) 

import timeit
import json 
#start = timeit.default_timer()
#from time import time
#t1 = time()
def rewrite(lst):
    ywg=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    if lst[0]==1:
        ywg[0]='y1'
    if lst[1]==1:
        ywg[1]='y2'
    if lst[2]==1:
        ywg[2]='y3'
    if lst[3]==1:
        ywg[3]='y4'
    if lst[4]==1:
        ywg[4]='y5'
    if lst[5]==1:
        ywg[5]='y6'
    if lst[6]==1:
        ywg[6]='w1'
    if lst[7]==1:
        ywg[7]='w2'
    if lst[8]==1:
        ywg[8]='w3'
    if lst[9]==1:
        ywg[9]='w4'
    if lst[10]==1:
        ywg[10]='w5'
    if lst[11]==1:
        ywg[11]='w6'
    if lst[12]==1:
        ywg[12]='ybar1'
    if lst[13]==1:
        ywg[13]='ybar2'
    if lst[14]==1:
        ywg[14]='ybar3'
    if lst[15]==1:
        ywg[15]='ybar4'
    if lst[16]==1:
        ywg[16]='ybar5'
    if lst[17]==1:
        ywg[17]='ybar6'
    if lst[18]==1:
        ywg[18]='wbar1'
    if lst[19]==1:
        ywg[19]='wbar2'
    if lst[20]==1:
        ywg[20]='wbar3'
    if lst[21]==1:
        ywg[21]='wbar4'
    if lst[22]==1:
        ywg[22]='wbar5'
    if lst[23]==1:
        ywg[23]='wbar6'
    return ywg

start=timeit.default_timer()

while s.check() == sat: 

    m = s.model () 
    
    if not m: 

        break 

    #Boolg=[m[g[i]] for i in range(24)]
# =============================================================================
#     f = open('BosonicPairingsInt.txt','a') 
# 
#     old_stdout = sys.stdout  #  store the default system handler to be able to restore it 
# 
#     sys.stdout = f 
#     #t2 = time()
#     #elapsed = t2 - t1
#     #print(elapsed) # Print elapsed time
#     Boolg=[m[g[i]] for i in range(24)]
#     BCg=[ 1 if item.sexpr()=='true' else 0 for item in Boolg]
# 
#     print(BCg)
#     #print(rewrite(BCg))
# 
# 
#     #print(type(modl))
#     
#     f.close() 
# 
#     sys.stdout=old_stdout 
# =============================================================================
    
    #print(sorted ([(d, m[d]) for d in m], key = lambda x: str(x[0]))) 
    #print(sorted ([(m[d]) for d in m], key = lambda x: str(x[0]))) 

    s.add(Not(And([v() == m[v] for v in m]))) 

    

stop = timeit.default_timer()
print("Time:", stop - start)



