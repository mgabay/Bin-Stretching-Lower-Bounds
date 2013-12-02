################################################################################
# Copyright (c) 1999-2010, Ecole des Mines de Nantes                           #
# All rights reserved.                                                         #
# Redistribution and use in source and binary forms, with or without           #
# modification, are permitted provided that the following conditions are met:  #
#                                                                              #
#     * Redistributions of source code must retain the above copyright         #
#       notice, this list of conditions and the following disclaimer.          #
#     * Redistributions in binary form must reproduce the above copyright      #
#       notice, this list of conditions and the following disclaimer in the    #
#       documentation and/or other materials provided with the distribution.   #
#     * Neither the name of the Ecole des Mines de Nantes nor the              #
#       names of its contributors may be used to endorse or promote products   #
#       derived from this software without specific prior written permission.  #
#                                                                              #
# THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS'' AND ANY  #
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED    #
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE       #
# DISCLAIMED. IN NO EVENT SHALL THE REGENTS AND CONTRIBUTORS BE LIABLE FOR ANY #
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES   #
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; #
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND  #
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT   #
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS#
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.                 #
################################################################################

 CHOCO
 -----

 CHOCO is a java library for constraint satisfaction problems (CSP) and constraint programming (CP).
 It is built on an event-based propagation mechanism with backtrackable structures.

 CHOCO can be used for:

 > teaching (as a user-oriented constraint solver with open-source code)
 > research (for state-of-the-art algorithms and techniques, user-defined constraints, domains and variables)
 > real-life applications (many applications now embed choco)

 Please visit the project web site (http://choco.emn.fr) for more information.

 REQUIREMENTS
 ------------

 > A Java 6 or later compatible virtual machine for your operating system.

 DOCUMENTATION
 -------------

 Look for the most up-to-date documentation on the CHOCO web site, under the Documentation menu
 (http://choco.emn.fr/choco-documentation.html)

 RELEASE
 -------

 The choco-2.1.5.zip file is composed of the following directories and files:

 > choco-solver: a JAR file providing tools for modeling and solving problems using CP (the heart of CHOCO)
 > choco-solver-cpviz: choco-solver + CP-Viz wrapper (using AOP), a JAR file providing tool for modeling and solving
    problems using CP and also producing XML files for CP-Viz (web site: http://sourceforge.net/projects/cpviz/)
 > extra: directory with extra JARs:
    > choco-db: a database toolbox, interfacing choco-solver
    > choco-parsers: parser interface and implementations (CSC, FZN) for choco-solver
    > choco-cli: Command-Line Interpreter facilities for choco-solver, choco-db and choco-parsers
    > choco-visu: "alive" visualization toolbox
 > samples: a directory of runnable classes of problems modeled and solved with choco-solver
 > apidocs: javadoc repository
 > documentation PDF file

-------------------------
 choco-2.1.5.zip
 |-- apidocs			             	        // javadoc files
 |-- choco-doc-2.1.5.pdf		        // Documentation
 |-- choco-solver-2.1.5.jar	        // CHOCO solver
 |-- choco-solver-2.1.5-with-sources.jar   // Sources of CHOCO solver
 |-- choco-solver-cpviz-2.1.5.jar		// CHOCO solver + CP Viz logs
 |-- extra
 |	|-- choco-db-2.1.5.jar 	    	// Database insertion tool
 |	|-- choco-parsers-2.1.5.jar    	// Parsers interfaces + MZN + FCSP
 |	|-- choco-cli-2.1.5.jar            // Command Line Interpreter
 |	`-- choco-visu-2.1.5.jar           // Visualization tool box
 |-- samples-2.1.5.jar			// Samples of CHOCO programs
 `-- README
 -------------------------