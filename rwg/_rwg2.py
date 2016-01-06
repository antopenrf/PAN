"""RWG algorithm, part2:
   Creates the following parameters of the RWG edge elements.

   Input:
   - Uses the mesh file from RWG1, mesh1.mat as an input.

   Output:
   - rho_plus:
   nx3 list, each coordinate is a vector.
   Position vector from the free vertex of the "plus" triangle to its center

   - rho_minus:
   nx3 list, each coordinate is a vector.
   Position vector from the center of the "minus" triangle to its free vertex

   In addition to these parameters creates the following arrays for
   nine subtriangles (barycentric subdivision):

   - center_:
   nx9 tuples, each 9-element tuple has 9 coordinates, each of which is a vector.
   Then, later turned into n x 9 matrix, each element of which is a vector
   Midpoints of nine subtriangles

   - rho__plus:
   nx9x3 (note: double underscores), n triangles x 9 sub-triangles x 3D coordinate
   For each triangle, it is divided into 9 sub-triangles.
   Position vectors from the free vertex
   of the "plus" triangle to 9 subtriangle midpoints

   - rho__minus:nx9x3 (note: double underscores)
   Position vectors from 9 subtriangle
   midpoints to the free vertex of the "minus" triangle

   Ref:   See Rao, Wilton, Glisson, IEEE Trans. Antennas and Propagation,
   vol. AP-30, No 3, pp. 409-418, 1982.
"""

def find_free_nodes(tri_plus, tri_minus):
    for node_p in tri_plus:
        flag_non_free = 0
        for node_m in tri_minus:
            if node_p == node_m:
                flag_non_free = 1
            else:
                pass
        if flag_non_free == 0:
            free_node_p = node_p

    non_free_nodes = list(tri_plus)
    non_free_nodes.remove(free_node_p)
    tri_minus = list(tri_minus)
    for node_p in non_free_nodes:
        tri_minus.remove(node_p)
    free_node_m = tri_minus[0]
    return free_node_p, free_node_m


## the onset of the rwg2
def rwg2(structure):
    center = structure.center
    center_ = structure.center_
    center_delta = structure.center_delta
    t = structure.triangles
    p = structure.points
    for m in range(structure.triangles_total):
        M = structure.center[m]
        r1 = p[t[m][0]]
        r2 = p[t[m][1]]
        r3 = p[t[m][2]]
        r21 = r2 - r1
        r32 = r3 - r2
        r31 = r3 - r1
        c1 = r1 + r21*(1.0/3.0)
        c2 = r1 + r21*(2.0/3.0)
        c3 = r2 + r32*(1.0/3.0)
        c4 = r2 + r32*(2.0/3.0)
        c5 = r1 + r31*(1.0/3.0)
        c6 = r1 + r31*(2.0/3.0)
        a1 = ((c1 + c5) + r1)*(1.0/3.0)
        a2 = ((c1 + c2) + M)*(1.0/3.0)
        a3 = ((c2 + c3) + r2)*(1.0/3.0)
        a4 = ((c2 + c3) + M)*(1.0/3.0)
        a5 = ((c3 + c4) + M)*(1.0/3.0)
        a6 = ((c1 + c5) + M)*(1.0/3.0)
        a7 = ((c5 + c6) + M)*(1.0/3.0)
        a8 = ((c4 + c6) + M)*(1.0/3.0)
        a9 = ((c4 + c6) + r3)*(1.0/3.0)
        nine_centers = (a1, a2, a3, a4, a5, a6, a7, a8, a9)
        center_.append(nine_centers)
        center_delta.append([each - center[m] for each in nine_centers])


    for m in range(structure.edges_total):
        plus_no = structure.triangle_plus[m]
        minus_no = structure.triangle_minus[m]
        (p1, p2, p3) = t[plus_no][0], t[plus_no][1], t[plus_no][2]
        (n1, n2, n3) = t[minus_no][0], t[minus_no][1], t[minus_no][2]
        free_plus, free_minus = find_free_nodes((p1, p2, p3), (n1, n2, n3))
        structure.rho_plus.append(center[plus_no] - p[free_plus])
        structure.rho_minus.append(p[free_minus] - center[minus_no])
        structure.rho__plus.append(map(lambda x: x-p[free_plus], center_[plus_no]))
        structure.rho__minus.append(map(lambda x: p[free_minus] - x, center_[minus_no]))


