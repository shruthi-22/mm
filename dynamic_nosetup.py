from collections import defaultdict
import pandas as pd

df = pd.read_csv("data.csv")
res = defaultdict(dict)

carry_over_qty, carry_over_month = 0, 0
for _, row in df.iterrows():
  res[row["Month"]] = defaultdict(list)
  res[row["Month"]]["Regular"].append(row["Regular"])
  expected_overtime_qty = row["Demand"]-res[row["Month"]]["Regular"][-1]
  if expected_overtime_qty <= row["Overtime"]:
    res[row["Month"]]["Overtime"].append(expected_overtime_qty)
    carry_over_qty = row["Overtime"] - expected_overtime_qty
    carry_over_month = row["Month"]
  else:
    res[row["Month"]]["Overtime"].append(row["Overtime"] )
    res[carry_over_month]["Overtime"].append(row["Demand"]-row["Regular"]-row["Overtime"])
    carry_over_qty -= row["Demand"]-row["Regular"]-row["Overtime"]
print(res, carry_over_qty)

tcu = 0
holding_cost = 0.1
cost_map = {
  "Regular": 6,
  "Overtime": 9
}
for period in res:
  for key in res[period]:
    for idx,val in enumerate(res[period][key]):
      tcu += val *(cost_map[key]+ holding_cost * idx)
print(f"Total inventory cost is {tcu}")
# data in qn
# Month Regular Overtime Demand
# 1  90 50 100
# 2 100 60 190
# 3 120 80 210
# 4 110 70 160
