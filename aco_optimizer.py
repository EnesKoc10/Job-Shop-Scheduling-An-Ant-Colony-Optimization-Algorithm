from typing import List
from models import ProblemInstance
from ant import Ant

class ACOOptimizer:
    def __init__(
            self,
            problem: ProblemInstance,
            num_ants: int = 10,
            num_iterations: int = 50,
            evaporation_rate: float = 0.5,
            alpha: float = 1,
            beta: float = 2
    ):
        self.problem = problem
        self.num_ants = num_ants
        self.num_iterations = num_iterations
        self.evaporation_rate = evaporation_rate
        self.alpha = alpha
        self.beta = beta

        self.pheromone = [
            [1.0 for _ in range(len(job))] for job in self.problem.jobs
        ]
        self.heuristic = [
            [1.0 / op.processing_time for op in job.operations] for job in self.problem.jobs
        ]

    def run(self):
        best_schedule = None
        best_makespan = float('inf')

        for iteration in range(self.num_iterations):
            ants = [Ant(self.problem) for _ in range(self.num_ants)]
            all_schedules = []

            for ant in ants:
                ant.construct_solution(self.pheromone, self.heuristic, self.alpha, self.beta)
                if ant.makespan < best_makespan:
                    best_makespan = ant.makespan
                    best_schedule = ant.schedule
                all_schedules.append(ant)

            self._update_pheromones(all_schedules)
            print(f"[Iteration {iteration + 1}] Best Makespan so far: {best_makespan}")

        return best_schedule

    def _update_pheromones(self, ants: List[Ant]):
        #Updates pheromone matrix based on all ants schedules.
        for i in range(len(self.pheromone)):
            for j in range(len(self.pheromone[i])):
                self.pheromone[i][j] *= (1 - self.evaporation_rate)

        for ant in ants:
            for op in ant.schedule:
                self.pheromone[op.job_id][op.order] += 1.0 / ant.makespan