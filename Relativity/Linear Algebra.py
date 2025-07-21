import numpy as np
from numpy.linalg import inv as mat_inv


mat = np.array([[1, 0, 0], [0, 2, 0], [0, 0, 19]])

vec1 = np.array([1, 2])
vec2 = np.array([2, 4])

# myVecTrans = mat @ vec1 #dot(vec1, vec2)

print(mat_inv(mat))
