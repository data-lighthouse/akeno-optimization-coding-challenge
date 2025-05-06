from ortools.sat.python import cp_model
import random
import time

def solve_assignment(jobs, machines, cost, time_limit_s=30):
    """
    Decide assignment of each job to exactly one machine,
    minimizing total cost[job][machine].
    Returns a dict job→machine.
    """
    model = cp_model.CpModel()
    x = {}
    for j in jobs:
        for m in machines:
            x[j, m] = model.NewBoolVar(f"x_{j}_{m}")

    # Each job assigned to exactly one machine
    for j in jobs:
        model.Add(sum(x[j, m] for m in machines) == 1)

    # Objective: minimize total cost
    model.Minimize(sum(cost[j][m] * x[j, m]
                       for j in jobs for m in machines))

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = time_limit_s
    solver.parameters.log_search_progress = True  # enable logging

    print("----- Solving assignment model -----")
    t0 = time.time()
    result = solver.Solve(model)
    t1 = time.time()
    print(f"Assignment solve finished in {t1 - t0:.2f} s\n")

    if result not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        raise RuntimeError("Assignment model infeasible")

    assignment = {
        j: m
        for j in jobs
        for m in machines
        if solver.Value(x[j, m]) == 1
    }

    print("Assignment objective:", solver.ObjectiveValue())
    return assignment


def solve_scheduling(jobs, machines, assignment, processing_time, time_limit_s=30):
    """
    Given assignment[job] = machine, schedule start times to minimize makespan.
    No two jobs on same machine may overlap.
    """
    model = cp_model.CpModel()
    horizon = sum(processing_time[j] for j in jobs)

    start = {}
    end = {}
    interval = {}
    for j in jobs:
        start[j] = model.NewIntVar(0, horizon, f"start_{j}")
        end[j] = model.NewIntVar(0, horizon, f"end_{j}")
        interval[j] = model.NewIntervalVar(
            start[j], processing_time[j], end[j], f"interval_{j}"
        )

    for m in machines:
        assigned = [j for j in jobs if assignment[j] == m]
        if assigned:
            model.AddNoOverlap([interval[j] for j in assigned])

    makespan = model.NewIntVar(0, horizon, "makespan")
    for j in jobs:
        model.Add(end[j] <= makespan)
    model.Minimize(makespan)

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = time_limit_s
    solver.parameters.log_search_progress = True  # enable logging

    print("----- Solving scheduling model -----")
    t0 = time.time()
    result = solver.Solve(model)
    t1 = time.time()
    print(f"Scheduling solve finished in {t1 - t0:.2f} s\n")

    if result not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        raise RuntimeError("Scheduling model infeasible")

    print("Scheduling makespan:", solver.Value(makespan))
    return {j: solver.Value(start[j]) for j in jobs}


if __name__ == "__main__":
    # --- Generate 50000 jobs and 30 machines ---
    random.seed(0)

    num_jobs = 50000
    num_machines = 30

    jobs = list(range(num_jobs))
    machines = list(range(num_machines))

    cost = {
        j: {m: random.randint(80, 100) for m in machines}
        for j in jobs
    }
    processing_time = {
        j: random.randint(20, 500)
        for j in jobs
    }

    # Step 1: solve assignment
    assignment = solve_assignment(jobs, machines, cost, time_limit_s=30)

    # Step 2: solve scheduling given assignment
    schedule = solve_scheduling(jobs, machines, assignment, processing_time, time_limit_s=300)

    # === TODO for applicant ===
    # Wrap the above two-step solve into a Logic-Based Benders Decomposition:
    #  1) Master: assign x[j,m]
    #  2) Subproblem: schedule on fixed assignment
    #  3) Generate Benders cuts (feasibility & optimality)
    #  4) Iterate until convergence