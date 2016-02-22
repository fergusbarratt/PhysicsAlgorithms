import numpy as np
import matplotlib.pyplot as plt
import qutip as qt
import seaborn as sns
sns.set()

class spinchain(object):
    def __init__(self, J, L, spin_levels):
        def tens_op(op, i):
            return qt.tensor(*[qt.identity(spin_levels) for _ in range(i-1)], op, *[qt.identity(spin_levels) for _ in range(L-1-i)])
        self.hamiltonian = J/2*np.sum([qt.tensor(tens_op(qt.sigmap(), i), tens_op(qt.sigmam(), i+1)) + qt.tensor(tens_op(qt.sigmam(), i), tens_op(qt.sigmap(), i+1)) for i in range(L-1)])
    def dmrg(self):
       pass

q = spinchain(2, 10, 2)
print(q.hamiltonian)
