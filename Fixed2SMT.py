#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 24 17:47:47 2021

@author: wmnc67
"""
#3 gen possible checker
# pairing : ybar56,wbar34

from z3 import * 

#import itertools 
set_param(proof=True)
c = [Bool('c%s' % (i)) for i in range(45)] 



#c[0]=1 S, c[1 ]=1 e1, c[2 ]=1 e2, c[3 ]=1 b1, c[4 ]=1 b2, c[5 ]=1 b3, c[6 ]=1 z1, c[7 ]=1 x, c[8 ]=1 g 
#          c[9 ]=S e1, c[10]=S e2, c[11]=S b1, c[12]=S b2, c[13]=S b3, c[14]=S z1, c[15]=S x, c[16]=S g  
#                      c[17]=e1e2, c[18]=e1b1, c[19]=e1b2, c[20]=e1b3, c[21]=e1z1, c[22]=e1x, c[23]=e1g
#                                  c[24]=e2b1, c[25]=e2b2, c[26]=e2b3, c[27]=e2z1, c[28]=e2x, c[29]=e2g,
#                                              c[30]=b1b2, c[31]=b1b3, c[32]=b1z1, c[33]=b1x, c[34]=b1g,
#                                                          c[35]=b2b3, c[36]=b2z1, c[37]=b2x, c[38]=b2g,                                                                                                                 
#                                                                      c[39]=b3z1, c[40]=b3x, c[41]=b3g
#                                                                                  c[42]=z1x, c[43]=z1g
#                                                                                             c[44]=x g

#  parity function
#  break up long input lists in two smaller lists

def MXor(ls): #solver,
    if len(ls) == 1:
        return ls[0]
    elif len(ls) == 2:
        return Xor(ls[0], ls[1])
    elif len(ls) == 3:
        return Xor(ls[0], Xor(ls[1], ls[2]))
    elif len(ls) == 4:
        #  this symmetric form is much faster than the chained forms
        return Xor(Xor(ls[0], ls[1]), Xor(ls[2], ls[3]))
    else:
        cut_len = len(ls) // 2
        return Xor(MXor(ls[:cut_len]), MXor(ls[cut_len:]))


s = Solver() # create a solver s 

#fix trivial phases
s.add(And(c[3]==True,c[4]==True,c[5]==True,c[6]==True,c[8]==True,c[16]==True,c[34]==True,\
          c[41]==True,c[43]==True,c[44]==True))

#implement SUSY
#s.add(And(c[0]==True,c[10]==True, c[11]==True, c[12]==True,c[13]==True,c[14]==True,c[15]==True,c[16]==True,c[17]==True,c[18]==True))
#implement not close to susyness
#s.add(Not(And(c[9]==True, c[10]==True, c[14]==True,c[15]==True,c[16]==True)))

#F1_pqrs projectors
#pqrs=0000
#N16s=0
#N16bars=0
F1_0000=And(c[18],c[24],c[32],MXor([c[30],c[31],c[32]]),c[33])
#c[34]=b1 g - imaginary! -i <-> FALSE, i <-> True
F1_0000_16=And(F1_0000,c[30])#chirality phase (b1)(b2)
#F1_0000_n5bar=And(F1_0000,c[30],Not(c[34]))#
F1_0000_16bar=And(F1_0000,Not(c[30]))#
#F1_0000_n5=And(F1_0000,Not(c[30]),Not(c[34]))#
# c[44] b1 g

#s.add(F1_0000)
#s.add(Sum([If(projBools[i],1,0) for i in range(len(projBools))]) >= 6)
#F1e3456
F1e3456=And(MXor([c[9],c[19],c[20],c[22],True,c[1],c[17]]),MXor([c[10],c[25],c[26],c[28],True,c[2],c[17]]),\
        MXor([c[14],c[36],c[39],c[42],c[21],c[27]]),MXor([c[0],c[11],c[12],c[13],c[14],\
        c[30],c[31],c[36],c[39],True,c[7],c[33],c[37],c[40],c[1],c[18],c[19],c[20],c[21],\
            c[2],c[24],c[25],c[26],c[27]]),MXor([c[15],c[37],c[40],c[7],c[22],c[28]]))


#B2 - from gamma projection you get + or - choices for (wbar56) giving full 16/16bar
#pqrs=0000
F2_0000=And(c[36],MXor([c[30],c[35],c[36]]),Not(c[37]))
F2_0000_n10=And(F2_0000,c[30],c[38])#chirality phase (b1)(b2)
F2_0000_n5bar=And(F2_0000,c[30],Not(c[38]))
F2_0000_n10bar=And(F2_0000,Not(c[30]),c[38])
F2_0000_n5=And(F2_0000,Not(c[30]),Not(c[38]))

#1000
F2_1000=And(Xor(c[36],c[21]),MXor([c[30],c[35],c[36],c[1],c[18],c[19],c[20],c[21]]),\
            Not(Xor(c[37],c[22])))
F2_1000_n10=And(F2_1000,MXor([True,c[30],c[18]]),Not(Xor(c[38],c[23])))#chirality phase (b2+e2)(b1)
F2_1000_n5bar=And(F2_1000,MXor([True,c[30],c[18]]),Xor(c[38],c[23]))
F2_1000_n10bar=And(F2_1000,Not(MXor([True,c[30],c[18]])),Not(Xor(c[38],c[23])))
F2_1000_n5=And(F2_1000,Not(MXor([True,c[30],c[18]])),Xor(c[38],c[23]))

#0100
F2_0100=And(MXor([c[36],c[27]]),MXor([c[30],c[35],c[36],c[2],c[24],c[25],c[26],c[27]]),\
            Not(MXor([c[37],c[28]])))
F2_0100_n10=And(F2_0100,MXor([True,c[30],c[24]]),Not(Xor(c[38],c[29]))) #chirality phase (b2+e2)(b1)
F2_0100_n5bar=And(F2_0100,MXor([True,c[30],c[24]]),Xor(c[38],c[29]))
F2_0100_n10bar=And(F2_0100,Not(MXor([True,c[30],c[24]])),Not(Xor(c[38],c[29])))
F2_0100_n5=And(F2_0100,Not(MXor([True,c[30],c[24]])),Xor(c[38],c[29]))

#1100
F2_1100=And(MXor([c[36],c[21],c[27]]),MXor([c[30],c[35],c[36],c[1],c[18],c[19],c[20],c[21],c[2],c[24],c[25],c[26],c[27]]),\
            Not(MXor([c[37],c[22],c[28]])))
F2_1100_n10=And(F2_1100,Not(MXor([True,c[30],c[18],c[24]])),Not(MXor([c[38],c[23],c[29]]))) #chirality phase (b2+e2)(b1)
F2_1100_n5bar=And(F2_1100,Not(MXor([True,c[30],c[18],c[24]])),MXor([c[38],c[23],c[29]]))
F2_1100_n10bar=And(F2_1100,MXor([True,c[30],c[18],c[24]]),Not(MXor([c[38],c[23],c[29]])))
F2_1100_n5=And(F2_1100,MXor([True,c[30],c[18],c[24]]),MXor([c[38],c[23],c[29]]))


# define 4 B3 projectors 

#pqrs=0000
F3_0000=And(c[39],MXor([c[31],c[35],c[39]]),c[40])
F3_0000_16=And(F3_0000,c[31])#chirality phase (b1)(b2)
#F2_0000_n5bar=And(F2_0000,c[30],Not(c[29]))
F3_0000_16bar=And(F3_0000,Not(c[31]))
#F2_0000_n5=And(F2_0000,Not(c[30]),Not(c[29]))

#1000
F3_1000=And(Xor(c[39],c[21]),MXor([c[31],c[35],c[39],c[1],c[18],c[19],c[20],c[21]]),\
            Xor(c[40],c[22]))
F3_1000_16=And(F3_1000,MXor([True,c[31],c[18]])) #chirality phase (b2+e2)(b1)
#F2_1000_n5bar=And(F2_0100,MXor([True,c[15],c[21]]),Not(Xor(c[29],c[20])))
F3_1000_16bar=And(F3_1000,Not(MXor([True,c[31],c[18]])))
#F2_1000_n5=And(F2_0100,Not(MXor([True,c[15],c[21]])),Not(Xor(c[29],c[20])))

#0100
F3_0100=And(MXor([c[39],c[27]]),MXor([c[31],c[35],c[39],c[2],c[24],c[25],c[26],c[27]]),\
            MXor([c[40],c[28]]))
F3_0100_16=And(F3_0100,MXor([True,c[31],c[24]])) #chirality phase (b2+e2)(b1)
#F2_0100_n5bar=And(F2_0100,MXor([True,c[15],c[21]]),Not(Xor(c[29],c[20])))
F3_0100_16bar=And(F3_0100,Not(MXor([True,c[31],c[24]])))
#F2_0100_n5=And(F2_0100,Not(MXor([True,c[15],c[21]])),Not(Xor(c[29],c[20])))

#1100
F3_1100=And(MXor([c[39],c[21],c[27]]),MXor([c[31],c[35],c[39],c[1],c[18],c[19],c[20],c[21],c[2],c[24],c[25],c[26],c[27]]),\
            MXor([c[40],c[22],c[28]]))
F3_1100_16=And(F3_1100,MXor([c[31],c[18],c[24]])) #chirality phase (b2+e2)(b1)
#F2_1100_n5bar=And(F2_0100,MXor([True,c[15],c[21]]),Not(Xor(c[29],c[20])))
F3_1100_16bar=And(F3_1100,Not(MXor([c[31],c[18],c[24]])))
#F2_1100_n5=And(F2_0100,Not(MXor([True,c[15],c[21]])),Not(Xor(c[29],c[20])))

n10s=[   F1_0000_16,F1_0000_16,F1_0000_16,F1_0000_16,F1e3456,F1e3456,\
         F2_0000_n10,F2_0000_n10,F2_1000_n10,F2_1000_n10,\
         F2_0100_n10,F2_0100_n10,F2_1100_n10,F2_1100_n10,\
         F3_0000_16,F3_1000_16,F3_0100_16,F3_1100_16] 

n5bars= [F1_0000_16,F1_0000_16,F1_0000_16,F1_0000_16,F1e3456,F1e3456,\
         F2_0000_n5bar,F2_0000_n5bar,F2_1000_n5bar,F2_1000_n5bar,\
         F2_0100_n5bar,F2_0100_n5bar,F2_1100_n5bar,F2_1100_n5bar,\
         F3_0000_16,F3_1000_16,F3_0100_16,F3_1100_16] 

n10bars=[F1_0000_16bar,F1_0000_16bar,F1_0000_16bar,F1_0000_16bar,F1e3456,F1e3456,\
         F2_0000_n10bar,F2_0000_n10bar,F2_1000_n10bar,F2_1000_n10bar,\
         F2_0100_n10bar,F2_0100_n10bar,F2_1100_n10bar,F2_1100_n10bar,\
         F3_0000_16bar,F3_1000_16bar,F3_0100_16bar,F3_1100_16bar]

n5s=    [F1_0000_16bar,F1_0000_16bar,F1_0000_16bar,F1_0000_16bar,F1e3456,F1e3456,\
         F2_0000_n5,F2_0000_n5,F2_1000_n5,F2_1000_n5,\
         F2_0100_n5,F2_0100_n5,F2_1100_n5,F2_1100_n5,\
         F3_0000_16bar,F3_1000_16bar,F3_0100_16bar,F3_1100_16bar]

#s.add(Sum([If(projBools[i],1,0) for i in range(len(projBools))]) >= 6)
#print(N16s)

s.add(Sum([If(n10s[i],1,0) for i in range(len(n10s))])-Sum([If(n10bars[i],1,0) for i in range(len(n10bars))]) == 3) 
s.add(Sum([If(n5bars[i],1,0) for i in range(len(n5bars))])-Sum([If(n5s[i],1,0) for i in range(len(n5s))]) == 3) 
"""
#HEAVY HIGGS
#B1_pqrs projectors
#pqrs=0000
#N16s=0
#N16bars=0
#deps on x phase - get 16+16bar or projected! 
B1_0000=And(Not(Xor(c[9],c[18])),Not(Xor(c[10],c[24])),Not(Xor(c[14],c[32])),Not(MXor([c[0],c[11],c[12],c[13],c[14],c[30],c[31],c[32]])),Not(Xor(c[15],c[33])))
#c[34]=b1 g - imaginary! -i <-> FALSE, i <-> True
#B1_0000_16=And(B1_0000,c[30],c[34])#chirality phase (b1)(b2)
#F1_0000_n5bar=And(F1_0000,c[30],Not(c[34]))#
#B1_0000_16bar=And(B1_0000,Not(c[30]),c[34])#
#F1_0000_n5=And(F1_0000,Not(c[30]),Not(c[34]))#
# c[44] b1 g

