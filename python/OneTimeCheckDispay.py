# Run in physics03 with conda environment ap-2021-2.2
# e.g.
# ssh physics03
# conda activate ap-2021-2.2


# The display of historical data

class OutputForOneTimeCheck:

    def __init__(self):
        self.rate = []
        self.slope = []
        self.predict_temp = []
        self.predict_time = []

    def display_slope_predict(self, cell_results_data, cell_pre_data):
        # with open('C01_Data_Accumulated_Linear_Model_Parameters.csv', newline='') as csvfile:
        #  self.slope = csvfile[1, :]
        self.rate = cell_results_data[1, :]
        self.slope = cell_results_data[0, :] * cell_results_data[1, :]
        self.predict_temp = cell_pre_data[:, 0]
        self.predict_time = cell_pre_data[:, 1]
