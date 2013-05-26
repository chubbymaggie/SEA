### Description

"Symbolic Exploit Assistant" ( **SEA** ) is a small tool designed to assist the discovery and construction of exploits in binary programs. SEA is free software (GPL3) and includes a minimal toolkit (BSD) to quickly develop binary analisys tools in Python.

This project is developed in colaboration between the research institutes [CIFASIS](http://www.cifasis-conicet.gov.ar/) (Rosario, Argentina) and [VERIMAG](http://www-verimag.imag.fr) (Grenoble, France) in an effort to improve security in binary programs.

### Features

* Fully symbolic analysis.
* Assisted exploitation of stack overflow.
* Assisted exploitation of dangling pointers.
* Detection of unfeasible paths.
* Detection of heap overflow, memory leaks and use-after-free.
* Intra-procedual support (wip).

### Development

The master branch represents a POC of SEA. A cleaned and extensible version of this tool is being developed 
in the work in progress (wip) branch as well as the toolkit for binary analysis in Python. Some of the 
features are broken in the wip branch right now. 

Documentation, examples and more can be found in the [wiki](https://github.com/neuromancer/SEA/wiki). The [issue tracker](https://github.com/neuromancer/SEA/issues) is available.
Discusson for support or collaboration is available in #sea-tool @ irc.freenode.net

### Quick Start

To get started, you should have **Python 2.7**. To prepare the tool, the official Z3 Python binding ([z3py](http://research.microsoft.com/en-us/um/redmond/projects/z3/)) should be installed. Fortunately, just executing **boostrap.sh** will download and compile z3py.

After it finishes compiling, SEA is ready to be used. You can test SEA analyzing the converted code of the [first example](http://community.corest.com/~gera/InsecureProgramming/stack1.html) of Gera's Insecure Programming:

    ./SEA.py tests/reil/stack1_gcc.reil
    
The **complete analysis** of this example can be found [here](https://github.com/neuromancer/SEA/wiki/Warming-up-on-stack---1).
Another interesting example to test detection of memory use is:

    ./SEA.py tests/reil/uaf_1.reil

An **explained analysis** of it is [here](https://github.com/neuromancer/SEA/wiki/Use-after-free-1).

**NOTE**: Right now, SEA uses REIL code as input, to analyze a path. Unfortunately, REIL can be **only** generated from an executable file using [BinNavi](http://www.zynamics.com/binnavi.html) which runs in the top of [IDA-Pro](https://www.hex-rays.com/products/ida/index.shtml) (two proprietary and expensive programs)
In the wip branch, the support of BAP aims to fix this issue.