#s.add(Sum([If(projBools[i],1,0) for i in range(len(projBools))]) >= 6)

#B2 - from gamma projection you get + or - choices for (wbar56) giving full 16/16bar
#pqrs=0000
B2_0000=And(Not(Xor(c[14],c[36])),Not(MXor([c[0],c[11],c[12],c[13],c[14],c[30],c[35],c[36]])),\
            Xor(c[15],c[37]))
B2_0000_n10=And(B2_0000,Not(Xor(c[16],c[38])))#chirality phase (b1)(b2)
B2_0000_n5=And(B2_0000,Xor(c[16],c[38]))
#B2_0000_n10bar=And(B2_0000,Not(c[30]),c[38])
#B2_0000_n5=And(B2_0000,Not(c[30]),Not(c[38]))

#1000
B2_1000=And(Not(MXor([c[14],c[36],c[21]])),\
            Not(MXor([c[0],c[11],c[12],c[13],c[14],c[30],c[35],c[36],\
                      c[1],c[18],c[19],c[20],c[21]])),MXor([c[15],c[37],c[22]]))
B2_1000_n10=And(B2_1000,Not(MXor([c[16],c[38],c[23]])))#chirality phase (b1)(b2)
B2_1000_n5=And(B2_1000,MXor([c[16],c[38],c[23]]))
#B2_1000_n10bar=And(B2_1000,Not(MXor([True,c[30],c[18]])),Xor(c[38],c[23]))
#B2_1000_n5=And(B2_1000,Not(MXor([True,c[15],c[21]])),Not(Xor(c[38],c[23])))

