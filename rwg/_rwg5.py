"""RWG algorithm, part5:

   Ref:   See Rao, Wilton, Glisson, IEEE Trans. Antennas and Propagation,
   vol. AP-30, No 3, pp. 409-418, 1982.
"""

from numpy import zeros
from numpy import complex_
from numpy import array


## the onset of the rwg5
def rwg5(structure, In):
    tri_plus = structure.triangle_plus
    tri_minus  = structure.triangle_minus
    rho_plus = structure.rho_plus
    rho_minus = structure.rho_minus
    edge_length = structure.edge_length
    area = structure.area

    Jm = []
    for tri in range(structure.triangles_total):
        count = 0
        Current_Density  = zeros((3,), dtype = complex_)

        for m in range(structure.edges_total):
            if count <= 3:
                if tri_plus[m] == tri:
                    scalar = In[m]*edge_length[m]/2.0/area[tri]
                    Current_Density += scalar*array(rho_plus[m])
                    count += 1

                elif tri_minus[m] == tri:
                    scalar = In[m]*edge_length[m]/2.0/area[tri]
                    Current_Density += scalar*array(rho_minus[m])
                    count += 1
                    
        Jm.append(Current_Density.tolist())

    return Jm 
