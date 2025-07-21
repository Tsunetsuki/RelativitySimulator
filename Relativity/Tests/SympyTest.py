import sympy as sp
import numpy as np
import time
from sympy import Matrix, solve, symbols

x, y, z, t = symbols("x y z t")
t1, t2 = symbols("t1 t2")
k, m, n = symbols("k m n", integer=True)
# f, g, h = symbols('f g h', cls=Function)
sp.init_printing()

a = np.array([0, 0])
u = np.array([2, 22])
b = np.array([7, 2])
v = np.array([1, -1])

a = Matrix([0, 0])
u = Matrix([2, 22])
b = Matrix([7, 2])
v = Matrix([1, -1])

myEquation1 = sp.Eq(a[0] + u[0] * t1, b[0] + v[0] * t2)
myEquation2 = sp.Eq(a[1] + u[1] * t1, b[1] + v[1] * t2)


myEquationV = sp.Eq(a + u * t1, b + v * t2)

# print(myEquationV)
# myEquation3 = sp.Eq(t * 5, t + 3)
# print(sp.solveset(myEquation3))

now = time.time()
eqs = 100
for _ in range(0, eqs):
    sol_t1 = sp.solve(myEquationV)
    print(sol_t1.get(t1))

print(eqs / (time.time() - now))
