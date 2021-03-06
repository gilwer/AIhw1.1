from .graph_problem_interface import *
from .best_first_search import BestFirstSearch
from typing import Optional
import numpy as np


class GreedyStochastic(BestFirstSearch):
    def __init__(self, heuristic_function_type: HeuristicFunctionType,
                 T_init: float = 1.0, N: int = 5, T_scale_factor: float = 0.95):
        # GreedyStochastic is a graph search algorithm. Hence, we use close set.
        super(GreedyStochastic, self).__init__(use_close=True)
        self.heuristic_function_type = heuristic_function_type
        self.T = T_init
        self.N = N
        self.T_scale_factor = T_scale_factor
        self.solver_name = 'GreedyStochastic (h={heuristic_name})'.format(
            heuristic_name=heuristic_function_type.heuristic_name)

    def _init_solver(self, problem: GraphProblem):
        super(GreedyStochastic, self)._init_solver(problem)
        self.heuristic_function = self.heuristic_function_type(problem)

    def _open_successor_node(self, problem: GraphProblem, successor_node: SearchNode):
        """
        TODO: implement this method!
        """
        if self.open.has_state(successor_node.state):
            old_node = self.open.get_node_by_state(successor_node.state)
            if old_node.expanding_priority > successor_node.expanding_priority:
                self.open.extract_node(old_node)
                self.open.push_node(successor_node)
        elif self.close.has_state(successor_node.state):
            old_node = self.close.get_node_by_state(successor_node.state)
            if old_node.expanding_priority > successor_node.expanding_priority:
                self.close.remove_node(old_node)
                self.open.push_node(successor_node)
        else:
            self.open.push_node(successor_node)

    def _calc_node_expanding_priority(self, search_node: SearchNode) -> float:
        """
        TODO: implement this method!
        Remember: `GreedyStochastic` is greedy.
        """
        return self.heuristic_function.estimate(search_node.state)

    def _extract_next_search_node_to_expand(self) -> Optional[SearchNode]:
        """
        Extracts the next node to expand from the open queue,
         using the stochastic method to choose out of the N
         best items from open.
        TODO: implement this method!
        Use `np.random.choice(...)` whenever you need to randomly choose
         an item from an array of items given a probabilities array `p`.
        You can read the documentation of `np.random.choice(...)` and
         see usage examples by searching it in Google.
        Notice: You might want to pop min(N, len(open) items from the
                `open` priority queue, and then choose an item out
                of these popped items. The other items have to be
                pushed again into that queue.
        """
        X = []
        n = min(self.N, len(self.open))
        for i in range(n):
             X.append(self.open.pop_next_node())

             if X[i].expanding_priority == 0.0: return X[i]
        deno = 0
        alpha = X[0].expanding_priority
        for j in range(n):
            deno += pow(X[j].expanding_priority/alpha, -1 / self.T)
        P = []
        for i in range(n):
            P.append(pow(X[i].expanding_priority/alpha, -1 / self.T)/deno)
        res = np.random.choice(X, None, False, P)
        self.T = self.T*self.T_scale_factor     # calculates T for next round
        for state in X:     # reinserts states that where not chosen
            if state == res:
                continue
            self.open.push_node(state)
        return res
