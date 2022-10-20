from collections import defaultdict


def cost_function(z):
  if z <= 3:
    return 10 * z
  return 30 + 20*(z - 3)

# def cost_function(z):
#   if z <= 6:
#     return z
#   return 6 + 2*(z-6)

def get_min_inventory_cost_util_v1(inventory_states, amount_states, function_output_map):
  idx = 0
  for xi_plus_1, zi in zip(inventory_states, amount_states):
    print(xi_plus_1, end = "  ")
    pdt_hi_xi_plus_1 =  xi_plus_1 * problem["holding_costs"][period]
    prev_fn_output =  function_output_map[period-1][zi] if period-1 in function_output_map and zi in function_output_map[period-1] else 0
    res = min(cost_function(zi) + setup_costs[period] + pdt_hi_xi_plus_1 + prev_fn_output, float("inf"))
    print("  "*idx,end=" ")
    print(res)
    function_output_map[period][xi_plus_1] = [zi, res]
    idx += 1
    print("")

def get_min_inventory_cost_util_v2(period, inventory_states, amount_states, function_output_map):
  for xi_plus_1 in inventory_states:
    print(xi_plus_1, end = "  ")
    pdt_hi_xi_plus_1 =  xi_plus_1 * problem["holding_costs"][period]
    for zi in amount_states:
      value = xi_plus_1 + problem["demand"][period] - zi
      if value < 0:
        res = float("inf")
      else:
        prev_fn_output =  function_output_map[period-1][value][1] if period-1 in function_output_map and value in function_output_map[period-1] else 0
        res = cost_function(zi) + (setup_costs[period] if zi > 0 else 0) + pdt_hi_xi_plus_1 + prev_fn_output
      print(res, end = "  ")
      if xi_plus_1 not in function_output_map[period] or period not in function_output_map:
        function_output_map[period][xi_plus_1] = []
      function_output_map[period][xi_plus_1].append([zi, res])
    function_output_map[period][xi_plus_1] = min(function_output_map[period][xi_plus_1], key= lambda x: x[1])
    print("")

def get_minimum_order_quantity(function_output_map, period):
  res_zi_star, res_function_output_value = float("inf"), float("inf")
  for _,function_output in function_output_map[period].items():
    zi_star, function_output_value = function_output
    if function_output_value < res_function_output_value:
      res_zi_star = zi_star
      res_function_output_value = function_output_value
  return res_zi_star

def min_inventory_cost_for_period(period, problem, function_output_map, initial_inventory_amount):
  res = 0
  min_inventory_amount, max_inventory_amount = 0, sum(demand[period+1:])
  min_amount_ordered, max_amount_ordered = min_inventory_amount + demand[period] - initial_inventory_amount, max_inventory_amount + demand[period] - initial_inventory_amount
  if period > 0:
    min_amount_ordered = 0
    max_amount_ordered = demand[period] + max_inventory_amount
  inventory_states = [i for i in range(min_inventory_amount, max_inventory_amount + 1)]
  amount_states = [i for i in range(min_amount_ordered, max_amount_ordered + 1)]
  print("", end="   ")
  for zi in amount_states:
    print(zi, end="  ")
  print("")
  if period > 0:
    get_min_inventory_cost_util_v2(period, inventory_states, amount_states, function_output_map)
  else:
    get_min_inventory_cost_util_v1(inventory_states, amount_states, function_output_map)
  print("----")
  return get_minimum_order_quantity(function_output_map, period)

demand = [3, 2, 4]
setup_costs = [3, 7, 6]
holding_costs = [1, 3, 2]
initial_inventory_amount = 1

# demand = [5, 2, 3, 3]
# setup_costs = [5, 7, 9, 7]
# holding_costs = [1, 1, 1, 1]
# initial_inventory_amount = 0

problem = {
  "demand": demand,
  "setup_costs": setup_costs,
  "holding_costs": holding_costs,
}

function_output_map = defaultdict(dict)
target_order_amounts = []

print("----")
for period in range(len(demand)):
  print(f"Period = {period+1}")
  min_inventory_cost_for_period(period, problem, function_output_map, initial_inventory_amount)

print(function_output_map)

future_period_quantity_at_start = 0
current_period_ordered_quantity, all_periods_cost = function_output_map[len(demand)-1][future_period_quantity_at_start][0], function_output_map[len(demand)-1][future_period_quantity_at_start][1]
current_period_demand = demand[-1]

comp_value = 0
for current_period in range(len(demand)-1, 0, -1):
  print(f"Z{current_period+1} = {current_period_ordered_quantity}")
  future_period_quantity_at_start = future_period_quantity_at_start + current_period_demand - current_period_ordered_quantity
  current_period_ordered_quantity = function_output_map[current_period-1][future_period_quantity_at_start][0]
  current_period_demand = demand[current_period-1]

print(f"Z1 = {current_period_ordered_quantity}")
print(f"\nTotal period cost = {all_periods_cost}")

  #  = function_output_map[current_period][comp_value][0]
  #  = comp_value
  #  = demand[current_period]
  # value = future_period_quantity_at_start + current_period_demand - current_period_ordered_quantity
  # comp_value = function_output_map[current_period-1][value][0]
  # print(f"x{current_period+2} = {future_period_quantity_at_start}, D{current_period + 1} = {current_period_demand}, z{current_period+1} = {current_period_ordered_quantity}")
  # print(f"z{current_period+1} = {comp_value}")
