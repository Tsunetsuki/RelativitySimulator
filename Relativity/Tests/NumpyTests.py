from numpy import *

a = array([0, 0])
u = array([2, 22])
b = array([7, 2])
v = array([1, -1])




def intersecc(a, u, b, v):
    row1 = array([u[0], -v[0]])
    row2 = array([u[1], -v[1]])
    consts = array([-a[0] + b[0], -a[1] + b[1]])

    myMat = array([row1, row2])

    t1, t2 = linalg.solve(myMat, consts)
    
    return t1, t2

t1, t2 = intersecc(a, u, b, v)
print(str(t1) + " " + str(t2))
print(a + u * t1)
print(b + v * t2)
#print(intersecc(a, u, b, v))



#xa0 + xa * t = xb0 + xb * t
#ya0 + ya * t = yb0 + yb * t

#(xa - xb) + (ya - yb) * t = (xb0 - xa0) + (yb0 - ya0)

#for coord in [0, 1]:
#    print(diff(sign(line2[:, coord] - line1[:, coord])))
#
#a = array([0, 1, 2, 3, 3, 3.5, 3, 9])
#print()