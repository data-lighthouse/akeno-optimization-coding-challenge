# Task Description
## Situation Summary
There are two solvers provided in a very simple example. The first one assigns the jobs to machines and the second one schedules them. Both only work against a single objective.

## Task
The duration it takes currently to run either 50.000 jobs or 500.000 jobs is just very high. We want to reduce this and yield better results by using Logic-Based Benders Decomposition.
Implement in the given script a logic-based benders decomposition, so that the assignment solver carries the master problem and the schedule solver carries the sub-problem.

## Further information
- You can exchange the solvers if you want to, but only use open source solvers. We would prefer you sticking with cpsat, but if necessary, you can pivot.
- Do a little evaluation (nothing interactive needed!) how your approach yields to different solving durations and as well compare the two objectives.
- There is no global optimality needed, an optimality gap of up to 10% is okay if you can achieve significant speed up.
- You can also go with any kind of benders cuts (analytics etc.).

## How to submit
- Please open a PR on this repo to submit your results.