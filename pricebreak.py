from math import sqrt
import matplotlib.pyplot as plt
import numpy as np

def plot_parabola(cur, unit_cost, min_limit, max_limit):
  x = np.linspace(min_limit, max_limit, 100)
  y = cur['Demand']*unit_cost + ((cur['SetupCost']*cur['Demand']) / x) + ((cur['HoldingCost'] / 2)*x)
  plt.plot(x, y)

# ordering cycle
def get_t0(y, d):
  return y/d

# get ideal order quantity
def get_y_m(d,h,k):
  return pow((2*d*k)/h, 0.5)

# get total inventory cost
def get_TCU(cur, cost_key):
  return cur[cost_key]*cur['Demand'] + ((cur['SetupCost']*cur['Demand'])/ cur['OrderQuantity']) + (cur['HoldingCost']*cur['OrderQuantity'])/2

# get roots for Q
def get_roots(coeffs):
  a,b,c = coeffs
  # calculate the discriminant
  d = (b**2) - (4*a*c)
  # find two solutions
  sol1 = (-b-sqrt(d))/(2*a)
  sol2 = (-b+sqrt(d))/(2*a)
  return [sol1, sol2]

# get quadratic equation coefficients
def get_quad_eqn_coeff(cur, unit_cost, tcu):
  a = 1
  b = (2 * (unit_cost*cur['Demand'] - tcu)) / cur['HoldingCost']
  c = (2 * cur['SetupCost'] * cur['Demand']) / cur['HoldingCost']
  return [a,b,c]

def get_zones(cur):
  return [ [0, cur['OrderQuantity']], [ cur['OrderQuantity'], cur['OrderLimit'] ], [cur['OrderLimit'], float('inf')] ]


def get_current_order_zone(cur):
  res_zone = None
  all_zones = cur['Zones']
  for i, zone in enumerate(all_zones):
    if zone[0] < cur['Quantity'] < zone[1]:
      res_zone = zone
  return res_zone


"""
d = 
cost2 =
cost1 = 
# size of the order
y = 
# limit
q = 
# unit purchasing price
c = 
"""
cur = {
  'Demand': 187.5,
  'HoldingCost': 0.02,
  'SetupCost': 20,
  'LeadTime': 2,
  'UnitCost1': 3,
  'UnitCost2': 2.5,
  'Quantity': 1000,
  'AdditionalCost': 0
}

y_m = get_y_m(cur['Demand'], cur['HoldingCost'], cur['SetupCost'])
print(f"ym = {y_m}")

cur['OrderQuantity'] = y_m
tcu_1 = get_TCU(cur, 'UnitCost1')
cur['TCU1'] = tcu_1
print(f"TCU({y_m}) = {tcu_1}")

tcu_2 = get_TCU(cur, 'UnitCost2')
cur['TCU2'] = tcu_2

parabola_1_coeffs = get_quad_eqn_coeff(cur, cur['UnitCost2'], cur['TCU1'])
parabola_2_coeffs = get_quad_eqn_coeff(cur, cur['UnitCost1'], cur['TCU2'])

print(f"Quadratic eqn. coefficients are {parabola_1_coeffs}, {parabola_2_coeffs}")

roots = get_roots(parabola_1_coeffs)
print(f"Roots are {roots}")

cur['OrderLimit'] = [x for x in roots if x > y_m ][0]
print(f"The order limit we are considering will be {cur['OrderLimit']}")
zones = get_zones(cur)

cur['Zones'] = zones
print(zones)

cur_order_zone = get_current_order_zone(cur)
print(f"Order belongs to the zone -> {cur_order_zone}")

print(f"Order {cur['Quantity']} units when inventory level drops to {cur['LeadTime'] * cur['Demand']} ")

plot_parabola(cur, cur['UnitCost1'], 1 ,cur['Quantity'])
plot_parabola(cur, cur['UnitCost2'], cur['Quantity']+1, 2*cur['Quantity'])
plt.show()
