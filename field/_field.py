from math import pi as PI
from math import exp
from math import cos
from math import sin
import numpy as np

from current import *
from material import *
from mesh import *
from rwg import *


def point(Ro, K, eta, dplctr, dplmmt):
    """Calculate field at a point.  Inputs are Ro(obervation coordinate), K(wave number), dplctr(dipole Center, dplmmt(dipole moment)."""
    r = []
    PointRM = []
    EXP = []
    PointRM2 = []
    C = []
    D = []
    M = []
    ConstantH = 1.0j*K/4.0/PI
    ConstantE = eta/4.0/PI
    HFieldi = []
    EFieldi = []
    HField = Vector(0.0j, 0.0j, 0.0j)
    EField = Vector(0.0j, 0.0j, 0.0j)
    fphase = lambda R, wn: (cos(wn*R) - 1j*sin(wn*R))    
    for index in range(len(dplctr)):
        RoC = Ro - dplctr[index]  #RoC: Ro to Center
        RoC_mag = RoC.mag
        r.append(RoC)
        PointRM.append(RoC_mag)
        RoC_mag2 = RoC_mag**2
        PointRM2.append(RoC_mag**2)
        EXP.append(fphase(RoC_mag, K))
        C.append(1/RoC_mag2*(1.0 - 1.0j/K/RoC_mag))
        Mi = RoC.dot(dplmmt[index])/RoC_mag2
        M.append(RoC*Mi)
        H = (dplmmt[index].cross(RoC))*ConstantH*C[-1]*EXP[-1]
        HFieldi.append(H)
        E = ((M[-1] - dplmmt[index])*(1j*K/PointRM[-1]+C[-1]) + M[-1]*2*C[-1])*ConstantE*EXP[-1]
        EFieldi.append(E)

    for index in range(len(HFieldi)):
        EField = EField + EFieldi[index]
        HField = HField + HFieldi[index]
    return EField, HField


class Field(object):
    """Class to produce farfield from the given structure (instanced from _mesh.Mesh class) and current density Im."""

    def __init__(self, strct, Isource):
        
        Im = Isource.Im
        centers = strct.center
        pts_plus = [centers[each] for each in strct.triangle_plus]
        pts_minus =[centers[each] for each in strct.triangle_minus]
        pts_mp = map(lambda x, y: y - x, pts_plus, pts_minus)
        
        ## dipole center and dipole momentq
        self.dplctr = map(lambda x, y: (x + y)*0.5, pts_plus, pts_minus)
        self.dplmmt = map(lambda I, edge, r: r*I*edge, Im, strct.edge_length, pts_mp)
        self.freq = Isource.freq
        self.K = 2*PI/strct.speed_of_light*self.freq
        self.eta = strct.eta
        self.observation = None
        self.EField = None
        self.HField = None
        self.PVector = None
 
        
    def radiate2(self, observation):
        """Radiate fields , E and H, are function of observation coordinate."""
        if observation.__class__.__name__ != 'Vector':
            raise TypeError
        else:
            ## Check if the observation is the same as previous, does not need to run the calculation again.
            if observation != self.observation:
                self.EField, self.HField = point(observation, self.K, self.eta, self.dplctr, self.dplmmt)
                self.observation = observation
                return self.EField, self.HField
            else:
                return self.EField, self.HField

    def Poynting(self, observation):
        self.radiate2(observation)
        E = self.EField
        H = self.HField
        E_x_H = E.cross(H.prime())
        self.PVector = E_x_H.real_parts()*0.5
        return self.PVector


if __name__ == "__main__":
    from plotter import *
    freq = 75.0 #MHz
    structure = Mesh('patch', 'plate', 0.05, 2, 1, 30)
    
    points = structure.points
    triangles = structure.triangles

    rwg1(structure)
    rwg2(structure)
    mat_prop = Material(epsilon_r = 1, mu_r = 1)

    rwg3(structure, mat_prop)
    Z = impmat(structure, freq)
    Vx = rwg4(structure, freq, incidence = [0,0,-1], pol=[0,1,0])
    
    Isource = Current(freq)
    
    Isource.Im = [complex(each[0]) for each in np.linalg.solve(Z, Vx)]

    a = Field(structure, Isource)
    R1 = Vector(5, 0, 0)
    R2 = Vector(0, 0, 5)


