#!/usr/bin/env python
# Proof of concept for solving the poisson equation in 2D using linear finite elements
# and our grid interface

from __future__ import absolute_import, division, print_function, unicode_literals

import sys
import math as m

import numpy as np

from pymor.common import BoundaryType
from pymor.common.domaindescription import RectDomain
from pymor.analyticalproblem import PoissonProblem
from pymor import discretizer

if len(sys.argv) < 4:
    sys.exit('Usage: %s RHS-NUMBER BOUNDARY-DATA-NUMBER NEUMANN-COUNT'.format(sys.argv[0]))

rhs0 = lambda X: np.ones(X.shape[0]) * 10
rhs1 = lambda X: (X[:, 0] - 0.5) ** 2 * 1000
dirichlet0 = lambda X: np.zeros(X.shape[0])
dirichlet1 = lambda X: np.ones(X.shape[0])
dirichlet2 = lambda X: X[:, 0]
domain0 = RectDomain()
domain1 = RectDomain(right=BoundaryType('neumann'))
domain2 = RectDomain(right=BoundaryType('neumann'), top=BoundaryType('neumann'))
domain3 = RectDomain(right=BoundaryType('neumann'), top=BoundaryType('neumann'), bottom=BoundaryType('neumann'))

nrhs = int(sys.argv[1])
assert 0 <= nrhs <= 1, ValueError('Invalid rhs number.')
rhs = eval('rhs{}'.format(nrhs))

ndirichlet = int(sys.argv[2])
assert 0 <= ndirichlet <= 2, ValueError('Invalid boundary number.')
dirichlet = eval('dirichlet{}'.format(ndirichlet))

nneumann = int(sys.argv[3])
assert 0 <= nneumann <= 3, ValueError('Invalid neumann boundary count.')
domain = eval('domain{}'.format(nneumann))


for n in [32, 128]:
    print('Solving on TriaGrid(({0},{0}))'.format(n))

    print('Setup problem ...')
    aproblem = PoissonProblem(domain=domain, rhs=rhs, dirichlet_data=dirichlet)

    print('Discretize ...')
    discrt = discretizer.PoissonCGDiscretizer(diameter=m.sqrt(2) / n)
    discretization = discrt.discretize(aproblem)

    print('Solve ...')
    U = discretization.solve()

    print('Plot ...')
    discretization.visualize(U)

    print('')
