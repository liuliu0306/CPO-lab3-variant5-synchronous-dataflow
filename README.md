
# GROUP -> HDU123 - Liu Riheng & Chen Weite - lab 3 - variant 5 - synchronous dataflow

# Student number

Liu Riheng 212320037
Chen Weite 212320039

## Laboratory work description

- A graph can represent a dataflow. Each node represents an action.
Each edge – data transfers.

- A node can be activated when all input edges received tokens and consume only
one value from each. After activation,
the node should provide a single tag on each output.

- Input nodes can be manually activated in the simulation process by a user.
Run-time error should be processed correctly.

- You should use the default Python logging module to make the interpreter work transparent.
Should provide complex examples such as a quadratic formula and RS-trigger.

- Visualization by a dataflow graph and as a dataflow graph with trace annotation.

## Features

- Each round loops for each node:
Update activation status -> get tokens ->perform node operations -> update activation status

- Implementation strategy:
Add a token array to each edge based on the traditional graph data structure,
which is convenient for saving temporary data. 
Immediately after the calculation of each node is completed,
the token array of each edge is executed in a loop until the token array
of all nodes except the final node is empty.

## Project structure

- `SDF.py` -- Implementation the class of `synchronous dataflow` and `Node`.

- `SDF_test.py` -- Unit PBT tests for `SDF.py`.

- `figure` -- Synchronize data flow graph and save the SDF graph of each data change.

- `log` -- logging every time the data changes.

## Contribution

- Liu Riheng
1. Implement `SDF.py`.
2. Analyze the characteristics of the SDF and model the task.

- Chen Weite
1. Implement `SDF_test.py`.

## Changelog

- 10.06.2022 - 0
1. Initial.
2. Implement `SDF.py` and `SDF_test.py`.
3. GitHub active successfully.
4. Update README.

