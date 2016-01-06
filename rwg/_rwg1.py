""" RWG algorithm, part1:
    Creates the RWG edge element for every inner edge of the structure.

    Input:
    - The structuers of mesh.Mesh objects, e.g. mesh.Mesh.plate(2,2,20,20)

    Outputs:
    - edge_: nx2
      2-D list;
      n total edges; and the 2 nodes that connect every inner edge

    - triangle_plus:
      nx1 2-D list;
      n total triangles; and the no. of the triangle specified as 'plus'

    - triangle_minus:
      nx1 2-D list;
      n total triangles; and the no. of the triangle specified as 'minus'

    - edge_length:
      nx1 2-D list;
      n total edges; and the total inner edges

    - edges_total:
      number of total edges

    - area:
      nx1 2-D list;
      n total triangles; the area for each triangle

    - center:
      nx3 2-D tuple; then turned into matrix element
      n total triangles; ant the 3D coordinate for each triangle

    - edge_indicator: ***has not yet been implemented
"""
##---import basic vector calculation module
from .vector import Vector

##---function to calculate triangle area for three given coordinates
def tri_area_and_center(coor1, coor2, coor3):
    coor13 = coor1 - coor3
    coor23 = coor2 - coor3
    return coor13.area(coor23), coor1.center(coor2, coor3)

##---function to decide if two triangles adjacent by sharing 2 nodes out of 3
def if_adjacent(tri1, tri2):
    connectivity = [0, 0, 0]
    for k, each1 in enumerate(tri1):
        for each2 in tri2:
            if each1 == each2:
                connectivity[k] = 1
    return connectivity ## returned connectivity based on triangle 1

##---onset of rwg1 main algorithm
##---input structure: the object from mesh
#from mesh import Mesh
#structure = Mesh('plate',2,2,2,2)
def rwg1(structure):
    """ rwg1 function """
    p = structure.points
    t = structure.triangles
    ## convert p array from 2D to 3D by adding z=0
    temp = []
    if len(p[0]) == 2:
        for k, each in enumerate(p):
            temp.append(Vector(p[k][0], p[k][1], 0.0))
    elif len(p[0]) == 3:
        for each in p:
            temp.append(Vector(p))
    p = temp
    triangles_total = len(t)
    ## Find areas of separate triangles
    for v in range(triangles_total):
        temp = tri_area_and_center(p[t[v][0]], p[t[v][1]], p[t[v][2]])
        structure.area.append(temp[0] / 2.0)
        structure.center.append(temp[1],)
    ## Find all edge elements "Edge_" with two adjacent triangles
    edge_ = []
    triangle_plus = []
    triangle_minus = []

    for i in range(triangles_total):
        n_tri = t[i]
        for j in range(i + 1, triangles_total):
            m_tri = t[j]
            temp_array = ()
            ## 'temp' is the array to show if any two triangles share the same edge.
            connectivity = if_adjacent(n_tri, m_tri)
            if sum(connectivity) == 2:
                for k, each in enumerate(connectivity):
                    if each == True:
                        temp_array = temp_array+(n_tri[k], )
                triangle_minus.append(j)
                triangle_plus.append(i)
                edge_.append(temp_array)

    ## associate the ouput results to the input object 'structure'
    structure.triangles_total = triangles_total
    structure.points = p
    structure.edge_ = edge_
    structure.triangle_plus = triangle_plus
    structure.triangle_minus = triangle_minus
    structure.edges_total = len(edge_)
    for each in edge_:
        coor1 = p[each[0]]
        coor2 = p[each[1]]
        structure.edge_length.append((coor1-coor2).mag)