#0100
B2_0100=And(Not(MXor([c[14],c[36],c[27]])),\
            Not(MXor([c[0],c[11],c[12],c[13],c[14],c[30],c[35],c[36],\
                      c[2],c[24],c[25],c[26],c[27]])),MXor([c[15],c[37],c[28]]))
B2_0100_n10=And(B2_0100,Not(MXor([c[16],c[38],c[29]])))#chirality phase (b1)(b2)
B2_0100_n5=And(B2_0100,MXor([c[16],c[38],c[29]]))
#B2_0100_n10bar=And(B2_0100,Not(MXor([True,c[30],c[24]])),Xor(c[38],c[29]))
#B2_0100_n5=And(B2_0100,Not(MXor([True,c[15],c[21]])),Not(Xor(c[38],c[29])))

#1100
B2_1100=And(Not(MXor([c[14],c[36],c[21],c[27]])),\
            Not(MXor([c[0],c[11],c[12],c[13],c[14],c[30],c[35],c[36],\
                      c[1],c[18],c[19],c[20],c[21],c[2],c[24],c[25],c[26],c[27]])),\
            MXor([c[15],c[37],c[22],c[28]]))
B2_1100_n10=And(B2_1100,Not(MXor([c[16],c[38],c[23],c[29]])))#chirality phase (b1)(b2)
B2_1100_n5=And(B2_1100,MXor([c[16],c[38],c[23],c[29]]))
#B2_1100_n10bar=And(B2_1100,Not(MXor([True,c[30],c[18],c[24]])),MXor([c[38],c[23],c[29]]))
#B2_1100_n5=And(B2_1100,Not(MXor([True,c[15],c[21]])),Not(MXor([c[38],c[23],c[29]])))


# define 4 B3 projectors 
#pqrs=0000
B3_0000=And(Not(Xor(c[14],c[39])),Not(MXor([c[0],c[11],c[12],c[13],c[14],c[31],c[35],c[39]])),\
            Not(Xor(c[15],c[40])))
#deps on x phase - get 16+16bar or projected! 
#B3_0000_16=And(B3_0000,Xor(c[16],c[30]))#chirality phase (b1)(b2)
#F2_0000_n5bar=And(F2_0000,c[30],Not(c[29]))
#B3_0000_16bar=And(B3_0000,Not(Xor(c[16],c[30])))
#F2_0000_n5=And(F2_0000,Not(c[30]),Not(c[29]))

#1000
B3_1000=And(Not(MXor([c[14],c[39],c[21]])),Not(MXor([c[0],c[11],c[12],c[13],c[14],c[31],c[35],c[39],c[1],c[18],c[19],c[20],c[21]])),\
            Not(MXor([c[15],c[40],c[22]])))
#B3_1000_16=And(B3_1000,MXor([True,c[31],c[18]])) #chirality phase (b2+e2)(b1)
#F2_1000_n5bar=And(F2_0100,MXor([True,c[15],c[21]]),Not(Xor(c[29],c[20])))
#B3_1000_16bar=And(B3_1000,Not(MXor([True,c[31],c[18]])))
#F2_1000_n5=And(F2_0100,Not(MXor([True,c[15],c[21]])),Not(Xor(c[29],c[20])))

