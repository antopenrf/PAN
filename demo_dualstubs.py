import cPickle as pickle
import current
import field
import material
import mesh
import pattern
import rwg
import numpy as np
from plotter import *


d = 0.01
cord = 0.091
fan = mesh.Poly([-d, 0])
fan.add_line2(d, 90, 2)
fan.add_line2(cord, 135, 8)
fan.add_arc2(end = [cord/(2**0.5)+d, cord/(2**0.5)+d], span = 90, divisions = 10)
fan.add_line2(cord, -135, 8)
fan.add_line2(2*d, -90, 2)
fan.add_line2(cord, -45, 8)
fan.add_arc2(end = [-cord/(2**0.5)-d, -cord/(2**0.5)-d], span = 90, divisions = 10)
fan.add_line2(cord, 45, 8)
fan.close()
pv = fan.vertices


freq = 750.0 ##MHz
structure=mesh.Mesh('dual_stub', 'poly', pv, 0.01, fan.bbox())

print('\nrwg1')
rwg.rwg1(structure)

print('\nrwg2')
rwg.rwg2(structure)

print('\nrwg3')
mat_prop = material.Material(epsilon_r = 1, mu_r = 1)
rwg.rwg3(structure, mat_prop)

print('\nimpmat')
Z = rwg.impmat(structure, freq)

print('\nrwg4')
Vx = rwg.rwg4(structure, freq, incidence=rwg.negEz, pol=rwg.posEx)

Ix = np.linalg.solve(Z, Vx)

print('\nrwg5')
Jm = rwg.rwg5(structure, Ix)

densities = []
for each in Jm:
    densities.append( (abs(each[0])**2 + abs(each[1])**2)**0.5 )
structure.densities = densities

import cPickle as pickle
with open("./results/dual_stub_strct.pkl", 'w') as file_strct:
    pickle.dump(structure, file_strct)

Isource = current.Current(freq)
Isource.Im = [complex(each[0]) for each in np.linalg.solve(Z, Vx)]

print('\nField and Measure Pattern.')
a = field.Field(structure, Isource)
p = pattern.Pattern(a, step = 5)
p.xy, p.yz, p.zx = p.cut2D()

with open("./results/dual_stub_strct.pkl", 'w') as file_strct:
    pickle.dump(structure, file_strct)

with open("./results/dual_stub_pattern.pkl", 'w') as file_strct:
    pickle.dump(p, file_strct)

