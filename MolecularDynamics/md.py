import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from numpy.random import rand
import matplotlib.colors as colors


class VectorTools(object):

    def _distance(self, vec_1, vec_2):
        return np.sum([(x - y)**2 for x, y in zip(vec_1, vec_2)])

    def _index_matrix_like(self, A, re_spacing=1):
        A = np.asarray(A)
        ind_mat = np.zeros_like(A)
        for row_ind, col in enumerate(ind_mat):
            for col_ind, elem in enumerate(col):
                ind_mat[row_ind, col_ind] = np.asarray([row_ind, col_ind])
        return ind_mat * re_spacing

    def _flip_second(dims):
        dims[1] = -dims[1]
        return dims

    def _flip_first(dims):
        dims[0] = -dims[0]
        return dims


class Solid(VectorTools):

    def __init__(
                self,
                initial_displacements,
                initial_velocities,
                masses,
                lennard_jones_params,
                friction_coefficients=None,
                lattice_spacing=0.2):
        '''initial_displacements is nxn matrix of tuples, and
        initial_velocities are nxn matrices for nxn solids'''
        if not friction_coefficients:
            self.friction_coefficients = np.zeros_like(initial_displacements)
        self.initial_positions = np.add(self._index_matrix_like(
            initial_displacements, lattice_spacing), initial_displacements)
        self.initial_velocities = np.asarray(initial_velocities)
        self.masses = np.asarray(masses)
        self.non_bonding_potential = self._non_bonding(lennard_jones_params)
        self.position_data = [self.initial_positions[i, j]
                              for i, j in np.ndindex(
                                self.initial_positions.shape[:2])]

    def _lennard_jones(self, diameter, well_depth):
        def potential(r):

            return 4 * well_depth * ((diameter / r)**12 - (diameter / r)**6)
        return potential

    def _non_bonding(self, lennard_jones_params):
        def potential(x, y):
            r = np.asarray([x, y])
            return np.sum([self._lennard_jones(*lennard_jones_params)(
                self._distance(r, r1)) for r1 in self.position_data
                    if (self._distance(r, r1)) != 0])
        return potential

# rand is called only once a row

dims = [2, 2]
initial_displacements = rand(*dims, 2)
initial_velocities = [0, 0, 0]
masses = [1, 1, 1]
lennard_jones_params = (1, 1)
flipFirst = VectorTools._flip_first
testSolid = Solid(initial_displacements, initial_velocities,
                  masses, lennard_jones_params, lattice_spacing=0.1)

xs = [testSolid.initial_positions[i, j][0]
      for i, j in np.ndindex(testSolid.initial_positions.shape[:2])]
ys = [testSolid.initial_positions[i, j][1]
      for i, j in np.ndindex(testSolid.initial_positions.shape[:2])]
sizes = [1000 for _ in range(len(initial_displacements))]


print([2*dim for dim in flipFirst(dims)])
X, Y = np.meshgrid(
                   np.linspace(*[2*dim for dim in flipFirst(dims)], 150),
                   np.linspace(*[2*dim for dim in flipFirst(dims)], 150))
vfunc = np.vectorize(testSolid.non_bonding_potential)
Z = vfunc(X, Y)
fig, ax = plt.subplots()
# plt.scatter(xs, ys, s=sizes)
pcm = ax.contourf(Z, cmap="seismic")
plt.colorbar(pcm)
plt.show()
