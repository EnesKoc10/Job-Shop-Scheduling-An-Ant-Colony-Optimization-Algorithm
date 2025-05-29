from dataclasses import dataclass, field
from typing import List, Tuple, Optional


@dataclass
class Operation:
    job_id: int
    machine_id: int
    processing_time: int
    order: int
    start_time: Optional[int] = None
    end_time: Optional[int] = None

    def __repr__(self):
        return f"Op(J{self.job_id}, M{self.machine_id}, T{self.processing_time})"

@dataclass
class Job:
    job_id: int
    raw_operations: List[List[Tuple[int, int]]]
    operations: List[Operation] = field(init=False)

    def __post_init__(self):
        self.operations = []
        for proc_step, machine_options in enumerate(self.raw_operations):
            # Her işlem adımı için sadece bir makine seçilebilir
            machine_id, proc_time = machine_options[0]  # Varsayılan olarak ilk makineyi seç
            self.operations.append(Operation(self.job_id, machine_id, proc_time, proc_step))

    def __len__(self):
        return len(self.operations)

    def __getitem__(self, idx):
        return self.operations[idx]

    def __repr__(self):
        return f"Job{self.job_id}: {self.operations}"

class ProblemInstance:

    def __init__(self, data: List[List[List[Tuple[int, int]]]], alt_selection: Optional[List[int]] = None):
        if alt_selection is None:
            alt_selection = [0] * len(data)  # Her iş için varsayılan olarak ilk alternatif

        self.jobs: List[Job] = [
            Job(job_id, data[job_id])
            for job_id in range(len(data))
        ]
        self.num_jobs = len(self.jobs)
        self.num_machines = self._count_machines()

    def _count_machines(self) -> int:
        """
        Count the total number of machines by finding the maximum machine ID + 1
        """
        max_machine_id = -1
        for job in self.jobs:
            for proc_step in job.raw_operations:
                for machine_id, _ in proc_step:
                    max_machine_id = max(max_machine_id, machine_id)
        return max_machine_id + 1  # +1 because machine IDs are 0-based

    def get_operations(self) -> List[Operation]:
        return [op for job in self.jobs for op in job.operations]

    def __repr__(self):
        return f"JSSP with {self.num_jobs} jobs and {self.num_machines} machines"