#0100
B3_0100=And(Not(MXor([c[14],c[39],c[27]])),Not(MXor([c[0],c[11],c[12],c[13],c[14],c[31],c[35],c[39],c[2],c[24],c[25],c[26],c[27]])),\
            Not(MXor([c[15],c[40],c[28]])))
#B3_0100_16=And(B3_0100,MXor([True,c[31],c[24]])) #chirality phase (b2+e2)(b1)
#F2_0100_n5bar=And(F2_0100,MXor([True,c[15],c[21]]),Not(Xor(c[29],c[20])))
#B3_0100_16bar=And(B3_0100,Not(MXor([True,c[31],c[24]])))
#F2_0100_n5=And(F2_0100,Not(MXor([True,c[15],c[21]])),Not(Xor(c[29],c[20])))

#1100
B3_1100=And(Not(MXor([c[14],c[39],c[21],c[27]])),\
            Not(MXor([c[0],c[11],c[12],c[13],c[14],c[31],c[35],c[39],c[1],c[18],c[19],c[20],c[21],c[2],c[24],c[25],c[26],c[27]])),\
            Not(MXor([c[15],c[40],c[22],c[28]])))
#B3_1100_16=And(B3_1100,MXor([True,c[31],c[18],c[24]])) #chirality phase (b2+e2)(b1)
#F2_1100_n5bar=And(F2_0100,MXor([True,c[15],c[21]]),Not(Xor(c[29],c[20])))
#B3_1100_16bar=And(B3_1100,Not(MXor([True,c[31],c[18],c[24]])))
#F2_1100_n5=And(F2_0100,Not(MXor([True,c[15],c[21]])),Not(Xor(c[29],c[20])))

n10Bs=[  B1_0000,B1_0000,B1_0000,B1_0000,\
         B2_0000_n10,B2_1000_n10,B2_0100_n10,B2_1100_n10,B2_0000_n10,B2_1000_n10,B2_0100_n10,B2_1100_n10,\
         B3_0000,B3_1000,B3_0100,B3_1100] 

#n5Bs= [B1_0000,B1_0000,B1_0000,B1_0000,\
#         B2_0000_n5,B2_1000_n5,B2_0100_n5,B2_1100_n5,\
#         B3_0000,B3_1000,B3_0100,B3_1100] 

#s.add(Sum([If(n10Bs[i],1,0) for i in range(len(n10Bs))]) >= 1) 

#VECTORIALS- LIGHT HIGGS

V1_0000=And(Not(MXor([c[9],c[18],c[22]])),Not(MXor([c[10],c[24],c[28]])),\
            Not(Xor(c[14],c[32])),\
            Not(MXor([c[0],c[11],c[12],c[13],c[14],c[30],c[31],c[32],True,c[7],c[33],c[37],c[40],c[42]])),Not(MXor([c[15],c[33],c[7]])))
#c[34]=b1 g - imaginary! -i <-> FALSE, i <-> True
#B1_0000_16=And(B1_0000,c[30],c[34])#chirality phase (b1)(b2)
#F1_0000_n5bar=And(F1_0000,c[30],Not(c[34]))#
#B1_0000_16bar=And(B1_0000,Not(c[30]),c[34])#
#F1_0000_n5=And(F1_0000,Not(c[30]),Not(c[34]))#
# c[44] b1 g

#s.add(Sum([If(projBools[i],1,0) for i in range(len(projBools))]) >= 6)

#B2 - from gamma projection you get + or - choices for (wbar56) giving full 16/16bar
#pqrs=0000
V2_0000=And(Not(MXor([c[14],c[36],c[42]])),Not(MXor([c[0],c[11],c[12],c[13],c[14],c[30],c[35],c[36],True,c[7],c[33],c[37],c[40],c[42]])),\
            Not(MXor([c[15],c[37],c[7]])))
#V2_0000_n10=And(V2_0000,Not(MXor([c[16],c[38],c[44]])))#chirality phase (b1)(b2)
#V2_0000_n5=And(V2_0000,MXor([c[16],c[38],c[44]]))
#B2_0000_n10bar=And(B2_0000,Not(c[30]),c[38])
#B2_0000_n5=And(B2_0000,Not(c[30]),Not(c[38]))

#1000
V2_1000=And(Not(MXor([c[14],c[36],c[42],c[21]])),\
            Not(MXor([c[0],c[11],c[12],c[13],c[14],c[30],c[35],c[36],True,c[7],c[33],c[37],c[40],c[42],\
                      c[1],c[18],c[19],c[20],c[21]])),Not(MXor([c[15],c[37],c[22],c[7]])))
#V2_1000_n10=And(V2_1000,Not(MXor([c[16],c[38],c[23],c[44]])))#chirality phase (b1)(b2)
#V2_1000_n5=And(V2_1000,MXor([c[16],c[38],c[23],c[44]]))
#B2_1000_n10bar=And(B2_1000,Not(MXor([True,c[30],c[18]])),Xor(c[38],c[23]))
#B2_1000_n5=And(B2_1000,Not(MXor([True,c[15],c[21]])),Not(Xor(c[38],c[23])))

#0100
V2_0100=And(Not(MXor([c[14],c[36],c[42],c[27]])),\
            Not(MXor([c[0],c[11],c[12],c[13],c[14],c[30],c[35],c[36],True,c[7],c[33],c[37],c[40],c[42],\
                      c[2],c[24],c[25],c[26],c[27]])),Not(MXor([c[15],c[37],c[28],c[7]])))
#V2_0100_n10=And(V2_0100,Not(MXor([c[16],c[38],c[29],c[44]])))#chirality phase (b1)(b2)
#V2_0100_n5=And(V2_0100,MXor([c[16],c[38],c[29],c[44]]))
#B2_0100_n10bar=And(B2_0100,Not(MXor([True,c[30],c[24]])),Xor(c[38],c[29]))
#B2_0100_n5=And(B2_0100,Not(MXor([True,c[15],c[21]])),Not(Xor(c[38],c[29])))

