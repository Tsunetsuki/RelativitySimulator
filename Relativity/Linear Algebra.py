import numpy as np
from numpy import *
from numpy.linalg import inv as mat_inv




mat = array([
    [1, 0, 0],
    [0, 2, 0],
    [0, 0, 19]
])

vec1 = array([1, 2])
vec2 = array([2, 4])

#myVecTrans = mat @ vec1 #dot(vec1, vec2)

print(mat_inv(mat))
