import numpy as np

class CellResultsData:
    def __init__(self, n_pvs):
        self.result_matrix_cell = np.zeros((3, n_pvs))
        self.predict_tem_result_cell = np.zeros((n_pvs, 2))
