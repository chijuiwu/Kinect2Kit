# playground
[![Build Status](https://travis-ci.org/chutsu/playground.png)][1]
[![Coverage Status](https://coveralls.io/repos/chutsu/playground/badge.png)][5]

Playground is an Meta-heuristic library implemented in Python.
Currently features:

- Hill Climbing
- Genetic Programming
    - Tree
    - Cartesian (In Development)
- Genetic Algorithm
- Particle Swarm Optimization


## Install
Currently the best way is to clone the repo and install the dependencies:

    git clone git@github.com:chutsu/playground.git
    pip install -r requirements.txt  # installs dependencies for playground

## Examples
At the moment the best example is the [symbolic regression][4] example.  ([what
is symbolic regression?][3]):

    # curve fitting - genetic programming
    cd examples/symbolic_regression
    python symbolic_regression.py  # takes a while (20 generations)

The example uses data in `examples/symbolic_regression/sine.dat` to find the
answer (an equation), this is also an example of data-driven search.

Others include:

    # HILL CLIMBING
    # find the word "hello world!"
    cd examples/climbing
    python hill_climbing.py

    # GENETIC ALGORITHM
    # find the word "hello world!"
    cd examples/hello_world
    python hello_world.py

    # PARTICLE SWARM OPTIMIZATION
    # find the most optimal point in a x-y graph
    cd examples/pso
    python pso.py


## Licence
LGPL License
Copyright (C) <2013> Chris Choi

This program is free software: you can redistribute it and/or modify it under
the terms of the Lesser GNU General Public License as published by the Free
Software Foundation, either version 3 of the License, or (at your option) any
later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program.  If not, see <http://www.gnu.org/licenses/>.

[1]: https://travis-ci.org/chutsu/playground
[3]: http://www.symbolicregression.com/?q=faq
[4]: https://github.com/chutsu/playground/tree/master/examples/symbolic_regression
[5]: https://coveralls.io/r/chutsu/playground