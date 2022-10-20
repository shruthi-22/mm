import scipy.stats as st
import numpy as np
import math
"""
Example 5.3
Suppose that the prices of two kinds of stock are S1(0) = 30 and S2(0) = 40
dollars. We prepare a portfolio worth V (0) = 1, 000 dollars by purchasing
x1 = 20 shares of stock number 1 and x2 = 10 shares of stock number 2.

"""
x1= 20
x2  = 10
s1_0 = 30
s2_0 = 40
v0 = 1000
#Find weights
w1 = (x1*s1_0)/v0
w2 = (x2*s2_0)/v0

print(w1)
print(w2)

#Weights can change as stock prices change. If S1(1) = 35 and S2(1) = 39, then
s1_1 = 35
s2_1 = 39
v1 = (x1*s1_1) + (x2*s2_1)
w1_1 = (x1*s1_1)/v1
w2_1 = (x2*s2_1)/v1
print(v1, w1_1, w2_1)

"""
Exercise 5.4
Compute the value V (1) of a portfolio worth initially V (0) = 100
dollars that consists of two securities with weights w1 = 25% and
w2 = 75%, given that the security prices are S1(0) = 45 and S2(0) = 33
dollars initially, changing to S1(1) = 48 and S2(1) = 32 dollars.
"""

v0 = 100
w1 = 0.25
w2 = 0.75
s1_0 = 45
s2_0 = 33
s1_1 = 48
s2_1 = 32

x1 = (w1*v0)/s1_0
x2 = (w2*v0)/s2_0
v1 = (x1*s1_1) + (x2*s2_1)
print(x1, x2, v1)


"""

The return KV on a portfolio consisting of two securities is the weighted average
KV = w1K1 + w2K2, 
where w1 and w2 are the weights and K1 and K2 the returns on the two
components.
"""


"""
The expected return on a portfolio consisting of two securities can easily be
expressed in terms of the weights and the expected returns on the components,
E(KV ) = w1E(K1) + w2E(K2).

Example 5.5
Consider three scenarios with the probabilities given below (a trinomial model).
Let the returns on two different stocks in these scenarios be as follows:
Scenario          Probability Return K1 Return K2
ω1 (recession)         0.2      −10%      −30%
ω2 (stagnation)        0.5        0%       20%
ω3 (boom)              0.3       10%       50%
Suppose that w1 = 60% of available funds is invested in stock 1 and 40% in
stock 2.

"""

p_n = [0.2, 0.5, 0.3]
k1 = [-.1, 0, .1]
k2 = [-.3, 0.2, .5]
w1 = 0.6
w2 = 0.4
x1 = st.rv_discrete(values=(k1, p_n))
x2 = st.rv_discrete(values=(k2, p_n))

E = (w1*x1.mean()) + (w2*x2.mean())
print(E)

"""
The variance of the return on a portfolio is given by
Var(KV ) = (w1^2)*Var(K1) + (w2^2)*Var(K2) + 2w1w2Cov(K1, K2)
Calculate covariance with numpy's np.cov. The value not on the diagonals is the covariance.
"""
t = np.cov(k1, k2)
print(t)
cov = t[0][1]
var_kv = (math.pow(w1, 2)*x1.var()) + (math.pow(w2, 2)*x2.var()) + (2*w1*w2*cov)
corr = (cov)/((math.pow(x1.var(), 0.5))*(math.pow(x2.var(), 0.5)))

print(var_kv)
print(corr)
