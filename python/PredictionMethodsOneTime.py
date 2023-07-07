# Run in physics03 with conda environment ap-2021-2.2
# e.g.
# ssh physics03
# conda activate ap-2021-2.2


import numpy as np


class Predictions:

    def __init__(self, num_data_per_day, num_day_per_prediction, pvs, temp_threshold):

        self.NumDataPerDay = num_data_per_day
        self.NumDayPerPrediction = num_day_per_prediction
        self.PVs = pvs
        self.Temp_Threshold = temp_threshold

    def long_period_prediction_least_squares(self, cell_data, cell_result_data, cell_pre_data):

        prediction_length = self.NumDataPerDay * self.NumDayPerPrediction

        df_data = cell_result_data
        temp_end = cell_pre_data[:, 0]
        temp_prediction = np.empty((prediction_length, 1))

        for num_pv in range(self.PVs):

            data_set = cell_data.data_matrix_pv[num_pv, :, :]
            intercept = data_set[0, -1]
            for k in range(prediction_length):
                temp_prediction[k] = intercept + (df_data[1, num_pv] * k) / prediction_length

            temp_end[num_pv] = temp_prediction[-1]
            cell_pre_data[num_pv, 0] = temp_end[num_pv]

        return cell_data, cell_result_data, cell_pre_data

    def long_period_prediction_lasso(self, cell_data, cell_result_data, cell_pre_data):

        prediction_length = self.NumDataPerDay * self.NumDayPerPrediction

        df_data = cell_result_data
        temp_end = cell_pre_data[:, 0]
        temp_prediction = np.empty((prediction_length, 1))

        for num_pv in range(self.PVs):

            data_set = cell_data.data_matrix_pv[num_pv, :, :]
            intercept = data_set[0, -1]
            for k in range(prediction_length):
                temp_prediction[k] = intercept + (df_data[1, num_pv] * k) / prediction_length

            temp_end[num_pv] = temp_prediction[-1]
            cell_pre_data[num_pv, 0] = temp_end[num_pv]

        return cell_data, cell_result_data, cell_pre_data

    def time_length_safe_check_least_squares(self, cell_data, cell_result_data, cell_pre_data):

        temp_threshold = self.Temp_Threshold

        df_data = cell_result_data
        temp_f = np.empty((self.PVs, 1))
        time_prediction = np.empty((self.PVs, 1))

        for num_pv in range(self.PVs):

            data_set = cell_data.data_matrix_pv[num_pv, :, :]
            temp_f[num_pv] = data_set[0, -1]

            if temp_f[num_pv] < temp_threshold:
                if df_data[1, num_pv] > 0:
                    time_prediction[num_pv] = int(abs(temp_threshold - temp_f[num_pv]) / df_data[1, num_pv])
                else:
                    time_prediction[num_pv] = 0

            elif temp_f[num_pv] > temp_threshold or temp_f[num_pv] > temp_threshold:
                time_prediction[num_pv] = 1

            cell_pre_data[num_pv, 1] = time_prediction[num_pv]

        return cell_data, cell_result_data, cell_pre_data

    def time_length_safe_check_lasso(self, cell_data, cell_result_data, cell_pre_data):

        temp_threshold = self.Temp_Threshold

        df_data = cell_result_data
        temp_f = np.empty((self.PVs, 1))
        time_prediction = np.empty((self.PVs, 1))

        for num_pv in range(self.PVs):

            data_set = cell_data.data_matrix_pv[num_pv, :, :]
            temp_f[num_pv] = data_set[0, -1]

            if temp_f[num_pv] < temp_threshold:
                if df_data[1, num_pv] > 0:
                    time_prediction[num_pv] = int(abs(temp_threshold - temp_f[num_pv]) / df_data[1, num_pv])
                else:
                    time_prediction[num_pv] = 0

            elif temp_f[num_pv] > temp_threshold or temp_f[num_pv] > temp_threshold:
                time_prediction[num_pv] = -1

            cell_pre_data[num_pv, 1] = time_prediction[num_pv]

        return cell_data, cell_result_data, cell_pre_data
