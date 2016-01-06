"""RWG algorithm, part3:
   Use the structure from rgw1 and rwg2 to create impedance matrix by impmat module

   Input:
   - structure object from mesh, and the info added to it from rwg1 and rwg2
   - material property: material object

   Output:
   - impedance matrix
"""

from math import pi as PI


def rwg3(structure, mat_prop):
    """
    Feed structure, generated from mesh class, into rwg algorithm, part3

    Arguments:
    frequency: a list, units in MHz.
    epsilon_r: relative er
    mu_r: relative ur
    """
    edge_length = structure.edge_length

    epsilon = mat_prop.epsilon
    mu = mat_prop.mu
    speed_of_light = mat_prop.speed_of_light
    ##vv----- Added from material._material object
    structure.speed_of_light = speed_of_light
    structure.eta = mat_prop.eta
    ##^^-----
    jk = 1.0j*2.0*PI/speed_of_light
    CONSTANT1 = mu/(4*PI)*1.0e6  #1e6 as a factor to denote MHz unit for frequency
    CONSTANT2 = 1.0/(8.0j*PI*PI*epsilon*1.0e6) ##1e6 functions the same factor for MHz
    FactorA = [ 0.5j*PI*CONSTANT1*each for each in edge_length]
    ## frequency-dependent is not added yet.
    FactorFi = [ CONSTANT2*each for each in edge_length]
    for each in ['FactorA', 'FactorFi', 'speed_of_light']:
        setattr(structure, each, eval(each))
        


