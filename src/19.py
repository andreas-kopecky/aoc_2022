import re

import cvxpy as cp
import numpy as np


def optimize(costs: list[int], turns: int) -> int:
    ore_ore, clay_ore, obsidian_ore, obsidian_clay, geode_ore, geode_obsidian = costs
    cost_matrix = np.matrix([
        [ore_ore, clay_ore,  obsidian_ore,      geode_ore], # costs for robots using ore
        [      0,        0, obsidian_clay,              0], # costs for robots using clay
        [      0,        0,             0, geode_obsidian], # costs fore robots using obsidian
        [      0,        0,             0,              0]  # Noone uses geodes for production
    ])

    stash = []      # stash[i] is how many resources are available at turn i
    robots = []     # robots[i] is how many robots are available at turn i
    build_plan = [] # build_plan[i] how many robots to build in turn i, limited by stash[i - 1], limited to 1 per turn

    constraints = []

    for turn in range(0, turns + 1):
        turn_stash = cp.Variable(4)
        turn_robots = cp.Variable(4)
        turn_plan = cp.Variable(4, boolean=True)
        if turn == 0:
            constraints.extend([
                turn_stash == 0,
                turn_robots[0] == 1,
                turn_robots[1:] == 0,
                turn_plan == 0
            ])
        else:
            input_resources = stash[-1] # Resources available start of this turn
            constraints.extend([
                    turn_robots == robots[-1] + build_plan[-1], # Robots available start of this turn
                    cp.sum(turn_plan) <= 1, # Build limit per turn
                    cost_matrix @ turn_plan <= input_resources, # Feasibility of turn building plan
                    turn_stash == (input_resources + turn_robots - (cost_matrix @ turn_plan)) # Resources at the end of the turn

            ])
        stash.append(turn_stash)
        robots.append(turn_robots)
        build_plan.append(turn_plan)

    objective = cp.Maximize(stash[-1][3])
    problem = cp.Problem(objective, constraints)
    return int(problem.solve())


def solve() -> tuple[int, int]:
    with open("../data/19_input.txt", "r") as fh:
        blueprints = [list(map(int, re.findall(r"\d+", line))) for line in fh]

    part_1 = 0
    part_2 = 1
    for i, blueprint in enumerate(blueprints):
        blueprint_id, *costs = blueprint
        part_1 += blueprint_id * optimize(costs, turns=24)
        if i < 3:
            part_2 *= optimize(costs, turns=32)
    return part_1, part_2

if __name__ == "__main__":
    print(solve())
