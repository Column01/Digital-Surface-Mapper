import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate
import statistics

fig = plt.figure()
ax = plt.axes(projection='3d')

pnts = [
    (0, 0, -0.80095), (1, 0, -0.83550), (2, 0, -0.99760), (3, 0, -1.09061), (4, 0, -1.25006),
    (0, 1, -0.91256), (1, 1, -0.98166), (2, 1, -1.11719), (3, 1, -1.13845), (4, 1, -1.27929),
    (0, 2, -1.00823), (1, 2, -1.09859), (2, 2, -1.15971), (3, 2, -1.27132), (4, 2, -1.32447),
    (0, 3, -1.11187), (1, 3, -1.22880), (2, 3, -1.27398), (3, 3, -1.31650), (4, 3, -1.37230),
    (0, 4, -1.24209), (1, 4, -1.31650), (2, 4, -1.39091), (3, 4, -1.41482), (4, 4, -1.49455)
]

# pnts.sort()
print(pnts)

# x = [0, 1, 2, 3, 4]
# y = [0, 1, 2, 3, 4]
# z = [
#     [-0.80095, -0.91256, -1.00823, -1.11187, -1.24209],
#     [-0.83550, -0.98166, -1.09859, -1.22880, -1.31650],
#     [-0.99760, -1.11719, -1.15971, -1.27398, -1.39091],
#     [-1.09061, -1.13845, -1.27132, -1.31650, -1.41482],
#     [-1.25006, -1.27929, -1.32447, -1.37230, -1.49455]
# ]

# pnts.sort()
x = np.array([tup[0] * 50 for tup in pnts]).reshape(5, 5)
y = np.array([tup[1] * 50 for tup in pnts]).reshape(5, 5)
z = [tup[2] for tup in pnts]

# print(x)
# print(y)
# print(z)

med = statistics.median(z)
new_z = np.array([pnt - med for pnt in z]).reshape(5, 5)

f_interp = interpolate.interp2d(x, y, new_z, kind='cubic')
print(f'X:{7 * 50} Y:{6 * 50} Z:{f_interp(7 * 50, 6 * 50)[0]}')

ax.scatter(x, y, new_z, color='red')
ax.plot_wireframe(x, y, new_z, color='black')
ax.plot_surface(x, y, f_interp(x[0], y[..., 0]), cmap='hot', color='green')
ax.set_title("Bed Mesh")
plt.show()
