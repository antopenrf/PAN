import unittest
import numpy as np

from _test import _TestBase
from current import *
from field import *
from material import *
from mesh import *
from pattern import *
from rwg import *


### Set up dipole structure for unittest.
freq = 75 #MHz

structure = Mesh('patch', 'plate', 0.05, 2, 1, 30)

rwg1(structure)
rwg2(structure)
mat_prop = Material(epsilon_r = 1, mu_r = 1)
rwg3(structure, mat_prop)
Z = impmat(structure, freq)
Vx = rwg4(structure, freq, incidence = [0,0,-1], pol=[0,1,0])

Isource = Current(freq)
Isource.Im = [complex(each[0]) for each in np.linalg.solve(Z, Vx)]

a = Field(structure, Isource)
p = Pattern(a, step = 30, distance = 5)


class TestPattern(_TestBase):
    def testTRPandD(self):
        answers = [8, 1.6]  ## TRP: 8mw, D: 2
        tobeTest = p.TRP*1000, p.directivity
        self._testCloseEnough(tobeTest, answers, tolerance = 0.1)

if __name__ == '__main__':
    unittest.main()