#1100
V2_1100=And(Not(MXor([c[14],c[36],c[42],c[21],c[27]])),\
            Not(MXor([c[0],c[11],c[12],c[13],c[14],c[30],c[35],c[36],True,c[7],c[33],c[37],c[40],c[42],\
                      c[1],c[18],c[19],c[20],c[21],c[2],c[24],c[25],c[26],c[27]])),\
            Not(MXor([c[15],c[37],c[22],c[28],c[7]])))
#V2_1100_n10=And(V2_1100,Not(MXor([c[16],c[38],c[23],c[29]])))#chirality phase (b1)(b2)
#V2_1100_n5=And(V2_1100,MXor([c[16],c[38],c[23],c[29]]))
#B2_1100_n10bar=And(B2_1100,Not(MXor([True,c[30],c[18],c[24]])),MXor([c[38],c[23],c[29]]))
#B2_1100_n5=And(B2_1100,Not(MXor([True,c[15],c[21]])),Not(MXor([c[38],c[23],c[29]])))


# define 4 B3 projectors 
#pqrs=0000
V3_0000=And(Not(MXor([c[14],c[39],c[42]])),Not(MXor([c[0],c[11],c[12],c[13],c[14],c[31],c[35],c[39],True,c[7],c[33],c[37],c[40],c[42]])),\
            Not(MXor([c[15],c[40],True,c[7]])))
#deps on x phase - get 16+16bar or projected! 
#B3_0000_16=And(B3_0000,Xor(c[16],c[30]))#chirality phase (b1)(b2)
#F2_0000_n5bar=And(F2_0000,c[30],Not(c[29]))
#B3_0000_16bar=And(B3_0000,Not(Xor(c[16],c[30])))
#F2_0000_n5=And(F2_0000,Not(c[30]),Not(c[29]))

#1000
V3_1000=And(Not(MXor([c[14],c[39],c[21],c[42]])),\
            Not(MXor([c[0],c[11],c[12],c[13],c[14],c[31],c[35],c[39],True,c[7],c[33],c[37],c[40],c[42],\
                      c[1],c[18],c[19],c[20],c[21]])),\
            Not(MXor([c[15],c[40],c[22],True,c[7]])))
#B3_1000_16=And(B3_1000,MXor([True,c[31],c[18]])) #chirality phase (b2+e2)(b1)
#F2_1000_n5bar=And(F2_0100,MXor([True,c[15],c[21]]),Not(Xor(c[29],c[20])))
#B3_1000_16bar=And(B3_1000,Not(MXor([True,c[31],c[18]])))
#F2_1000_n5=And(F2_0100,Not(MXor([True,c[15],c[21]])),Not(Xor(c[29],c[20])))

#0100
V3_0100=And(Not(MXor([c[14],c[39],c[27],c[42]])),\
            Not(MXor([c[0],c[11],c[12],c[13],c[14],c[31],c[35],c[39],True,c[7],c[33],c[37],c[40],c[42],\
                      c[2],c[24],c[25],c[26],c[27]])),\
            Not(MXor([c[15],c[40],c[28],True,c[7]])))
#B3_0100_16=And(B3_0100,MXor([True,c[31],c[24]])) #chirality phase (b2+e2)(b1)
#F2_0100_n5bar=And(F2_0100,MXor([True,c[15],c[21]]),Not(Xor(c[29],c[20])))
#B3_0100_16bar=And(B3_0100,Not(MXor([True,c[31],c[24]])))
#F2_0100_n5=And(F2_0100,Not(MXor([True,c[15],c[21]])),Not(Xor(c[29],c[20])))

#1100
V3_1100=And(Not(MXor([c[14],c[39],c[21],c[27],c[42]])),\
            Not(MXor([c[0],c[11],c[12],c[13],c[14],c[31],c[35],c[39],True,c[7],c[33],c[37],c[40],c[42],\
                      c[1],c[18],c[19],c[20],c[21],c[2],c[24],c[25],c[26],c[27]])),\
            Not(MXor([c[15],c[40],c[22],c[28],True,c[7]])))

nHs=[  V1_0000,V1_0000,V1_0000,V1_0000,\
       V2_0000,V2_1000,V2_0100,V2_1100,\
       V2_0000,V2_1000,V2_0100,V2_1100,\
       V3_0000,V3_1000,V3_0100,V3_1100,\
       V3_0000,V3_1000,V3_0100,V3_1100] 

#n5Bs= [B1_0000,B1_0000,B1_0000,B1_0000,\
#         B2_0000_n5,B2_1000_n5,B2_0100_n5,B2_1100_n5,\
#         B3_0000,B3_1000,B3_0100,B3_1100] 

#s.add(Sum([If(nHs[i],1,0) for i in range(len(nHs))]) >= 1) 

#TQMC
V2s=[V2_0000,V2_1000,V2_0100,V2_1100]
V3s=[V3_0000,V3_1000,V3_0100,V3_1100]
#untwisted higgs on all 3 planes I think- double check from fortran
F3s=[F3_1100_16,F3_1100_16,F3_1100_16,F3_1100_16]
F2s=[F2_0000_n10,F2_1000_n10,F2_0100_n10,F2_1100_n10]
#degeneracy F2 is 2 so only need one of them to form untwisted TQMC(?)
#s.add(Or(F1_0000,Or(F2_0000_n10,F2_1000_n10,F2_0100_n10,F2_1100_n10),\
      #Sum([If(F3s[i],1,0) for i in range(len(F3s))]) >= 2,\
      #And(V1_0000,Sum([If(F2s[i],1,0) for i in range(len(F2s))]) >= 1,Sum([If(F3s[i],1,0) for i in range(len(F3s))]) >= 1),\
      #And(V2_0000,F1_0000,Sum([If(F3s[i],1,0) for i in range(len(F3s))]) >= 1),\
      #And(V3_0000,F1_0000,Sum([If(F2s[i],1,0) for i in range(len(F2s))]) >= 1)))
