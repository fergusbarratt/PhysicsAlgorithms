import numpy as np
import matplotlib.pyplot as plt
from numpy.linalg import eigvalsh


class RandomMatrixEnsemble():
    def __init__(self, mat_size, N_mats, mat_type='GOE'):
        self.mat_size = mat_size
        self.N_mats = N_mats
        if mat_type=='GOE':
            self.data = [self.gen_GOE_mems(mat_size) for _ in range(N_mats)]
        else:
            self.data = []
            print('empty ensemble')

    def gen_GOE_mems(self, N):
        A = np.random.normal(size=[N, N])
        return A+A.T

    def eigs(self, sort=True):
        if sort:
            return np.asarray([sorted(eigvalsh(datum)) for datum in self.data])

    def splittings(self):
        un_normalised = np.asarray([eigs[(len(eigs)//2)]-eigs[(len(eigs)//2)-1] for eigs in self.eigs()])
        mean = np.mean(un_normalised)
        return un_normalised/mean
    def test(self):
        ''' test symmetric, right size, right shape, right no. of eigs, right no. of eig-lists, right no. of mats'''
        for mat in self.data:
            assert not (mat - mat.T).any()
            assert not (np.asarray(mat.shape) - np.asarray(
                [self.mat_size, self.mat_size])).any()
        assert len(self.data) == self.N_mats
        assert len(self.eigs()) == self.N_mats
        assert len(self.eigs()[0]) == self.mat_size
        assert len(self.splittings()) == self.N_mats

ens = RandomMatrixEnsemble(2, 10000)
ens.test()
splits = ens.splittings()
binwidth = 0.1
plt.hist(splits, bins=np.arange(min(splits), max(splits)+binwidth, binwidth))
plt.xlabel('splitting')
plt.ylabel('magnitude')
plt.show()
