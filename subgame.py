from utilities import Formation
import math 

s1a = 0.88
s1d = 0.72
s2a = 0.76
s2d = 0.79

def diminishing_returns(x):
    return 1 - math.e ** ( -0.7 * x)

def utility(a1, d2, a2, d1, g1=0, g2=0):
    a1 = diminishing_returns(a1)
    a2 = diminishing_returns(a2)
    d1 = diminishing_returns(d1)
    d2 = diminishing_returns(d2)

    pot1 = (s1a * a1 / s2d * d2)
    pot2 = (s2a * a2 / s1d * d1)

    if pot1 > 0.5:
        g1 += 1

    if pot2 > 0.5:
        g2 += 1

    return g1 + round(pot1) - (g2 + round(pot2)), g1, g2

f1 = Formation(4, 4, 2)
f2 = Formation(4, 4, 2)
# f2 = Formation(5, 3, 2)
# f2 = Formation(4, 3, 3)


u1, g1, g2 = utility(f1.a, f2.d, f2.a, f1.d, 0, 0)
u2, g1, g2 = utility(f2.a, f1.d, f1.a, f2.d, 0, 0)

print(f"({u1}, {u2})")
print(f"g1: {g1}")
print(f"g2: {g2}")