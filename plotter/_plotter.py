from platform import system as os_type
import os
import matplotlib.pylab as plt

class Graph(object):
    def __init__(self):
        self.fig = plt.figure()

    def _options(self, filepath, filename, shown):
        plt.savefig(filepath + filename)
        if shown: self._ifshown(filepath, filename)

    def _ifshown(self, filepath, filename):
        if os_type().lower() == "cygwin":
            command = "cygstart"
        elif os_type().lower() == "linux":
            command = "eog"
        else:
            command = "open"
        os.system(command + " " + filepath + filename + " &")


class GraphPattern2D(Graph):
    def __init__(self):
        super(GraphPattern2D, self).__init__()
        self.ax = self.fig.add_subplot(1,1,1, projection = 'polar')

    def plot2Dcut(self, angles, pattern, filename = "2Dcut.png", filepath = "./results/", shown = True, rmax = 5, rmin = -20, step = 5):
        self.ax.plot(angles, pattern, color='r', linewidth=3)
#        self.ax.set_rmax(rmax+2)
#        self.ax.set_rmin(rmin)
        self.ax.set_yticks([rmin + step*each for each in range(int((rmax-rmin)/5)+2)])
        self.ax.grid(True)
        self._options(filepath, filename, shown)        
        
        

class GraphStruct(Graph):

    def __init__(self):
        super(GraphStruct, self).__init__()
        self.ax = self.fig.add_subplot(1,1,1)
        self.ax.set_aspect('equal')
        
    def plotDensity(self, points, triangles, densities, filename = "density.png", filepath = "./results/", xlabel = 'x', ylabel = 'y', shown = True):
        x = [each[0] for each in points]
        y = [each[1] for each in points]
        self.ax.set_title("current density", loc='center')        
        colors = self.ax.tripcolor(x, y, triangles, densities)
        self.fig.colorbar(colors)
        self._options(filepath, filename, shown)
        
    def plotPoly(self, points, filename = "poly.png", filepath = "./results/", xlabel = 'x', ylabel = 'y', shown = True):
        x = [each[0] for each in points]
        y = [each[1] for each in points]
        self.ax.set_title("poly", loc='center')        
        self.ax.plot(x, y)
        self._options(filepath, filename, shown)

    def plot2Dmesh(self, points, triangles, centers = None, filename =  "mesh.png", filepath = "./results/", keepout_ratio = 1.02, xlabel = 'x', ylabel = 'y', shown = True):
        ## -- Prepare data and plot
        x = [each[0] for each in points]
        y = [each[1] for each in points]        
        self.ax.triplot(x, y, triangles, 'g.-')
        ## -- Set specific plotting parameters.
        self.ax.set_title("mesh", loc='center')
        self._set_label(xlabel, ylabel)
        if centers != None:
            self._annotate_tri_number(centers)
        ## -- Call common plotting parameters.
        self._options(filepath, filename, shown)


    def _set_label(self, xlabel, ylabel):
        self.ax.set_xlabel(xlabel)
        self.ax.set_ylabel(ylabel)
        
    def _annotate_tri_number(self, centers): 
        for k, each in enumerate(centers):
            self.ax.text(each[0], each[1], str(k), fontsize = 8)
       
    
def plotAll(structure, densities):
    name = structure.name
    v = structure.vertices
    p = structure.points
    t = structure.triangles
    c = structure.center

    polygon = GraphStruct()
    polygon.plotPoly(v, filename = name + "_" + "poly.png" )
    
    mesh = GraphStruct()
    mesh.plot2Dmesh(p, t, c, filename = name + "_" + "mesh.png" )

    density = GraphStruct()
    density.plotDensity(p, t, densities, filename = name + "_" + "densities.png" )
    
    
