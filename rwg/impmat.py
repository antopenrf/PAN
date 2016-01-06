from math import exp
from math import sin
from math import cos
from math import pi as PI

from .matrix import Matrix
from .matrix import zeros
from .matrix import fill

import numpy as np

class Element(object):

    def __init__(self):
        self._type = "Zelement"
        self._set = {}

    def add(self, index, node):
        self.index = index
        self.node = node
        self._set[self.index] = self.node

    def __call__(self, *indices):
        index = indices[0], indices[1]
        return self._set[index]


def impmat(structure, freq):
    """Function to generate Z matrix per the given structure and freq (MHz)."""
    center = Matrix(structure.center)
    center_ = Matrix(structure.center_)
    edge_length = structure.edge_length

    edges_total = structure.edges_total
    triangles_total = structure.triangles_total
    speed_of_light = structure.speed_of_light

    wn = 2*PI*freq/speed_of_light
    Z_matrix = np.zeros(shape = (edges_total, edges_total), dtype = np.complex_)


    for tri in range(triangles_total):
        ## find the edge no for each tri, and group into plus or minus
        plus = []
        minus = []
        count = 0
        for index in range(edges_total):
            if count <= 3:
                if structure.triangle_plus[index] == tri:
                    plus.append(index)
                    count += 1
                elif structure.triangle_minus[index] == tri:
                    minus.append(index)
                    count += 1

        G = center_ - fill(center(tri), triangles_total, 9)   ## dim = no of ttl triangles x 9 sub's
        abs(G)
        fphase = lambda R: (cos(wn*R) - 1j*sin(wn*R))/R
        G.element_wise(fphase)
        ZF=[]
        for k in range(edges_total):
            Fi = sum(G.row(structure.triangle_plus[k])) - sum(G.row(structure.triangle_minus[k]))
            ZF.append(structure.FactorFi[k] / freq * Fi / 9)

        Z = None
        Zi = None
        ### --- loop thru each source edge (S); for each edge, fill in the entire column
        for n in plus + minus:
            if n in plus:
                source = structure.rho__plus
                func = lambda x, y: x+y
            else:
                source = structure.rho__minus
                func = lambda x, y: x-y
            src = source[n]
            rho_p = [[each.dot(structure.rho_plus[row]) for each in src] for row in range(edges_total)]
            rho_m = [[each.dot(structure.rho_minus[row])for each in src] for row in range(edges_total)]
            # dim of rho_p and rho_m: no of triangles x 9 sub's

            area = []
            ### --- loop through each obverver edge (O)
            for m in range(edges_total):
                g_p = G.row(structure.triangle_plus[m])
                g_m = G.row(structure.triangle_minus[m])
                r_p = rho_p[m]
                r_m = rho_m[m]
                area_p = sum([each*g_p[index] for index, each in enumerate(r_p)])
                area_m = sum([each*g_m[index] for index, each in enumerate(r_m)])
                area.append(area_p + area_m)
            Z1 = [ each*area[index]*freq/9.0 for index, each in enumerate(structure.FactorA)]
            edge = edge_length[n]
            Zi = [ each*edge for each in map(func, Z1, ZF)]
            Z_matrix[:,n] += Zi

    return Z_matrix
