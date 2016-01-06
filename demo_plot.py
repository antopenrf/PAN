
import mesh
import rwg
from plotter import *
import cPickle as pickle

number = raw_input("\nSelect mesh to plot: (1)dipole (2)dual stubs (3)patch\n")
if number not in ('1', '2', '3'):
    print("Input invalid!")
else:
    if number == '1':
        mesh_to_plot = 'dipole'
    elif number == '2':
        mesh_to_plot = 'dual_stub'
    elif number == '3':
        mesh_to_plot = 'patch'
    else:
        pass
    
    print("Plot mesh, boundary and currents for " + mesh_to_plot + ".\n")
    print(mesh_to_plot)
    with open("./results/" + mesh_to_plot + "_strct.pkl", 'r') as file_strct:
        structure = pickle.load(file_strct)
        structure.center = None
        plotAll(structure, structure.densities)

    
    with open("./results/" + mesh_to_plot + "_pattern.pkl", 'r') as file_pattern:
        p = pickle.load(file_pattern)
        g1 = GraphPattern2D()
        g1.plot2Dcut(p.angles(), p.xy, rmax = p.directivity_dB, rmin = -20, filename = structure.name + '_xy.png')
        g2 = GraphPattern2D()
        g2.plot2Dcut(p.angles(), p.yz, rmax = p.directivity_dB, rmin = -20, filename = structure.name + '_yz.png')
        g3 = GraphPattern2D()
        g3.plot2Dcut(p.angles(), p.zx, rmax = p.directivity_dB, rmin = -20, filename = structure.name + '_zx.png')






                                                                                      
