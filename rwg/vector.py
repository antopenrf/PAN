## simple function library for vector calculation
## All the vectors are in tuple type.

class Vector(list):
    """Basic Vector class
    Arguments:
    - Either given as a tuple,
    - Or given as a sequence of numbers

    Returned:
    - in a form of tuple

    Methods:
    v1 = Vector(given tuple 1)
    v2 = Vector(given tuple 2)
    - __add__(self, other): v1 + v2
    - __sub__(self, other): v1 - v2
    - __mul__(self, scalar): c*v1
    - cross(self, scalar):  v1 X v2
    - mag(@property): |v1|
    """

    def __init__(self, *argv):
        answer = []
        arg_type = type(argv[0])
        if (arg_type == tuple or arg_type == list) and len(argv) == 1:
            argv = argv[0]
        for each in argv:
            answer = answer + [each,]
        list.__init__(self, answer)

    def str__(self):
        answer = "("
        for k, each in enumerate(self):
            if each == 0.0:
                formatted = "0"
            elif abs(each)>100 or abs(each)<0.0001:
                if type(each) == float:
                    formatted = "%.2e"%each
                elif type(each) == complex:
                    formatted = "%.2e + %.2ei"%(each.real, each.imag)
            elif type(each) == int:
                formatted = str(each)
            else:
                if type(each) == float:
                    formatted = "%.2f"%each
                elif type(each) == complex:
                    formatted = "%.2f + %.2fi"%(each.real, each.imag)                    
            answer = answer + formatted
            if k != len(self) - 1:
                answer += ', '
        answer += ")"
        return answer

    def __add__(self, other):
        answer=[]
        for k,each in enumerate(other):
            answer = answer + [self[k] + each, ]
        return self.__class__(answer)

    def __sub__(self, other):
        answer=[]
        for k,each in enumerate(other):
            answer = answer + [self[k] - each, ]
        return self.__class__(answer)

    def __mul__(self, scalar):
        answer=[]
        for k,each in enumerate(self):
            answer = answer + [scalar*self[k], ]
        return self.__class__(answer)

    def dot(self, other):
        answer = 0
        for k,each in enumerate(self):
            answer += self[k]*other[k]
        return answer


    def cross(self, other):
        """For 3-dim only"""
        x=self[1]*other[2]-self[2]*other[1]
        y=self[2]*other[0]-self[0]*other[2]
        z=self[0]*other[1]-self[1]*other[0]
        return self.__class__(x,y,z)


    def real_parts(self):
        return self.__class__(self[0].real, self[1].real, self[2].real)

        
    def prime(self):
        x, y, z = self[0].conjugate(), self[1].conjugate(), self[2].conjugate()
        return self.__class__(x, y, z)

                
    @property
    def mag(self):
        summation = 0
        for each in self:
            summation = summation + each*each
        return summation**0.5

    def __abs__(self):
        return self.mag

    def area(self, other):
        return self.cross(other).mag

    def append(self, element):
        answer=[]
        for each in self:
            answer = answer + (each,)
        answer = answer + (element,)
        return self.__class__(answer)

    def center(self, *veclist):
        summation = self
        for each in veclist:
            summation = summation.__add__(each)
        return summation*(1.0/len(veclist[0]))

if __name__ == "__main__":
    a = Vector(1,2,3)
    print a
    print a*3
    print a*(3+1j)
    
