import math
PI = math.pi
sin = math.sin
cos = math.cos

class Poly(object):

    def __init__(self, start = [0.0, 0.0]):
        self.nofs = 0      # number of sections
        self.start = start
        self.vertices = []
        self.vertices.append(start)
    
    def bbox(self):
        xmin, ymin, xmax, ymax = 0, 0, 0, 0
        for each in self.vertices:
            x = each[0]
            y = each[1]
            if x < xmin: xmin = x
            if x > xmax: xmax = x
            if y < ymin: ymin = y
            if y > ymax: ymax = y
        return [xmin, ymin, xmax, ymax]

    def add_points(self, x, y):
        self.nofs += 1
        self.vertices.append([x, y])

    def add_line(self, length = 1.0, tilt = 0.0):
        """Add a straight line with assigned length and tilt angle (in deg, starts from x-axis)."""
        self.nofs += 1
        start = self.vertices[-1]
        x = start[0] + float(length)*cos(tilt/180.0*PI)
        y = start[1] + float(length)*sin(tilt/180.0*PI)
        self.add_points(x, y)

    def add_line2(self, length = 1.0, tilt = 0.0, divisions = 10):
        step = float(length) / divisions
        for each in range(divisions):
            self.add_line(step, tilt)

    def add_arc2(self, end, span = 90.0, divisions = 10):
        """Add an arc by giving the coordinates of the start and end points."""
        start = self.vertices[-1]
        y_delta = float(end[1]) - start[1]
        x_delta = float(end[0]) - start[0]
        tilt = 180*math.atan(y_delta / x_delta)/PI
        if end[0] - start[0] < 0:
            tilt += 180.0
        line_len = ((end[0] - start[0])**2 + (end[1] - start[1])**2)**0.5
        radius = line_len / 2.0 / sin(span/180.0*PI/2.0)
        self.add_arc(radius, tilt, span)
        
    def add_arc(self, radius = 1.0, tilt = 0.0, span = 60.0, divisions = 10):
        """Add an arc by using partical circle of given radius, and span (deg), tilting from x (deg)."""
        self.nofs += 1
        start = self.vertices[-1]
        
        step = float(span)/divisions
        points_on_arc = []     # len is divisions + 1.

        for each in range(divisions + 1):
            angle = 90 - (tilt - span/2.0 + step*each)
            x = float(radius)*cos(angle/180.0*PI)
            y = float(radius)*sin(angle/180.0*PI)
            points_on_arc.append([x, y])

        displacement = [start[0] - points_on_arc[0][0], start[1] - points_on_arc[0][1]]
        f = lambda coor, dis: [coor[0] + dis[0], coor[1] + dis[1]]        
        self.vertices += [ f(each, displacement) for each in points_on_arc[1:]]
        
    def close_arc(self):
        self.add_arc2(self.vertices[0])
        self.close()
            
    def close(self, tolerance = 1e-3):
        last = self.vertices[-1]
        first = self.vertices[0]
        if abs(last[0] - first[0]) < tolerance and abs(last[1] - first[1]) < tolerance:
            self.vertices[-1] = self.vertices[0]
        else:
            self.vertices += [self.vertices[0], ]
        
if __name__ == '__main__':
    width = 1
    length = 1
    nx = 2
    ny = 2
    polygon = Poly([-width/2, -length/2])
    print(polygon.vertices)
    polygon.add_line2(length, 90, ny)
    polygon.add_line2(width, 0, nx)
    polygon.add_line2(length, -90, ny)
    polygon.close()
    print(polygon.vertices)
