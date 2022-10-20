
from math import ceil, floor, isnan
import pandas as pd

def get_y_star(d,h,k):
  return pow((2*d*k)/h, 0.5)

def get_t0_star(y_star, d):
  return y_star/d

def get_n(L,t0):
  return floor(L/t0)

def get_eff_lead_time(l,n,t0_star):
  return l - n*t0_star

def get_reorder_point(l_e, d):
  return l_e*d

def get_optimal_inventory_policy(cur):
  t = get_reorder_point( 
    get_eff_lead_time(
      cur['LeadTime'], 
      get_n(
        cur['LeadTime'], 
        get_t0_star(
          get_y_star(
            cur['Demand'], cur['HoldingCost'], cur['SetupCost']
          ), 
          cur['Demand']
        )
      ),
      get_t0_star(
        get_y_star(
          cur['Demand'], cur['HoldingCost'], cur['SetupCost']
        ), 
        cur['Demand']
      )
    ), 
    cur['Demand'] 
  )
  return get_y_star(cur['Demand'], cur['HoldingCost'], cur['SetupCost']), t

def get_total_inventory_cost(cur):
  def cur_cost(d,h,k):
    return pow(2*h*d*k, 0.5)
  def additional_cost(d,c):
    if not c or isnan(c):
      return 0
    return d*c
  return cur_cost( cur['Demand'], cur['HoldingCost'], cur['SetupCost'] ) + additional_cost(cur['Demand'], cur['AdditionalCost'])

data = pd.read_csv('data.csv')

for i,cur in data.iterrows():
  units_to_order, threshold = get_optimal_inventory_policy(cur)
  print(f"Order {ceil(units_to_order)} units when the inventory reaches {ceil(threshold)} units")
  print(f"Total Inventory cost is : {get_total_inventory_cost(cur)}")

#Demand,SetupCost,HoldingCost,AdditionalCost,LeadTime
#100,100,0.02,null,12
