# Data Flow Chart in the Operation with machine learning methods

import numpy as np
from DataCleaning import DataCleaning
from MachineLearningMethodsOneTime import MachineLearning
from PredictionMethodsOneTime import Predictions
from OneTimeCheckDispay import OutputForOneTimeCheck


class ML_and_Prediction_One_Time_Check:

    def __init__(self, minute, num_data_per_day, num_data_per_test, num_data_per_period, ml_method,
                 lambda_reg, temp_threshold, temp_limit, num_day_per_prediction):

        self.Minute = minute
        self.NumDataPerDay = num_data_per_day
        self.NumDataPerTest = num_data_per_test
        self.NumDataPerPeriod = num_data_per_period
        self.MLMethod = ml_method
        self.lambda_reg = lambda_reg
        self.Temp_Threshold = temp_threshold
        self.Temp_Limit = temp_limit
        self.NumDayPerPrediction = num_day_per_prediction

    def one_time_ml_check_cell(self, cellxx_data, cellxx_results):
        # read data and establish ML models
        cellxx_output = OutputForOneTimeCheck()
        cell_data = cellxx_data
        cell_results_data = cellxx_results.result_matrix_cell
        cell_pre_data = cellxx_results.predict_tem_result_cell
        cell_output = cellxx_output
        #print(cell_data.n_pvs)

        cleaning = DataCleaning(self.Minute, self.NumDataPerDay, self.NumDataPerTest, 
                                self.NumDataPerPeriod, cell_data.n_pvs)

        machine_learning_methods = MachineLearning(self.Minute, self.lambda_reg, self.NumDataPerTest, 
                                     cell_data.n_pvs)

        prediction = Predictions(self.NumDataPerDay, self.NumDayPerPrediction, 
                                 cell_data.n_pvs, self.Temp_Threshold)

        # Data Cleaning (based on the reorganized data, identify outliers and resolutions)
        cell_data = cleaning.data_cleaning(cell_data)

        #temp_end = np.empty(cell_data.n_pvs)
        #for num_pv in range(cell_data.n_pvs):
            #matrix = cell_data.data_matrix_pv[num_pv, :, :]
            #temp_end[num_pv] = matrix[0, -1]

        # Machine Learning Methods (Linear regression -> Accumulated regression -> Prediction)
        if self.MLMethod == 1:
            # Least Square Method / Ridge Method
            cell_data, cell_results_data = machine_learning_methods.linear_regression_least_squares(cell_data,                                                                                             
                                                                                                    cell_results_data)

            cell_data, cell_results_data, cell_pre_data = prediction.long_period_prediction_least_squares(cell_data,
                                                                                                          cell_results_data,
                                                                                                          cell_pre_data)

            cell_data, cell_results_data, cell_pre_data = prediction.time_length_safe_check_least_squares(cell_data,
                                                                                                          cell_results_data,
                                                                                                          cell_pre_data)

        elif self.MLMethod == 2:
            # Lasso Method
            cell_data, cell_results_data = machine_learning_methods.linear_regression_lasso(cell_data,
                                                                                            cell_results_data)

            cell_data, cell_results_data, cell_pre_data = prediction.long_period_prediction_lasso(cell_data,
                                                                                                  cell_results_data,
                                                                                                  cell_pre_data)

            cell_data, cell_results_data, cell_pre_data = prediction.time_length_safe_check_lasso(cell_data,
                                                                                                  cell_results_data,
                                                                                                  cell_pre_data)

        # Update the output data
        cell_output.display_slope_predict(cell_results_data, cell_pre_data)
        # Update all of the results data
        cellxx_data = cell_data
        cellxx_results.result_matrix_cell = cell_results_data
        cellxx_results.predict_tem_result_cell = cell_pre_data
        cellxx_output = cell_output

        return cellxx_data, cellxx_results, cellxx_output
