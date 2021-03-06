from framework import *
from deliveries import *

from matplotlib import pyplot as plt
import numpy as np
from typing import List, Union

# Load the map
roads = load_map_from_csv(Consts.get_data_file_path("tlv.csv"))

# Make `np.random` behave deterministic.
Consts.set_seed()


# --------------------------------------------------------------------
# -------------------------- Map Problem -----------------------------
# --------------------------------------------------------------------

def plot_distance_and_expanded_wrt_weight_figure(
            weights: Union[np.ndarray, List[float]],
        total_distance: Union[np.ndarray, List[float]],
        total_expanded: Union[np.ndarray, List[int]]):
    """
    Use `matplotlib` to generate a figure of the distance & #expanded-nodes
     w.r.t. the weight.
    """
    assert len(weights) == len(total_distance) == len(total_expanded)

    fig, ax1 = plt.subplots()
    ax1.plot(weights, total_distance, 'b-')
    # ax1: Make the y-axis label, ticks and tick labels match the line color.
    ax1.set_ylabel('distance traveled', color='b')
    ax1.tick_params('y', colors='b')
    ax1.set_xlabel('weight')

    # Create another axis for the #expanded curve.
    ax2 = ax1.twinx()
    ax2.plot(weights, total_expanded, 'r-')
    ax2.set_ylabel('states expanded', color='r')
    ax2.tick_params('y', colors='r')
    ax2.set_xlabel('weight')
    fig.tight_layout()
    plt.show()


def run_astar_for_weights_in_range(heuristic_type: HeuristicFunctionType, problem: GraphProblem):
    # TODO:
    # 1. Create an array of 20 numbers equally spreaded in [0.5, 1]
    #    (including the edges). You can use `np.linspace()` for that.
    sample_array = np.linspace(0.5,1,20)
    cost_array = []
    expanded_array = []
    for sample in sample_array:
        star = AStar(heuristic_type,sample)
        res = star.solve_problem(problem)
        cost_array.append(res.final_search_node.cost)
        expanded_array.append(res.nr_expanded_states)
    plot_distance_and_expanded_wrt_weight_figure(sample_array, cost_array, expanded_array)

    # 2. For each weight in that array run the A* algorithm, with the
    #    given `heuristic_type` over the map problem. For each such run, =
    #    store the cost of the solution (res.final_search_node.cost)
    #    and the number of expanded states (res.nr_expanded_states).
    #    Store these in 2 lists (array for the costs and array for
    #    the #expanded.
    # Call the function `plot_distance_and_expanded_by_weight_figure()`
    #  with that data.



def map_problem():
    print()
    print('Solve the map problem.')

    # Ex.8
    map_prob = MapProblem(roads, 54, 549)
    uc = UniformCost()
    res = uc.solve_problem(map_prob)
    print(res)

    astar = AStar(NullHeuristic)
    res = astar.solve_problem(map_prob)
    print(res)

    astar = AStar(AirDistHeuristic)
    res = astar.solve_problem(map_prob)
    print(res)

    run_astar_for_weights_in_range(AirDistHeuristic, map_prob)





# --------------------------------------------------------------------
# ----------------------- Deliveries Problem -------------------------
# --------------------------------------------------------------------

def relaxed_deliveries_problem():

    print()
    print('Solve the relaxed deliveries problem.')

    big_delivery = DeliveriesProblemInput.load_from_file('big_delivery.in', roads)
    big_deliveries_prob = RelaxedDeliveriesProblem(big_delivery)

    astar = AStar(MaxAirDistHeuristic)
    res = astar.solve_problem(big_deliveries_prob)
    print(res)

    astar = AStar(MSTAirDistHeuristic)
    res = astar.solve_problem(big_deliveries_prob)
    print(res)
    run_astar_for_weights_in_range(MSTAirDistHeuristic, big_deliveries_prob)


    # Ex.18
    # TODO: Call here the function `run_astar_for_weights_in_range()`
    #       with `MSTAirDistHeuristic` and `big_deliveries_prob`.


    # Ex.24
    # TODO:
    # 1. Run the stochastic greedy algorithm for 100 times.
    #    For each run, store the cost of the found solution.
    #    Store these costs in a list.

    costs = []
    anytime =[]
    k= 100
    for i in range(k):
        stochastic = GreedyStochastic(MSTAirDistHeuristic)
        costs.append(stochastic.solve_problem(big_deliveries_prob).final_search_node.cost)
        anytime.append( min(anytime[i-1], costs[i]) if i > 0 else costs[i] )
    # 2. The "Anytime Greedy Stochastic Algorithm" runs the greedy
    #    greedy stochastic for N times, and after each iteration
    #    stores the best solution found so far. It means that after
    #    iteration #i, the cost of the solution found by the anytime
    #    algorithm is the MINIMUM among the costs of the solutions
    #    found in iterations {1,...,i}. Calculate the costs of the
    #    anytime algorithm wrt the #iteration and store them in a list.
    astar_res2 = [AStar(MSTAirDistHeuristic,0.5).solve_problem(big_deliveries_prob).final_search_node.cost]*k
    gredy_res = [AStar(MSTAirDistHeuristic,1).solve_problem(big_deliveries_prob).final_search_node.cost]*k
    # 3. Calculate and store the cost of the solution received by
    #    the A* algorithm (with w=0.5).
    # 4. Calculate and store the cost of the solution received by
    #    the deterministic greedy algorithm (A* with w=1).
    # 5. Plot a figure with the costs (y-axis) wrt the #iteration
    #    (x-axis). Of course that the costs of A*, and deterministic
    #    greedy are not dependent with the iteration number, so
    #    these two should be represented by horizontal lines.
    plt.plot(range(k), costs, label="stochastic")
    plt.plot(range(k), anytime, label="anytime")
    plt.plot(range(k), astar_res2, label="Astar")
    plt.plot(range(k), gredy_res, label="Greedy")
    plt.xlabel("Iter")
    plt.ylabel("cost")
    plt.title("Stochastic as a function of the Iteration")
    plt.legend()
    plt.grid()
    plt.show()



def strict_deliveries_problem():
    print()
    print('Solve the strict deliveries problem.')

    small_delivery = DeliveriesProblemInput.load_from_file('small_delivery.in', roads)
    small_deliveries_strict_problem = StrictDeliveriesProblem(
        small_delivery, roads, inner_problem_solver=AStar(AirDistHeuristic))

    run_astar_for_weights_in_range(MSTAirDistHeuristic, small_deliveries_strict_problem)
    res = AStar(RelaxedDeliveriesHeuristic).solve_problem(small_deliveries_strict_problem)
    print(res)

    # Ex.26
    # TODO: Call here the function `run_astar_for_weights_in_range()`
    #       with `MSTAirDistHeuristic` and `big_deliveries_prob`.


    # Ex.28
    # TODO: create an instance of `AStar` with the `RelaxedDeliveriesHeuristic`,
    #       solve the `small_deliveries_strict_problem` with it and print the results (as before).



def main():
    map_problem()
    relaxed_deliveries_problem()
    strict_deliveries_problem()


if __name__ == '__main__':
    main()
