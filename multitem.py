import matplotlib.pyplot as plt
from scipy import optimize
import numpy as np
from dataclasses import dataclass

@dataclass
class InventoryItem:
    setup_cost: float
    demand: float
    holding_cost: float
    area: float

def build_objective_fn(items: list[InventoryItem]):
    def objective_fn(x):
        val = 0
        for index, item in enumerate(items):
            val += item.setup_cost * item.demand/x[index] + item.holding_cost * x[index]/2

        return val
    return objective_fn


def build_constraint_fn(items: list[InventoryItem], total_area: float):
    def constraint(x):
        # sum should be less than total_area available
        return total_area - np.sum([xi*item.area for item, xi in zip(items, x)])
    return constraint

def no_setup_cost_model(items: list[InventoryItem], total_area: float):
    objective_fn = build_objective_fn(items)
    constraint = build_constraint_fn(items, total_area)
    initial_guess_values = [1] * len(items)
    result = optimize.minimize(objective_fn, initial_guess_values, constraints={"fun": constraint, "type": "ineq"}, bounds=((0, 10000), (0, 10000), (0, 10000)))
    print(f"Optimal order quantities: {list(result['x'])}")

    print(f"TCU={result['fun']}")

if __name__ == "__main__":
    items = [InventoryItem(10, 2, 0.30, 1),
    InventoryItem(5, 4, 0.10, 1),
    InventoryItem(15, 4, 0.20, 1)
    ]
    no_setup_cost_model(items, 25)
