import pandas as pd
import numpy as np

df = pd.read_csv("data.csv")
E_k1 = 0
for i, row in df.iterrows():
  E_k1 += row["prob"]*row["k1"]
print(f"E(k1) = {E_k1}")

E_k2 = 0
for i, row in df.iterrows():
  E_k2 += row["prob"]*row["k2"]
print(f"E(k2) = {E_k2}")

V_k1 = 0
print("V(k1) = ", end="")
for i, row in df.iterrows():
  print(f'{row["prob"]}*(({row["k1"]} - {E_k1})**2)', end="+")
  V_k1 += row["prob"]*((row["k1"] - E_k1)**2)
print(f"\b = {V_k1}")

V_k2 = 0
print("V(k2) = ", end="")
for i, row in df.iterrows():
  print(f'{row["prob"]}*(({row["k2"]} - {E_k2})**2)', end="+")
  V_k2 += row["prob"]*((row["k2"] - E_k2)**2)
print(f"\b = {V_k2}")

cov_k1_k2 = 0
for i, row in df.iterrows():
  cov_k1_k2 += row["prob"]*((row["k2"] - E_k2)*(row["k1"] - E_k1))

corr_coeff = cov_k1_k2 / (pow(V_k1, 0.5) * pow(V_k2, 0.5))

print(f"corr(k1,k2) = {corr_coeff}")

# data
# scenario k1 k2 prob
# recession -10 30 0.2
# stag        0 20 0.5
# boom       10 50 0.3

# data - percentage divided by 10
# scenario,k1,k2,prob
# recession,-0.1,0.3,0.2
# stag,0,0.2,0.5
# boom,0.1,0.5,0.3
