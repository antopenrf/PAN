"""RWG algorithm, part4:

   Ref:   See Rao, Wilton, Glisson, IEEE Trans. Antennas and Propagation,
   vol. AP-30, No 3, pp. 409-418, 1982.
"""
import numpy as np
from math import pi as PI
from math import cos
from math import sin


## the onset of the rwg4
def rwg4(structure, freq, incidence, pol):
    Voltage  = np.zeros(shape = (structure.edges_total, 1), dtype = np.complex_)
    kvec = [ 2*PI*freq/structure.speed_of_light*each for each in incidence] #wave number vector

    for m in range(structure.edges_total):
        tri_plus = structure.triangle_plus[m]
        tri_minus  = structure.triangle_minus[m]
        phase_p = structure.center[tri_plus].dot(kvec)
        phase_m = structure.center[tri_minus].dot(kvec)
        Exp_p = cos(phase_p) - 1.0j*sin(phase_p)
        Exp_m = cos(phase_m) - 1.0j*sin(phase_m)
        EM_p = [each*Exp_p for each in pol]
        EM_m = [each*Exp_m for each in pol]
        ER_p = structure.rho_plus[m].dot(EM_p)
        ER_m = structure.rho_minus[m].dot(EM_m)
        Voltage[m][0] = structure.edge_length[m]*(ER_p/2.0 + ER_m/2.0)

    return Voltage
