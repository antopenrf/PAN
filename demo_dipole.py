import cPickle as pickle
import current
import field
import material
import mesh
import pattern
import rwg
import numpy as np
from plotter import *

freq = 75.0

structure=mesh.Mesh('dipole', 'plate', 0.05, 2, 1, 10)

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
Vx = rwg.rwg4(structure, freq, incidence=rwg.negEz, pol=rwg.posEy)

Ix = np.linalg.solve(Z, Vx)

print('\nrwg5')
Jm = rwg.rwg5(structure, Ix)

densities = []
for each in Jm:
    densities.append( (abs(each[0])**2 + abs(each[1])**2)**0.5 )
structure.densities = densities

Isource = current.Current(freq)
Isource.Im = [complex(each[0]) for each in np.linalg.solve(Z, Vx)]

print('\nField and Measure Pattern.')
a = field.Field(structure, Isource)
p = pattern.Pattern(a, step = 5)
p.xy, p.yz, p.zx = p.cut2D()

with open("./results/dipole_strct.pkl", 'w') as file_strct:
    pickle.dump(structure, file_strct)

with open("./results/dipole_pattern.pkl", 'w') as file_strct:
    pickle.dump(p, file_strct)


