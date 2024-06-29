from math import sin, cos, atan2

class Vec2D(tuple):
    def get_additive_identity():
        return Vec2D((0, 0))
    
    def __neg__(self):
        return Vec2D((-self[0], -self[1]))
    
    def __add__(self, other):
        return Vec2D((self[0] + other[0], self[1] + other[1]))
    
    def __radd__(self, other):
        return self + other
    
    def __sub__(self, other):
        return self + (-other)
    
    def __mul__(self, scalar):
        return Vec2D((self[0] * scalar, self[1] * scalar))
    
    def __rmul__(self, scalar):
        return self * scalar 
    
    def __truediv__(self, scalar):
        return 1/scalar * self
    
    def __floordiv__(self, scalar):
        return Vec2D((self[0] // scalar, self[1] // scalar))
    
    def round(self):
        return Vec2D((round(self[0]), round(self[1])))
    
    def __xor__(self, other):
        return abs(self - other)
    
    def rot90(self):
        return Vec2D((self[1], -self[0]))
    
    def invRot90(self):
        return Vec2D((-self[1], self[0]))
    
    def dot(self, other):
        return self[0]*other[0] + self[1]*other[1]
    
    def norm_squared(self):
        return self.dot(self)
        
    def __abs__(self):
        return (self.norm_squared())**0.5
    
    def normalise(self):
        return self/abs(self)
    
    def project(self, other):
        return self.dot(other.normalise())
    
    def zero():
        return Vec2D((0,0))
    
    def make_from_arg_mag(arg, mag):
        return Vec2D((cos(arg),sin(arg)))*mag
    
    def angle(self):
        return atan2(self[1], self[0])
    
    def rotate(self, angle):
        return Vec2D.make_from_arg_mag(self.angle()+angle, abs(self))