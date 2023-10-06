# Run in physics03 with conda environment ap-2021-2.2
# e.g.
# ssh physics03
# conda activate ap-2021-2.2

import numpy as np

# The display of results data for different learning & prediction methods, part of variables will be displayed on CSS
# t is time, T is temperature


class OutputForOneTimeCheck:

    def __init__(self):
        self.intercept = []             # Intercept: initial values T_{0} = beta_{0}
        self.slope = []                 # Temperature change per day (only for Method 1): beta_{1}
        self.rate = []                  # Linear parameter: beta_{1}
        self.rate_square = []           # Quadratic parameter: beta_{2}
        self.rate_exp = []              # Exponential parameter: beta_{1}
        self.ls_error = []              # Least-squares error: err_{ls}
        self.predict_temp_1 = []        # Predicted Temperature for given time period: T_1_{final}
        self.predict_temp_2 = []        # Predicted Temperature for given time period: T_2_{final}
        self.predict_temp_3 = []        # Predicted Temperature for given time period: T_3_{final}
        self.predict_temp_4 = []        # Predicted Temperature for given time period: T_4_{final}
        self.predict_time = []          # Safe time period for given temperature warning
        self.Delta_T = []               # Temperature change in Polynomial (total time):  Delta T
        self.Delta_T_exp = []           # Temperature change in EXP (total time): Delta T

    def display_learned_predict_linear_regression(self, cell_results_data, cell_pre_data, num_day):
        # with open('C01_Data_Accumulated_Linear_Model_Parameters.csv', newline='') as csvfile:
        #  self.slope = csvfile[1, :]
        self.intercept = cell_results_data[0, :]
        self.slope = cell_results_data[1, :]
        self.ls_error = cell_results_data[3, :]
        self.predict_temp_1 = cell_pre_data[:, 0]
        self.predict_temp_2 = cell_pre_data[:, 1]
        self.predict_temp_3 = cell_pre_data[:, 2]
        self.predict_temp_4 = cell_pre_data[:, 3]
        self.predict_time = cell_pre_data[:, 4]
        self.Delta_T = num_day * cell_results_data[1, :] + np.square(num_day) * cell_results_data[2, :]

    def display_learned_predict_quadratic_regression(self, cell_results_data, cell_pre_data, num_day):
        self.intercept = cell_results_data[0, :]
        self.rate = cell_results_data[1, :]
        self.rate_square = cell_results_data[2, :]
        self.ls_error = cell_results_data[3, :]
        self.predict_temp_1 = cell_pre_data[:, 0]
        self.predict_temp_2 = cell_pre_data[:, 1]
        self.predict_temp_3 = cell_pre_data[:, 2]
        self.predict_temp_4 = cell_pre_data[:, 3]
        self.predict_time = cell_pre_data[:, 4]
        self.Delta_T = num_day * cell_results_data[1, :] + np.square(num_day) * cell_results_data[2, :]

    def display_learned_predict_nonlinear_exponential_regression(self, cell_results_data, cell_pre_data, num_day):
        self.intercept = cell_results_data[0, :]
        self.rate_exp = cell_results_data[1, :]
        self.ls_error = cell_results_data[3, :]
        self.predict_temp_1 = cell_pre_data[:, 0]
        self.predict_temp_2 = cell_pre_data[:, 1]
        self.predict_temp_3 = cell_pre_data[:, 2]
        self.predict_temp_4 = cell_pre_data[:, 3]
        self.predict_time = cell_pre_data[:, 4]
        self.Delta_T_exp = cell_results_data[0, :] * (np.exp(num_day * cell_results_data[1, :]) - 1)
