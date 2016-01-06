import unittest
import numpy as np

from _test import _TestBase
from current import *
from field import *
from material import *
from mesh import *
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

# Measure fields at two positions at the same H-plane.  Thus, the EField should be the same, but HField heads to the directions that are in 90 degree phase difference.
Ro1 = Vector(5, 0, 0)
Ro2 = Vector(0, 0, 5)
E1, H1 = a.radiate2(Ro1)
E2, H2 = a.radiate2(Ro2)

P1 = a.Poynting(Ro1)
P2 = a.Poynting(Ro2)

class TestField(_TestBase):
    def testEField1(self):
        answers = [-0.1328, 0.1149]  ## Answers from page 45 of the Makarov's book.  Same as HField below.
        tobeTest = [E1[1].real, E1[1].imag]
        self._testCloseEnough(tobeTest, answers, tolerance = 0.02)

    def testHField1(self):
        answers = [0.00003595, -0.000031121]
        tobeTest = [H1[2].real, H1[2].imag]
        self._testCloseEnough(tobeTest, answers, tolerance = 1e-3)

    def testEField_at_two_positions(self):
        self._testCloseEnough(E1, E2, tolerance = 1e-3)

    def testHField_at_two_positions(self):
        self.assertLess(abs(H1.dot(H2)),  1e-3)

    def testPoynting1(self):
        answers = [4.1e-5, 0, 0]
        self._testCloseEnough(P1, answers, tolerance = 1e-6)

    def testPoynting2(self):
        answers = [0, 0, 4.1e-5]
        self._testCloseEnough(P2, answers, tolerance = 1e-6)
        
if __name__ == '__main__':
    unittest.main()

