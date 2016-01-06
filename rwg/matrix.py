## simple function library for vector calculation
## All the vectors are in tuple type.
from .vector import Vector

class Matrix(list):
    """Basic Matrix class

    Arguments:
    - for __new__ method, gives matrix of tuples

    Returned:
    - in a form of combined tuples

    Methods:
    m1 = Matrix(given tuples set1)
    m2 = Matrix(given tuples set2)
    - __add__(self, other): m1 + m2
    - __sub__(self, other): m1 - m2
    - __mul__(self, other): other*v1, other can be scaler of matrix
    """
    
    def __new__(cls, *argv):
        mat = []
        if len(argv)==1:
            argv = argv[0]
        for each in argv:
            if each[0].__class__.__name__ != 'Vector':
                mat.append(Vector(each))
            else:
                mat.append(each)
        return list.__new__(cls, mat)
    
    @property
    def dim_m(self):
        return len(self)

    @property
    def dim_n(self):
        return len(self[0])

    @property
    def dim(self):
        return len(self), len(self[0])

    def row(self, m):
        return (self[m])

    def column(self, n):
        return tuple([self[m][n] for m in range(self.dim_m)])

    def indices(self):
        for i in range(self.dim_m):
            for j in range(self.dim_n):
                yield i, j

        
    def __repr__(self):
        representation = "dim: %d x %d" % (len(self), len(self[0])) + "\n"
        for i in range(self.dim_m):
            row = str(i)+"-row:"
            for j in range(self.dim_n):
                element = self[i][j]
                if type(element) == float:
                    if float(element) == 0.0:
                        s = "0"
                    elif element > 100 or element < 0.01:
                        s = "%.2e"%element
                    else:
                        s = "%.2f"%element
                else:
                    s = str(self[i][j])
                row += "\t" + s
            representation += row + "\n"
        return representation
        
    def __call__(self, *argv):
        """Using __call__ to call out the value of the matrix element at (m, n)"""
        if type(argv[0]) in (list, tuple):
            argv = argv[0]
            return self[argv[0]][argv[1]]
        elif len(argv) == 2:
            return self[argv[0]][argv[1]]
        elif len(argv) == 1 and type(argv[0]) == int:
            return self[argv[0]]
        else:
            pass
            
    def element_wise(self, operator):
        for i in range(self.dim_m):
            for j in range(self.dim_n):
                self[i][j] = operator(self[i][j])

    def __operator__(self, other, operator):
        mat = []
        for i in range(self.dim_m):
            row = []
            for j in range(self.dim_n):
                row.append(operator(self[i][j], other[i][j]))
            mat.append(row)
        return self.__class__(mat)
    
    def __add__(self, other, operator = lambda x, y: x+y):
        return self.__operator__(other, operator)
        
    def __sub__(self, other, operator = lambda x, y: x-y):
        return self.__operator__(other, operator)

    def __mul__(self, other):
        """Multiplication operator for doing scalar multiplication or scalar scaling."""
        if type(other) in (float, int, complex):
            mul_func = lambda o, self_mat, i, j: self_mat[i][j]*o
        elif other.__class__.__name__ == "Matrix":
            mul_func = lambda o, self_mat, i, j: sum([self_mat[i][each]*o[each][j] for each in range(len(self_mat))])
            
        m = self.dim_m
        n = self.dim_n
        mat = ()
        for i in range(m):
            row = ()
            for j in range(n):
                temp = mul_func(other, self, i, j)
                row = row + (temp, )
            mat = mat + (row, )
        return self.__class__(mat)
    
    def __abs__(self):
        for i in range(self.dim_m):
            for j in range(self.dim_n):
                self[i][j] = abs(self[i][j])

    
def fill(value, m, n = None):
    if n == None: n = m
    row = [value for each in range(n)]
    return Matrix([row for each in range(m)])

def zeros(m, n = None):
    return fill(0.0, m, n)

def ones(m, n = None):
    return fill(1.0, m, n)

def identity(m):
    rows = []
    for each in range(m):
        row = [0.0 for x in range(m)]
        row[each] = 1.0
        rows.append(tuple(row))
    return Matrix(rows)
