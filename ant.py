import random
from models import ProblemInstance, Operation
import copy


class Ant:
    def __init__(self, problem: ProblemInstance):
        self.problem = problem
        self.schedule = []
        self.makespan = None

    def construct_solution(self, pheromone, heuristic, alpha, beta):
        # Her iş için mevcut işlem adımını takip et
        current_step = [0] * self.problem.num_jobs
        operations = [copy.deepcopy(job.operations) for job in self.problem.jobs]
        schedule = []
        machine_time = [0] * self.problem.num_machines
        job_time = [0] * self.problem.num_jobs

        while any(current_step[job_id] < len(self.problem.jobs[job_id].raw_operations) for job_id in range(self.problem.num_jobs)):
            eligible_ops = []
            for job_id in range(self.problem.num_jobs):
                if current_step[job_id] < len(self.problem.jobs[job_id].raw_operations):
                    # Mevcut işlem adımı için makine seçeneklerini al
                    machine_options = self.problem.jobs[job_id].raw_operations[current_step[job_id]]
                    # Her makine seçeneği için bir operasyon oluştur
                    for machine_id, proc_time in machine_options:
                        if machine_id < self.problem.num_machines:  # Makine ID'sinin geçerli olduğundan emin ol
                            op = Operation(job_id, machine_id, proc_time, current_step[job_id])
                            eligible_ops.append(op)

            if not eligible_ops:  # Eğer uygun operasyon yoksa döngüden çık
                break

            probabilities = []
            total = 0
            for op in eligible_ops:
                tau = pheromone[op.job_id][op.order]
                eta = heuristic[op.job_id][op.order]
                prob = (tau ** alpha) * (eta ** beta)
                probabilities.append(prob)
                total += prob

            if total == 0:
                selected = random.choice(eligible_ops)
            else:
                r = random.uniform(0, total)
                cumulative = 0
                for i, op in enumerate(eligible_ops):
                    cumulative += probabilities[i]
                    if r <= cumulative:
                        selected = op
                        break

            start = max(machine_time[selected.machine_id], job_time[selected.job_id])
            end = start + selected.processing_time
            selected.start_time = start
            selected.end_time = end

            machine_time[selected.machine_id] = end
            job_time[selected.job_id] = end
            schedule.append(selected)

            # Seçilen işin bir sonraki adımına geç
            current_step[selected.job_id] += 1

        self.schedule = schedule
        self.makespan = max(op.end_time for op in schedule) if schedule else float('inf')
        return schedule