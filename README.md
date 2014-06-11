Bin Stretching Lower Bounds
================================

This is a scientific project. The code is a proof of concept on how to use game theory results to automatically find and prove new lower bounds for online and semi-online scheduling and packing problems.

This program aim at finding and proving new lower bounds for the bin stretching problem.
A detailed paper, explaining the ideas and purpose of this project is available on [HAL] [1].

Source code is provided under [CeCILL License] [2].
Any use of this work shall cite both [the paper] [1] and this project with [its license] [2].

[1]: http://hal.archives-ouvertes.fr/hal-00921663                 "HAL"
[2]: http://www.cecill.info/licences/Licence_CeCILL_V2.1-en.html  "CeCILL License"


Installation
------------

The configuration file `py/config.conf` is the only file to configure.
The path of the java virtual machine shall be specified.

Other options can remain unchanged, unless directories are reorganized or the user wants to use a different solver.

The program dependencies are Python and PyYaml (to parse configuration files). For the other dependencies, imports are done dynamically, so only one of the following dependencies needs to be satisfied:
 * Choco (provided) and JPype
 * Choco (provided) and Py4J
 * PuLP and an LP solver among GLPK/Cbc/CPLEX/Gurobi
 * Gurobi with its python bindings


Running program
---------------

The main program can be run using Python interpreter and command:

    python py/upper_bounding.py C N

Where *C* denotes the capacity of the bins and *N* their numbers.

The optional option `-r R` can be specified to realize a sampling of *R* accepted capacities among the *C* possibly considered.

A file named backtrack.dot is generated. If the lower bound is improved, the decision tree is written to this file.
This file is in Dot (GraphViz) format. You can generate a picture from it using the command:

    dot -Tpdf backtrack.dot -o file.pdf


A few code details
------------------

The code is a proof of concept, it is written in Python.
In the course of the algorithm, some bin packing problems have to be solved exactly. Several approach are implemented to solve this problem. Each of these can be selected by setting the variable `solver`, in [the configuration file](py/config.conf). The available approaches are:

1. Constraint programming, using Choco as a solver. Choco is implemented in java, so an additional component is required for Python to communicate with the jvm.
   * *(Preferred with CPython)* Using JPype to communicate with the jvm. `solver: CHOCO`
   * *(Preferred with PyPy)* Using Py4J as a communicating component. `solver: CHOCO4J`
2. Using integer programming.
   * The problem is modeled using PuLP and then, one of the solver compatible with PuLP has to be selected:
        * *(Preferred LP solver)* GLPK: `solver: GLPK`.
        * COIN Cbc: `solver: CBC`.
        * CPLEX: `solver: CPLEX`.
        * Gurobi: `solver: GUROBI`.
        * Various solvers through yaposib. To use it, browse and modify [`bpsolver.py`](py/bpsolver.py).
   * The model has also been implemented using Gurobi's API. To use it, browse and modify [`bpsolver.py`](py/bpsolver.py).

We recommend using the **PyPy** interpreter to run programs. However, PyPy is complicated to interface with JPype. Hence, using PyPy, CHOCO4J is the preferred option for solving bin packing problems.


Referenced projects
-------------------

This project includes Choco 2 which is provided under BSD license.
Details on Choco project and licensing details are available in [`lib/CHOCO.txt`](lib/CHOCO.txt).

Other referenced projects and their licenses:

* PuLP is under MIT License (MIT).
* JPype is under Apache License V2.0.
* Py4J is under BSD License.
* GLPK is under GNU General Public License (GPL).
* COIN Cbc is under Eclipse Public License (EPL),
* Yaposib is under Eclipse Public License (EPL).
* CPLEX and Gurobi are commercial solvers.
