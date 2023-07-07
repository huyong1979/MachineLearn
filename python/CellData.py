import numpy as np

class CellVariableData:
    def __init__(self, num_data_per_test, n_pvs):
        self.num_data = num_data_per_test
        self.data_matrix_pv = np.zeros((n_pvs, 3, self.num_data))
        self.n_pvs = n_pvs  
