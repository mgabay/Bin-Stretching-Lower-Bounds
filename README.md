Bin Stretching Lower Bounds
================================

This is a scientific project. The provided code is a proof of concept on how to use game theoretic results to automatically find and prove new lower bounds for online and semi-online scheduling and packing problems.

A paper explaining the ideas and purpose of this project is available on [HAL] [1].

Source code is provided under [CeCILL License] [2].
Any use of this work shall include a citation to [the paper] [1] and [the license] [2].

[1]: http://hal.archives-ouvertes.fr/index.php                    "HAL"
[2]: http://www.cecill.info/licences/Licence_CeCILL_V2.1-en.html  "CeCILL License"


Running program
---------------

The main program can be run using Python interpreter and command:

    python upper_bounding.py C N

Where *C* denotes the capacity of the bins and *N* their numbers.

The optional option `-r R` can be specified to realize a sampling of *R* accepted capacities among the *C* possibly considered.


A few code details
------------------

The code is a proof of concept, it is written in Python and sometimes has to solves exact bin packing problems.
Several approach are implemented to solve exactly the problems. Each of these option can be selected by setting the variable `SOLVER`, in upper_bounding.py to the corresponding value:

1. Constraint programming, using Choco as a solver. Choco is implemented in java,
so an additional component is required for Python to communicate with the jvm.
   * *(Preferred with CPython)* Using JPype to communicate with the jvm. `SOLVER="CHOCO"`
   * *(Preferred with PyPy)* Using Py4J as a communicating component. `SOLVER="CHOCO4J"`
2. Using integer programming.
   * The problem is modeled using PuLP and then, one of the solver compatible
 with PuLP has to be selected. This include:
        * *(Preferred LP solver)* GLPK: `SOLVER="GLPK"`.
        * COIN Cbc: `SOLVER="CBC"`.
        * CPLEX: `SOLVER="CPLEX"`.
        * Gurobi: `SOLVER="GUROBI"`.
        * Various solvers through yaposib. To use it, browse and modify [`bpsolver.py`](bpsolver.py).
   * The model has also been implemented using Gurobi API. To use it, browse and
 modify [`bpsolver.py`](bpsolver.py).

We recommend using the **PyPy** interpreter to run programs. However, PyPy is complicated to interface with JPype. Hence, using PyPy, CHOCO4J is the preferred option for solving bin packing problems.

Referenced projects
-------------------

This project includes Choco 2 which is provided under BSD license.
Details on Choco project and licensing details are available in [`lib/CHOCO.txt`](lib/CHOCO.txt).

Other references projects and their license are:

* PuLP is under MIT License (MIT).
* JPype is under Apache License V2.0.
* Py4J is under BSD License.
* GLPK is under GNU General Public License (GPL).
* COIN Cbc: ​Open source: Eclipse Public License (EPL),
* Yaposib is provided under Eclipse Public License (EPL).
* CPLEX and Gurobi are commercial solvers.
