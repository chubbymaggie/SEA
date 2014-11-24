"Symbolic Exploit Assistant" ( **SEA** ) is a small tool designed to assist the
discovery and construction of exploits in binary programs. SEA is free software 
(GPL3) and includes a minimal toolkit (BSD) to quickly develop binary analysis 
tools in Python.
This project is developed in collaboration between the research institutes
[CIFASIS](http://www.cifasis-conicet.gov.ar/) (Rosario, Argentina) and
[VERIMAG](http://www-verimag.imag.fr) (Grenoble, France) in an effort to improve
security in binary programs.

### Using SEA

We can use SEA to deduce exploitability conditions of binary programs without
executing code. For example, if we have the following assembly code 
(expressed in a simple intermediate language):

```python
1: call
2: t0 := eax xor 42
3: eax := t0
4: ebx := eax + t0
5: if not (t0 == 0) then jump ebx
```

SEA allows us to enforce this particular sequence of instructions in 
order to jump to address **0xdeadc0de**. The tool will track and propagate backwards 
all the constraints required. In this case, SEA detects the **EAX** register as the only free operand
and returns its initial condition:

```python
eax := 0x6f56e06f
```

SEA also performs pointer detection (stack, heap and globals) in traces. These pointers 
can be used to enforce particular memory conditions, even if they require to overflow
buffers. The current implementation can be used to "solve", some of the examples of
[Gera's Insecure Programming](http://community.coresecurity.com/~gera/InsecureProgramming/):

* The [first example of simple buffer overflow on stack](http://community.coresecurity.com/~gera/InsecureProgramming/stack1.html):
  * Compiled with gcc 4.8.0 (default parameters). The complete analysis is [here](https://github.com/neuromancer/SEA/wiki/Warming-up-on-stack-1-gcc). The tool found it 
    solvable if the user inputs data using standard input.
  * Compiled with Visual Studio 2005 (default parameters), The complete analysis is [here](https://github.com/neuromancer/SEA/wiki/Warming-up-the-stack-1-vs2005). The tool founds it is solvable if the user 
    controls the initial value of a local variable (which is usually not possible)

* The [third example of advanced buffer overflow](http://community.coresecurity.com/~gera/InsecureProgramming/abo3.html):
  * Compiled with gcc 4.8.0 (default parameters), The tool founds it is solvable if the user inputs 
    data using command line arguments (allowing to execute a call to system).

Documentation, examples and the complete list of features can be found in the 
[wiki](https://github.com/neuromancer/SEA/wiki). The [issue tracker](https://github.com/neuromancer/SEA/issues) is available.
Discussion for support or collaboration is available in #sea-tool @ irc.freenode.net

### Quick Start

To get started, you should have **Python 2.7**. To prepare the tool, the
official Z3 Python binding ([z3py](http://research.microsoft.com/en-us/um/redmond/projects/z3/)) 
should be installed. Fortunately, just executing **boostrap.sh** will download
and compile z3py.
After it finishes compiling, SEA is ready to be used. 

**NOTE**: Right now, SEA uses REIL code as input, to analyze a path. 
Unfortunately, REIL can be **only** generated from an executable file using
[BinNavi](http://www.zynamics.com/binnavi.html) which runs in the top of
[IDA-Pro](https://www.hex-rays.com/products/ida/index.shtml) (two proprietary and expensive programs)
Hopefully, this will change soon when SEA supports open frameworks for binary
analysis like Bincoa or BAP.
