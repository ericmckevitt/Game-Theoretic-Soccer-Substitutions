import math

def diminishing_returns(x):
    return 1 - math.e ** (-0.7*x)

# print(diminishing_returns(4))

# num = 0.8 * diminishing_returns(3)
# den = 0.75 * diminishing_returns(5)
# print(num)
# print(den)
# print(num/den)
# print((num/den) >= 0.5)

# num = 0.65 * 0.753
# den = 0.6 * 0.940
# print(num/den)

s1a = 0.8
s1d = 0.6
s2a = 0.65
s2d = 0.75

att = s2a * diminishing_returns(2)
defe = s1d * diminishing_returns(5)
print(att)
print(defe)

# if att > defe:
#     print("goal scored")
# else:
#     print("no goal")

print(max(att - defe, 0))
