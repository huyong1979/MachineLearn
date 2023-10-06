# Run in physics03 with conda environment ap-2021-2.2
# e.g.
# ssh physics03
# conda activate ap-2021-2.2


import numpy as np
import math


# Prediction based on the learning models for several outcomes

class Predictions:

    def __init__(self, num_data_per_day, num_day_per_prediction_1, num_day_per_prediction_2, num_day_per_prediction_3,
                 num_day_per_prediction_4, pvs, temp_threshold, temp_limit):

        self.NumDataPerDay = num_data_per_day
        self.NumDayPerPrediction_1 = num_day_per_prediction_1
        self.NumDayPerPrediction_2 = num_day_per_prediction_2
        self.NumDayPerPrediction_3 = num_day_per_prediction_3
        self.NumDayPerPrediction_4 = num_day_per_prediction_4
        self.PVs = pvs
        self.Temp_Threshold = temp_threshold
        self.Temp_Limit = temp_limit

    def long_period_prediction_least_squares(self, cell_data, cell_result_data, cell_pre_data):

        prediction_length_1 = self.NumDataPerDay * self.NumDayPerPrediction_1
        prediction_length_2 = self.NumDataPerDay * self.NumDayPerPrediction_2
        prediction_length_3 = self.NumDataPerDay * self.NumDayPerPrediction_3
        prediction_length_4 = self.NumDataPerDay * self.NumDayPerPrediction_4

        df_data = cell_result_data
        temp_end_1 = cell_pre_data[:, 0]
        temp_end_2 = cell_pre_data[:, 1]
        temp_end_3 = cell_pre_data[:, 2]
        temp_end_4 = cell_pre_data[:, 3]
        temp_prediction_1 = np.empty((prediction_length_1, 1))
        temp_prediction_2 = np.empty((prediction_length_2, 1))
        temp_prediction_3 = np.empty((prediction_length_3, 1))
        temp_prediction_4 = np.empty((prediction_length_4, 1))

        for num_pv in range(self.PVs):

            data_set = cell_data.data_matrix_pv[num_pv, :, :]
            intercept = data_set[0, -1]
            for k in range(prediction_length_1):
                temp_prediction_1[k] = intercept + (df_data[1, num_pv] * k) / self.NumDataPerDay

            temp_end_1[num_pv] = temp_prediction_1[-1]

            for k in range(prediction_length_2):
                temp_prediction_2[k] = intercept + (df_data[1, num_pv] * k) / self.NumDataPerDay

            temp_end_2[num_pv] = temp_prediction_2[-1]

            for k in range(prediction_length_3):
                temp_prediction_3[k] = intercept + (df_data[1, num_pv] * k) / self.NumDataPerDay

            temp_end_3[num_pv] = temp_prediction_3[-1]

            for k in range(prediction_length_4):
                temp_prediction_4[k] = intercept + (df_data[1, num_pv] * k) / self.NumDataPerDay

            temp_end_4[num_pv] = temp_prediction_4[-1]

            cell_pre_data[num_pv, 0] = temp_end_1[num_pv]
            cell_pre_data[num_pv, 1] = temp_end_2[num_pv]
            cell_pre_data[num_pv, 2] = temp_end_3[num_pv]
            cell_pre_data[num_pv, 3] = temp_end_4[num_pv]

        return cell_data, cell_result_data, cell_pre_data

    def long_period_prediction_quadratic_least_squares(self, cell_data, cell_result_data, cell_pre_data):

        prediction_length_1 = self.NumDataPerDay * self.NumDayPerPrediction_1
        prediction_length_2 = self.NumDataPerDay * self.NumDayPerPrediction_2
        prediction_length_3 = self.NumDataPerDay * self.NumDayPerPrediction_3
        prediction_length_4 = self.NumDataPerDay * self.NumDayPerPrediction_4

        df_data = cell_result_data
        temp_end_1 = cell_pre_data[:, 0]
        temp_end_2 = cell_pre_data[:, 1]
        temp_end_3 = cell_pre_data[:, 2]
        temp_end_4 = cell_pre_data[:, 3]
        temp_prediction_1 = np.empty((prediction_length_1, 1))
        temp_prediction_2 = np.empty((prediction_length_2, 1))
        temp_prediction_3 = np.empty((prediction_length_3, 1))
        temp_prediction_4 = np.empty((prediction_length_4, 1))

        for num_pv in range(self.PVs):

            data_set = cell_data.data_matrix_pv[num_pv, :, :]
            intercept = data_set[0, -1]
            for k in range(prediction_length_1):
                temp_prediction_1[k] = intercept + (df_data[1, num_pv] * k) / self.NumDataPerDay + df_data[
                    2, num_pv] * (
                                               (k / self.NumDataPerDay) ** 2)

            temp_end_1[num_pv] = temp_prediction_1[-1]

            for k in range(prediction_length_2):
                temp_prediction_2[k] = intercept + (df_data[1, num_pv] * k) / self.NumDataPerDay + df_data[
                    2, num_pv] * (
                                               (k / self.NumDataPerDay) ** 2)

            temp_end_2[num_pv] = temp_prediction_2[-1]

            for k in range(prediction_length_3):
                temp_prediction_3[k] = intercept + (df_data[1, num_pv] * k) / self.NumDataPerDay + df_data[
                    2, num_pv] * (
                                               (k / self.NumDataPerDay) ** 2)

            temp_end_3[num_pv] = temp_prediction_3[-1]

            for k in range(prediction_length_4):
                temp_prediction_4[k] = intercept + (df_data[1, num_pv] * k) / self.NumDataPerDay + df_data[
                    2, num_pv] * (
                                               (k / self.NumDataPerDay) ** 2)

            temp_end_4[num_pv] = temp_prediction_4[-1]

            cell_pre_data[num_pv, 0] = temp_end_1[num_pv]
            cell_pre_data[num_pv, 1] = temp_end_2[num_pv]
            cell_pre_data[num_pv, 2] = temp_end_3[num_pv]
            cell_pre_data[num_pv, 3] = temp_end_4[num_pv]

        return cell_data, cell_result_data, cell_pre_data

    def long_period_prediction_nonlinear_exponential(self, cell_data, cell_result_data, cell_pre_data):

        prediction_length_1 = self.NumDataPerDay * self.NumDayPerPrediction_1
        prediction_length_2 = self.NumDataPerDay * self.NumDayPerPrediction_2
        prediction_length_3 = self.NumDataPerDay * self.NumDayPerPrediction_3
        prediction_length_4 = self.NumDataPerDay * self.NumDayPerPrediction_4

        df_data = cell_result_data
        temp_end_1 = cell_pre_data[:, 0]
        temp_end_2 = cell_pre_data[:, 1]
        temp_end_3 = cell_pre_data[:, 2]
        temp_end_4 = cell_pre_data[:, 3]
        temp_prediction_1 = np.empty((prediction_length_1, 1))
        temp_prediction_2 = np.empty((prediction_length_2, 1))
        temp_prediction_3 = np.empty((prediction_length_3, 1))
        temp_prediction_4 = np.empty((prediction_length_4, 1))

        for num_pv in range(self.PVs):

            data_set = cell_data.data_matrix_pv[num_pv, :, :]
            intercept = data_set[0, -1]
            for k in range(prediction_length_1):
                temp_prediction_1[k] = intercept * math.exp((df_data[1, num_pv] * k) / self.NumDataPerDay)

            temp_end_1[num_pv] = temp_prediction_1[-1]

            for k in range(prediction_length_2):
                temp_prediction_2[k] = intercept * math.exp((df_data[1, num_pv] * k) / self.NumDataPerDay)

            temp_end_2[num_pv] = temp_prediction_2[-1]

            for k in range(prediction_length_3):
                temp_prediction_3[k] = intercept * math.exp((df_data[1, num_pv] * k) / self.NumDataPerDay)

            temp_end_3[num_pv] = temp_prediction_3[-1]

            for k in range(prediction_length_4):
                temp_prediction_4[k] = intercept * math.exp((df_data[1, num_pv] * k) / self.NumDataPerDay)

            temp_end_4[num_pv] = temp_prediction_4[-1]

            cell_pre_data[num_pv, 0] = temp_end_1[num_pv]
            cell_pre_data[num_pv, 1] = temp_end_2[num_pv]
            cell_pre_data[num_pv, 2] = temp_end_3[num_pv]
            cell_pre_data[num_pv, 3] = temp_end_4[num_pv]

        return cell_data, cell_result_data, cell_pre_data

    def time_length_safe_check_least_squares(self, cell_data, cell_result_data, cell_pre_data):

        temp_threshold = self.Temp_Threshold
        temp_limit = self.Temp_Limit

        df_data = cell_result_data
        temp_f = np.empty((self.PVs, 1))
        time_prediction = np.empty((self.PVs, 1))

        for num_pv in range(self.PVs):

            data_set = cell_data.data_matrix_pv[num_pv, :, :]
            temp_f[num_pv] = data_set[0, -1]

            if temp_f[num_pv] <= temp_threshold:
                if df_data[1, num_pv] > 0:
                    time_prediction[num_pv] = int(abs(temp_threshold - temp_f[num_pv]) / df_data[1, num_pv])
                else:
                    time_prediction[num_pv] = 0

            elif temp_f[num_pv] > temp_threshold or temp_f[num_pv] <= temp_limit:
                time_prediction[num_pv] = -1

            elif temp_f[num_pv] > temp_limit:
                time_prediction[num_pv] = -2

            cell_pre_data[num_pv, 4] = time_prediction[num_pv]

        return cell_data, cell_result_data, cell_pre_data

    def time_length_safe_check_quadratic_least_squares(self, cell_data, cell_result_data, cell_pre_data):

        temp_threshold = self.Temp_Threshold
        temp_limit = self.Temp_Limit

        df_data = cell_result_data
        temp_f = np.empty((self.PVs, 1))
        time_prediction = np.empty((self.PVs, 1))

        for num_pv in range(self.PVs):

            data_set = cell_data.data_matrix_pv[num_pv, :, :]
            temp_f[num_pv] = data_set[0, -1]

            if temp_f[num_pv] <= temp_threshold:
                if np.square(df_data[1, num_pv]) - 4 * df_data[2, num_pv] * (temp_f[num_pv] - temp_threshold) >= 0:
                    time_prediction[num_pv] = int((-1 * df_data[1, num_pv] + np.sqrt(
                        np.square(df_data[1, num_pv]) - 4 * df_data[2, num_pv] * (temp_f[num_pv] - temp_threshold))) / (
                                                          2 * df_data[2, num_pv]))
                else:
                    time_prediction[num_pv] = 0

            elif temp_f[num_pv] > temp_threshold or temp_f[num_pv] <= temp_limit:
                time_prediction[num_pv] = -1

            elif temp_f[num_pv] > temp_limit:
                time_prediction[num_pv] = -2

            cell_pre_data[num_pv, 4] = time_prediction[num_pv]

        return cell_data, cell_result_data, cell_pre_data

    def time_length_safe_check_nonlinear_exponential(self, cell_data, cell_result_data, cell_pre_data):

        temp_threshold = self.Temp_Threshold
        temp_limit = self.Temp_Limit

        df_data = cell_result_data
        temp_f = np.empty((self.PVs, 1))
        time_prediction = np.empty((self.PVs, 1))

        for num_pv in range(self.PVs):

            data_set = cell_data.data_matrix_pv[num_pv, :, :]
            temp_f[num_pv] = data_set[0, -1]

            if temp_f[num_pv] <= temp_threshold:
                if df_data[1, num_pv] > 0:
                    time_prediction[num_pv] = int(math.log(abs(temp_threshold / temp_f[num_pv])) / df_data[1, num_pv])
                else:
                    time_prediction[num_pv] = 0

            elif temp_f[num_pv] > temp_threshold or temp_f[num_pv] <= temp_limit:
                time_prediction[num_pv] = -1

            elif temp_f[num_pv] > temp_limit:
                time_prediction[num_pv] = -2

            cell_pre_data[num_pv, 4] = time_prediction[num_pv]

        return cell_data, cell_result_data, cell_pre_data
