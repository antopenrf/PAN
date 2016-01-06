from math import pi as PI
from math import log10
from math import cos
from math import sin
import numpy as np

from current import *
from exception import *
from field import *
from material import *
from mesh import *
from rwg import *

class Pattern(object):

    def __init__(self, field, step = 30, distance = 5):
        icheck_TypeError(field, 'Field', '_field.Field should be used!')
        self.field = field
        self._prepare(step, distance)
        self._measure()

    def _prepare(self, step, distance):
        while 90%step != 0:  ## Force the step size to be 90-degree dividable.
            step = int(step) + 1
        self.step = step
        self.distance = distance
        self.data_densities = {}
        self.TRP = 0.0
        self.max_density = 0.0
        self.iso_density = 0.0

    def angles(self, span = 360, unit = 'rad'):
        t = [each*self.step for each in range(span/self.step + 1)]
        if unit == 'rad':
            return [each/180.0*PI for each in t]
        else:
            return t

        
    def remeasure(self, step = 90, distance = 5):
        self._prepare(step, distance)
        self._measure()

    def _gain(self, data_type = 'dB'):
        self.data_gain = {}
        for theta in [self.step*each for each in range(int(180/self.step)+1)]:
            self.data_gain[theta] = []
            for each in self.data_densities[theta]:
                gain = each/self.iso_density
                if data_type == 'dB':
                    gain = 10*log10(gain)
                self.data_gain[theta].append(gain)
        
    def cut2D(self):
        thetas = [self.step*each for each in range(int(180/self.step)+1)]
        phis = thetas + [each + 180 for each in thetas[1:]]

        index_90 = int(90/self.step)
        index_180 = index_90*2
        index_270 = index_90*3
        xycut = self.data_gain[90] + [self.data_gain[90][0],]  ## Add data at 360 degree at the end to close the pattern.
        zxcut = [self.data_gain[each][0] for each in thetas]
        yzcut = [self.data_gain[each][index_90] for each in thetas]
        thetas.reverse()
        zxcut += [self.data_gain[each][index_180] for each in thetas[1:-1]]+[self.data_gain[0][0],]
        yzcut += [self.data_gain[each][index_270] for each in thetas[1:-1]]+[self.data_gain[0][index_90],]
        return xycut, yzcut, zxcut
            
    def _measure(self):
        nof_phi = 360/self.step
        nof_theta = 180/self.step
        step = self.step/180.0*PI
        half_step = step/2
        distance = self.distance
        sphere_convex = distance*distance*4*PI

        pre_partial_sphere = 0.0
        for theta_no in range(nof_theta+1):
            theta = self.step*theta_no
            self.data_densities[theta] = []
            if theta_no == nof_theta:
                partial_sphere = 2.0
            else:
                partial_sphere = 1-cos(half_step + step*theta_no) ## 360 degree is 4PI solid angle

            for phi_no in range(nof_phi):
                area = (partial_sphere - pre_partial_sphere) / nof_phi / 2 * sphere_convex

                phi = self.step*phi_no
                theta_rad = theta/180.0*PI
                phi_rad = phi/180.0*PI
                norm = Vector(sin(theta_rad)*cos(phi_rad), sin(theta_rad)*sin(phi_rad), cos(theta_rad))
                R = norm*distance
                density = self.field.Poynting(R)
                density = density.dot(norm)
                power = density*area
                self.data_densities[theta].append(density)
                self.TRP += power
                if self.max_density < density:
                    self.max_density = density

            pre_partial_sphere = partial_sphere
        
        self.iso_density = self.TRP/4/PI/distance/distance
        self.directivity = self.max_density/self.iso_density
        self.directivity_dB = 10*log10(self.directivity)
        self._gain()
        print "TRP = {0} Watt, D = {1}, {2} dB".format(self.TRP, self.directivity, self.directivity_dB)

if __name__ == "__main__":

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

    p = Pattern(a, step = 30)



    xy, yz, zx = p.cut2D()

    from plotter import *

    g1 = GraphPattern2D()
    g1.plot2Dcut(p.angles(), xy, rmax = p.directivity_dB, rmin = -20, filename = 'xy.png')
    g2 = GraphPattern2D()
    g2.plot2Dcut(p.angles(), yz, rmax = p.directivity_dB, rmin = -20, filename = 'yz.png')
    g3 = GraphPattern2D()
    g3.plot2Dcut(p.angles(), zx, rmax = p.directivity_dB, rmin = -20, filename = 'zx.png')