"""  
#TACHYONS
#Vectorials
#e1 { }, projs: S,e2,z1,z2,x,b1,g - do S separatel
#y2bar/w2bar oscillator case
y2e1=And(c[17],Not(c[21]),Not(MXor([c[1],c[18],c[19],c[20],c[21]])),Not(c[22]),Not(c[18]),Not(c[23]))
#y3456bar
y3e1=And(Not(c[17]),Not(c[21]),Not(MXor([c[1],c[18],c[19],c[20],c[21]])),Not(c[22]),c[18],Not(c[23]))
#wbar3456...
w3e1=And(Not(c[17]),Not(c[21]),Not(MXor([c[1],c[18],c[19],c[20],c[21]])),Not(c[22]),Not(c[18]),c[23])
#psibareta -projected by gamma
#psie1=And(Not(c[9]),Not(c[17]),Not(c[21]),Not(MXor([c[1],c[18],c[19],c[20],c[21]])),Not(c[22]),c[23])
#phi34
phi3e1=And(Not(c[17]),c[21],Not(MXor([c[1],c[18],c[19],c[20],c[21]])),Not(c[22]),Not(c[18]))
#phi58
phi5e1=And(Not(c[17]),Not(c[21]),MXor([c[1],c[18],c[19],c[20],c[21]]),Not(c[22]),Not(c[18]))


s.add(Or(c[9],And(Not(y2e1),Not(y3e1),Not(w3e1),Not(phi5e1),Not(phi3e1))))

#e2 { }, projs: S,e1,z1,z2,x,b1,g - do S separately
#y2bar/w2bar oscillator case
y1e2=And(c[17],Not(c[27]),Not(MXor([c[2],c[24],c[25],c[26],c[27]])),Not(c[28]),Not(c[24]),Not(c[29]))
#y3456bar
y3e2=And(Not(c[17]),Not(c[27]),Not(MXor([c[2],c[24],c[25],c[26],c[27]])),Not(c[28]),c[24],Not(c[29]))
#wbar3456...
w3e2=And(Not(c[17]),Not(c[27]),Not(MXor([c[2],c[24],c[25],c[26],c[27]])),Not(c[28]),Not(c[24]),c[29])
#psibareta -projected by gamma
#psie1=And(Not(c[9]),Not(c[17]),Not(c[21]),Not(MXor([c[1],c[18],c[19],c[20],c[21]])),Not(c[22]),c[23])
#phi34
phi3e2=And(Not(c[17]),c[27],Not(MXor([c[2],c[24],c[25],c[26],c[27]])),Not(c[28]),Not(c[24]))
#phi58
phi5e2=And(Not(c[17]),Not(c[27]),MXor([c[2],c[24],c[25],c[26],c[27]]),Not(c[28]),Not(c[24]))

s.add(Or(c[10],And(Not(y1e2),Not(y3e2),Not(w3e2),Not(phi5e2),Not(phi3e2))))

#e1+e2 { }, projs: S,z1,z2,x,b1,g - do S separatel
#y3456bar
y3e12=And(Not(Xor(c[21],c[27])),Not(MXor([c[1],c[18],c[19],c[20],c[21],c[2],c[24],c[25],c[26],c[27]])),Not(Xor(c[22],c[28])),Xor(c[18],c[24]),Not(Xor(c[23],c[28])))
#wbar3456...
#w3e12=And(Not(Xor(c[21],c[27])),Not(MXor([c[1],c[18],c[19],c[20],c[21],c[2],c[24],c[25],c[26],c[27]])),Not(Xor(c[22],c[28])),Xor(c[18],c[24]),Not(Xor(c[23],c[28])))
#psibareta -projected by gamma
#psie1=And(Not(c[9]),Not(c[17]),Not(c[21]),Not(MXor([c[1],c[18],c[19],c[20],c[21]])),Not(c[22]),c[23])
#phi34
phi3e12=And(Xor(c[21],c[27]),Not(MXor([c[1],c[18],c[19],c[20],c[21],c[2],c[24],c[25],c[26],c[27]])),Not(Xor(c[22],c[28])),Xor(c[18],c[24]))
#phi58
phi5e12=And(Not(Xor(c[21],c[27])),MXor([c[1],c[18],c[19],c[20],c[21],c[2],c[24],c[25],c[26],c[27]]),Not(Xor(c[22],c[28])),Xor(c[18],c[24]))

s.add(Or(Not(Xor(c[9],c[10])),And(Not(y3e12),Not(phi5e12),Not(phi3e12))))

#Spinorials
#z1, projs: S,e1,e2,x,b1,b2,b3 
z1T=And(Not(c[14]),Not(c[21]),Not(c[27]),Not(c[42]),Not(c[32]),Not(c[36]),Not(c[39]))

#z2, projs: S,e1,e2,z1,x,b1,b2,b3- i'll just do b1 
z2T=And(Not(MXor([c[0],c[11],c[12],c[13],c[14]])),Not(MXor([c[1],c[18],c[19],c[20],c[21]])),Not(MXor([c[2],c[24],c[25],c[26],c[27]])),\
    Not(MXor([True,c[32],c[36],c[39]])),Not(MXor([c[30],c[31],c[32]])),Not(MXor([c[30],c[35],c[36]])))

#2g+x, just b1 not b2 and b3..?
ggxT=And(Not(c[15]),Not(c[22]),Not(c[27]),Not(c[33]),Not(c[37]),Not(c[40]),c[7])

#2g+x+z1
ggxz1T=And(Not(MXor([True,c[15],c[14]])),Not(MXor([c[22],c[21]])),\
    Not(MXor([True,c[28],c[27]])),Not(MXor([True,c[7],c[42]])),MXor([c[33],c[32]]),\
    Not(MXor([True,c[37],c[36]])),Not(MXor([True,c[40],c[39]])))

#2g+x+z2
ggxz2T=And(Not(MXor([True,c[15],c[0],c[11],c[12],c[13],c[14]])),Not(MXor([c[22],c[1],c[18],c[19],c[20],c[21]])),\
    Not(MXor([c[28],c[2],c[24],c[25],c[26],c[27]])),Not(MXor([c[33],c[37],c[40],c[42]])),Not(MXor([True,c[33],c[30],c[31],c[32]])),\
    Not(MXor([True,c[37],c[30],c[35],c[36]])),Not(MXor([True,c[40],c[31],c[35],c[39]])))

#2g+x+z1+z2
ggxz1z2T=And(Not(MXor([True,c[15],c[0],c[11],c[12],c[13]])),Not(MXor([c[22],c[1],c[18],c[19],c[20]])),\
    Not(MXor([c[28],c[2],c[24],c[25],c[26]])),Not(MXor([c[33],c[37],c[40]])),Not(MXor([True,c[33],c[30],c[31]])),\
    Not(MXor([True,c[37],c[30],c[35]])),Not(MXor([True,c[40],c[31],c[35]])))

s.add(And(Not(z1T),Not(z2T),Not(ggxT),Not(ggxz1T),Not(ggxz2T),Not(ggxz1z2T)))

#e1+z1, b1...
e1z1=And(Xor(c[9],c[14]),Not(Xor(c[17],c[27])),Not(Xor(c[22],c[42])),\
    Not(MXor([c[1],c[18],c[19],c[20],c[21],c[32],c[36],c[39]])),Not(MXor([True,c[18],c[32]])))

#e1+z2
e1z2=And(MXor([c[9],c[0],c[11],c[12],c[13],c[14]]),Not(MXor([c[17],c[2],c[24],c[25],c[26],c[27]])),MXor([c[22],c[7],c[33],c[37],c[40],c[42]]),\
    Not(MXor([c[21],c[32],c[36],c[39]])),Not(MXor([True,c[18],c[30],c[31],c[32]])))

#e1+2g+x
ggxz1z2_e1=MXor([c[22],c[1],c[18],c[19],c[20],c[33],c[37],c[40]])
e1x=And(Xor(c[9],c[15]),Not(Xor(c[17],c[28])),Not(MXor([c[22],True,c[7]])),\
    Not(MXor([True,c[18],c[33]])),Not(ggxz1z2_e1))

#e1+2g+x+z1
ggxz2_e1=MXor([True,c[22],c[1],c[18],c[19],c[20],c[21],c[33],c[37],c[40],c[32],c[36],c[39]])
e1xz1=And(Not(MXor([c[9],c[15],c[14]])),Not(MXor([c[17],c[28],c[27]])),Not(MXor([c[22],True,c[7],c[42]])),\
    Not(MXor([True,c[18],c[33],c[32]])),Not(ggxz2_e1))

#e1+2g+x+z2
ggxz1_e1=MXor([True,c[22],c[21],c[33],c[37],c[40],c[32],c[36],c[39]])
e1ggxz2=And(MXor([c[9],c[0],c[11],c[12],c[13],c[14]]),Not(MXor([c[17],c[28],c[2],c[24],c[25],c[26],c[27]])),Not(MXor([c[22],c[33],c[37],c[40],c[42]])),\
    Not(MXor([c[18],c[33],c[30],c[31],c[32]])),Not(ggxz1_e1))

#e1+2g+x+z1+z2
#ggx_e1=MXor([True,c[22],c[21],c[33],c[37],c[40],c[32],c[36],c[39]])
e1ggxz1z2=And(MXor([True,c[9],c[0],c[11],c[12],c[13]]),Not(MXor([c[17],c[28],c[2],c[24],c[25],c[26]])),Not(MXor([c[22],c[33],c[37],c[40]])),\
    Not(MXor([True,c[18],c[33],c[30],c[31]])))#,Not(ggx_e1))

s.add(And(Not(e1z1),Not(e1z2),Not(e1x),Not(e1xz1),Not(e1ggxz2),Not(e1ggxz1z2)))


#e2+z1, b1...
e2z1=And(Xor(c[10],c[14]),Not(Xor(c[17],c[21])),Not(Xor(c[28],c[42])),\
    Not(MXor([c[2],c[24],c[25],c[26],c[27],c[32],c[36],c[39]])),Not(MXor([True,c[24],c[32]])))

#e2+z2 #Not() absorbed by True in x proj
e2z2=And(MXor([c[10],c[0],c[11],c[12],c[13],c[14]]),Not(MXor([c[17],c[1],c[18],c[19],c[20],c[21]])),\
    MXor([c[28],c[7],c[33],c[37],c[40],c[42]]),\
    Not(MXor([c[27],c[32],c[36],c[39]])),Not(MXor([True,c[24],c[30],c[31],c[32]])))

#e2+2g+x
ggxz1z2_e2=MXor([c[28],c[2],c[24],c[25],c[26],c[33],c[37],c[40]])
e2x=And(Xor(c[10],c[15]),Not(Xor(c[17],c[22])),Not(MXor([c[28],True,c[7]])),\
    Not(MXor([True,c[24],c[33]])),Not(ggxz1z2_e2))

#e2+2g+x+z1
ggxz2_e2=MXor([True,c[28],c[2],c[24],c[25],c[26],c[27],c[33],c[37],c[40],c[32],c[36],c[39]])
e2xz1=And(Not(MXor([c[10],c[15],c[14]])),Not(MXor([c[17],c[22],c[21]])),Not(MXor([c[28],True,c[7],c[42]])),\
    Not(MXor([c[24],c[33],c[32]])),Not(ggxz2_e2))

#e2+2g+x+z2
ggxz1_e2=MXor([True,c[28],c[27],c[33],c[37],c[40],c[32],c[36],c[39]])
e2ggxz2=And(MXor([c[10],c[0],c[11],c[12],c[13],c[14]]),Not(MXor([c[17],c[22],c[1],c[18],c[19],c[20],c[21]])),\
    Not(MXor([c[28],c[33],c[37],c[40],c[42]])),\
    Not(MXor([c[24],c[33],c[30],c[31],c[32]])),Not(ggxz1_e2))

#e2+2g+x+z1+z2
#ggx_e2=MXor([True,c[22],c[21],c[33],c[37],c[40],c[32],c[36],c[39]])
e2ggxz1z2=And(MXor([True,c[10],c[0],c[11],c[12],c[13]]),Not(MXor([c[17],c[22],c[1],c[18],c[19],c[20]])),\
    Not(MXor([c[28],c[33],c[37],c[40]])),\
    Not(MXor([True,c[24],c[33],c[30],c[31]])))#,Not(ggx_e2))

s.add(And(Not(e2z1),Not(e2z2),Not(e2x),Not(e2xz1),Not(e2ggxz2),Not(e2ggxz1z2)))

#e1+e2+z1
e1e2z1=And(Not(MXor([c[9],c[10],c[14]])),Not(MXor([c[22],c[28],c[42]])),\
    Not(MXor([c[1],c[18],c[19],c[20],c[21],c[2],c[24],c[25],c[26],c[27],c[32],c[36],c[39]])),\
        Not(MXor([c[18],c[24],c[32]])))


#e1+e2+z2
e1e2z2=And(Not(MXor([c[10],c[11],c[0],c[11],c[12],c[13],c[14]])),\
    Not(MXor([c[22],c[28],True,c[7],c[33],c[37],c[40],c[42]])),Not(MXor([c[21],c[27],c[32],c[36],c[39]])),\
        Not(MXor([c[18],c[24],c[30],c[31],c[32]])))

#e1+e2+2g+x
ggxz1z2_e12=MXor([c[22],c[28],c[1],c[18],c[19],c[20],c[2],c[24],c[25],c[26],c[33],c[37],c[40]])
e1e2x=And(Not(MXor([c[9],c[10],c[15]])),Not(MXor([c[22],c[28],True,c[7]])),Not(ggxz1z2_e12),\
        Not(MXor([c[18],c[24],c[33]])))

#e1+e2+2g+x+z1
ggxz2_e12=MXor([True,c[22],c[32],c[1],c[18],c[19],c[20],c[21],c[2],c[24],c[25],c[26],c[27],c[33],c[37],c[40],c[32],c[36],c[39]])
e12ggxz1=And(Not(MXor([True,c[9],c[10],c[15],c[14]])),\
             Not(MXor([c[22],c[28],True,c[7],c[42]])),Not(ggxz2_e12),\
        Not(MXor([c[18],c[24],c[32],c[33]])))

#e1+e2+2g+x+z2
ggxz1_e12=MXor([True,c[22],c[28],c[21],c[27],c[33],c[37],c[40],c[32],c[36],c[39]])
e12ggxz2=And(Not(MXor([True,c[9],c[10],c[15],c[0],c[11],c[12],c[13],c[14]])),\
    Not(MXor([c[22],c[28],c[33],c[37],c[40],c[42]])),Not(ggxz1_e12),\
        Not(MXor([c[18],c[24],c[33],c[30],c[31],c[32]])))

#e1+e2+2g+x+z1z2
e12ggxz1z2=And(Not(MXor([c[9],c[10],c[15],c[0],c[11],c[12],c[13]])),\
    Not(MXor([c[22],c[28],c[33],c[37],c[40]])),\
        Not(MXor([c[18],c[24],c[33],c[30],c[31]])))

s.add(And(Not(e1e2z1),Not(e1e2z2),Not(e1e2x),Not(e12ggxz1),Not(e12ggxz2),Not(e12ggxz1z2)))

print(s.check()) 

import timeit
import json 
import sys
from pandas import DataFrame
start = timeit.default_timer()
from time import time
t1 = time()
counter=0

if s.check() == unsat:
    f = open('No3GenSMTProof.txt','a') 
    old_stdout = sys.stdout  #  store the default system handler to be able to restore it 

    sys.stdout = f 
    print(s.proof())
    
    f.close()
    sys.stdout=old_stdout
    
while s.check() == sat: 
#for i in range(10):
    m = s.model () 
    
    if not m: 

        break 
    t2 = time()
    #counter+=1
    #if counter%1000==0:
        #print([t2-t1,counter])
    #if t2-t1>=600:
        #print("10 mins gone")
        #break
    #f = open('FixedSMTTimings221121.txt','a') 
    #old_stdout = sys.stdout  #  store the default system handler to be able to restore it 

    #sys.stdout = f 
    #t2 = time()
    #elapsed = t2 - t1
    #print(elapsed)
    
    #f.close()
    #sys.stdout=old_stdout
    
    #f = open('FixedSMTTimings191121.txt','a') 
    #finds 15389 in 1 hour
    #old_stdout = sys.stdout  #  store the default system handler to be able to restore it 

    #sys.stdout = f 
    #t2 = time()
    #elapsed = t2 - t1
    #print(elapsed) # Print elapsed time
    Boolm=[m[c[i]] for i in range(45)]
    #print(Boolm)
    """
    BCm=[]
    for item in Boolm:
        #print(type(item))
        if type(item)==BoolRef:
            if item.sexpr()=='true':
                BCm.append(1)
            else:
                BCm.append(0)
        else:
            BCm.append(1)
    #BCm=[ 1 if item.sexpr()=='true' else 0 for item in Boolm]

    print(BCm)"""
    #print(type(modl))
    
    #f.close() 

    #sys.stdout=old_stdout 
    
    #print(sorted ([(d, m[d]) for d in m], key = lambda x: str(x[0]))) 
    #print(sorted ([(m[d]) for d in m], key = lambda x: str(x[0]))) 

    s.add(Not(And([v() == m[v] for v in m]))) 

stop = timeit.default_timer()
print("Time:", stop - start)