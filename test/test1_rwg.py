import unittest

import numpy as np

from _test import _TestBase
from material import *
from mesh import *
from rwg import *


structure = Mesh('patch', 'plate', 18, 18, 2, 2)
points = structure.points
triangles = structure.triangles

rwg1(structure)
rwg2(structure)
mat_prop = Material(epsilon_r = 1, mu_r = 1)
rwg3(structure, mat_prop)
Z = impmat(structure, freq = 300)
Vx = rwg4(structure, freq = 300, incidence = [0,0,-1], pol=[1,0,0])
Ix = np.linalg.solve(Z, Vx)
Jm = rwg5(structure, Ix)

edges = structure.edge_
area = structure.area
center = structure.center
center_ = structure.center_
triangle_plus = structure.triangle_plus
triangle_minus = structure.triangle_minus
rho_plus = structure.rho_plus
rho_minus = structure.rho_minus
FactorA = structure.FactorA
FactorFi= structure.FactorFi



class TestMeshPlate(_TestBase):
    def testPoints(self):
        answers = [(-9.0, -9.0), (-9.0, 0.0), (-9.0, 9.0), (0.0, -9.0), (0.0, 0.0), (0.0, 9.0), (9.0, -9.0), (9.0, 0.0), (9.0, 9.0)]
        self._testEqual(points, answers)

    def testTriangles(self):
        answers = [(1, 3, 4), (3, 1, 0), (3, 7, 4), (7, 3, 6), (5, 1, 4), (1, 5, 2), (7, 5, 4), (5, 7, 8)]
        self._testEqual(triangles, answers)


class Test_RWG1(_TestBase):
    def testEdge(self):
        answers = [(1, 3), (3, 4), (1, 4), (3, 7), (7, 4), (5, 1), (5, 4), (7, 5)]
        self._testEqual(edges, answers)

    def testTriMinus(self):
        answers = [1, 2, 4, 3, 6, 5, 6, 7]
        self._testEqual(triangle_minus, answers)

    def testTriPlus(self):
        answers = [0, 0, 0, 2, 2, 4, 4, 6]
        self._testEqual(triangle_plus, answers)

    def testArea(self):
        answers = [40.5,]*len(triangles)
        self._testEqual(area, answers)

    def testCenter(self):
        answers = [(-3.0, -3.0, 0.0), (-6.0, -6.0, 0.0), (3.0, -3.0, 0.0), (6.0, -6.0, 0.0), (-3.0, 3.0, 0.0), (-6.0, 6.0, 0.0), (3.0, 3.0, 0.0), (6.0, 6.0, 0.0)]
        answers = [list(each) for each in answers]
        self._testEqual(center, answers)

class Test_RWG2(_TestBase):
    def testCenter9subs(self):
        answers = {}
        answers[0] = [(-7, -1), (-4,-4), (-1, -7), (-2, -5), (-1, -4), (-5, -2), (-4, -1), (-2, -2), (-1, -1)]
        answers[1] = [(-2, -8), (-5,-5), (-8, -2), (-7, -4), (-8, -5), (-4, -7), (-5, -8), (-7, -7), (-8, -8)]
        answers[2] = [( 1, -7), ( 4,-4), ( 7, -1), ( 5, -2), ( 4, -1), ( 2, -5), ( 1, -4), ( 2, -2), ( 1, -1)]
        answers[3] = [( 8, -2), ( 5,-5), ( 2, -8), ( 4, -7), ( 5, -8), ( 7, -4), ( 8, -5), ( 7, -7), ( 8, -8)]
        answers[4] = [(-1*each[0], -1*each[1]) for each in answers[2]]
        answers[5] = [(-1*each[0], -1*each[1]) for each in answers[3]]
        answers[6] = [(-1*each[0], -1*each[1]) for each in answers[0]]
        answers[7] = [(-1*each[0], -1*each[1]) for each in answers[1]]
        self._testEqual([(each[0], each[1]) for each in center_[0]], answers[0])
        self._testEqual([(each[0], each[1]) for each in center_[1]], answers[1])
        self._testEqual([(each[0], each[1]) for each in center_[2]], answers[2])
        self._testEqual([(each[0], each[1]) for each in center_[3]], answers[3])
        self._testEqual([(each[0], each[1]) for each in center_[4]], answers[4])
        self._testEqual([(each[0], each[1]) for each in center_[5]], answers[5])
        self._testEqual([(each[0], each[1]) for each in center_[6]], answers[6])
        self._testEqual([(each[0], each[1]) for each in center_[7]], answers[7])

    def testRhoPlus(self):
        answers = [(-3.0, -3.0, 0.0), (6.0, -3.0, 0.0), (-3.0, 6.0, 0.0), (3.0, -3.0, 0.0), (3.0, 6.0, 0.0), (-3.0, 3.0, 0.0), (6.0, 3.0, 0.0), (3.0, 3.0, 0.0)]
        answers = [list(each) for each in answers]
        self._testEqual(rho_plus, answers)

    def testRhoMinus(self):
        answers = [(-3.0, -3.0, 0.0), (6.0, 3.0, 0.0), (3.0, 6.0, 0.0), (3.0, -3.0, 0.0), (-3.0, 6.0, 0.0), (-3.0, 3.0, 0.0), (6.0, -3.0, 0.0), (3.0, 3.0, 0.0)]
        answers = [list(each) for each in answers]        
        self._testEqual(rho_minus, answers)

class Test_RWG3(_TestBase):
    def testFactorA(self):
        answers = [1.998, 1.413, 1.413, 1.998, 1.413, 1.998, 1.413, 1.998]
        self._testCloseEnough(FactorA, answers)

    def testFactorFi(self):
        answers = [-18212.4j, -12873.6j, -12873.6j, -18207j, -12873.6j, -18207j, -12873.6j, -18207j]
        self._testCloseEnough(FactorFi, answers)
        
class TestImpMat(_TestBase):
    def testZmatrix(self):
        answers = [88730-25070j, -30950-6300j, -30953-6300j, 2939+1664j, -13944-7441j, 2939+1665j, -13944-7441j, -3868-2465j]
        self._testCloseEnough(Z[0], answers, tolerance = 620)
        
class Test_RWG4(_TestBase):
    def testV(self):
        answers = [-38.18, 54.0, 0.0, 38.18, 0.0, -38.18, 54.0, 38.18]
        self._testCloseEnough(Vx, answers, tolerance = 1)
        
    def testI(self):
        answers = [-2.72e-4-2.03e-5j, 2.81e-4+9.08e-6j, -1.84e-19+6.09e-20j, 2.72e-4 + 2.03e-5j, 1.54e-19-2.89e-20j, -2.72e-4-2.03e-5j, 2.81e-4+9.08e-6j, 2.72e-4+2.03e-5j]
        self._testCloseEnough(Ix, answers, tolerance = 5e-6)

class Test_RWG5(_TestBase):
    def testJ(self):
        answers = [3.18e-04, 1.82e-04, 3.18e-04, 1.82e-04, 3.18e-04, 1.82e-04, 3.18e-04, 1.82e-04]
        self._testCloseEnough([np.linalg.norm(each) for each in Jm], answers, tolerance = 2e-6)

if __name__ == '__main__':
    unittest.main()

