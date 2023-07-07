# Run in physics03 with conda environment ap-2021-2.2
# e.g.
# ssh physics03
# conda activate ap-2021-2.2

import numpy as np
from sklearn.ensemble import IsolationForest


class DataCleaning:

    def __init__(self, minute, num_data_per_day, num_data_per_test, num_data_per_period, pvs):

        self.temp_end = np.zeros((pvs, 1))
        self.minute = minute
        self.num_data_per_day = num_data_per_day
        self.num_data_per_test = num_data_per_test
        self.num_data_per_period = num_data_per_period
        self.pvs = pvs

    def data_cleaning(self, cell_data):

        for num_pv in range(self.pvs):

            data_set = cell_data.data_matrix_pv[num_pv, :, :]
            data_set_update = np.empty((np.size(data_set, 0), np.size(data_set, 1)))
            data_set_update_iso = np.empty((np.size(data_set, 0), np.size(data_set, 1)))
            num_period = int((np.size(data_set, 1)) / self.num_data_per_period)

            total_outlier_num_eu = 0
            total_outlier_num_iso = 0

            for i in range(num_period):
                outlier_num = 0
                data_period = data_set[:, i * self.num_data_per_period:(i + 1) * self.num_data_per_period]
                temp_i_den_period = data_period[0, :]
                mean_temp = temp_i_den_period.mean()

                eu_norm = np.sqrt((temp_i_den_period - mean_temp) ** 2)
                mean_eu_norm = eu_norm.mean()
                eu_norm_dist = np.abs(eu_norm - mean_eu_norm)
                #            eu_norm_dist = np.abs(temp_i_den_period-mean_temp)

                data_period_regression = data_period[0:2, :]
                outlier_period_id = []
                for j in range(self.num_data_per_period):
                    if eu_norm_dist[j] > 2:
                        outlier_period_id.append(j)
                        outlier_num += 1

                data_period_regression = np.delete(data_period_regression, outlier_period_id, 1)
                data_period_matrix = np.transpose(data_period_regression)

                n = np.size(data_period_matrix[:, 1])
                one_vector = np.ones((n, 1))
                var_vector_init = np.delete(data_period_matrix, 0, 1)
                var_vector_diff = var_vector_init - var_vector_init[0]
                # var_vector = var_vector_diff / (self.num_data_per_test * self.minute * 60)
                var_vector = var_vector_diff / 86400

                a_matrix_one = one_vector
                a_matrix = np.append(a_matrix_one, var_vector, axis=1)
                b_vector = np.delete(data_period_matrix, 1, 1)

                period_theta_compute = np.linalg.pinv(np.dot(np.transpose(a_matrix), a_matrix)).dot(
                    np.dot(np.transpose(a_matrix), b_vector))

                data_period_update = data_period
                for k in range(np.size(outlier_period_id)):
                    data_period_update[0, outlier_period_id[k]] = period_theta_compute[0] + (
                            outlier_period_id[k] / self.num_data_per_period) * period_theta_compute[1]

                data_set_update[:, i * self.num_data_per_period:(i + 1) * self.num_data_per_period] = data_period_update
                total_outlier_num_eu += outlier_num

                outlier_num_iso = 0
                data_period_iso = data_period_update
                temp_time_i_den_period = data_period[0:2, :]
                temp_time_i_den_period_iso = data_period_iso[0:2, :]
                clf = IsolationForest(contamination=0.02).fit(np.transpose(temp_time_i_den_period_iso))
                iso_score = clf.predict(np.transpose(temp_time_i_den_period))
                outlier_period_id_iso = []
                for j in range(self.num_data_per_period):
                    if iso_score[j] == -1:
                        outlier_period_id_iso.append(j)
                        outlier_num_iso += 1

                data_period_regression_iso = data_period_update[0:2, :]
                data_period_regression_iso = np.delete(data_period_regression_iso, outlier_period_id_iso, 1)
                data_period_matrix_iso = np.transpose(data_period_regression_iso)

                n = np.size(data_period_matrix_iso[:, 1])
                one_vector_iso = np.ones((n, 1))
                var_vector_iso_init = np.delete(data_period_matrix_iso, 0, 1)
                var_vector_iso_diff = var_vector_iso_init - var_vector_iso_init[0]
                # var_vector_iso = var_vector_iso_diff / (self.num_data_per_test * self.minute * 60)
                var_vector_iso = var_vector_iso_diff / 86400

                a_matrix_iso_one = one_vector_iso
                a_matrix_iso = np.append(a_matrix_iso_one, var_vector_iso, axis=1)
                b_vector_iso = np.delete(data_period_matrix_iso, 1, 1)

                period_theta_iso_compute = np.linalg.pinv(np.dot(np.transpose(a_matrix_iso), a_matrix_iso)).dot(
                    np.dot(np.transpose(a_matrix_iso), b_vector_iso))

                data_period_update_iso = data_period_update
                for k in range(np.size(outlier_period_id_iso)):
                    data_period_update_iso[0, outlier_period_id_iso[k]] = period_theta_iso_compute[0] + (
                            outlier_period_id_iso[k] / self.num_data_per_period) * period_theta_iso_compute[1]

                data_set_update_iso[:, i * self.num_data_per_period:(i + 1) * self.num_data_per_period] = data_period_update_iso
                total_outlier_num_iso += outlier_num_iso

            #           print("The number of outlier by Eucidean Norm is", TotalOutlierNum_Eucid)
            #           print("The number of outlier by Isolation Forest is", TotalOutlierNum_Iso)

            cell_data.data_matrix_pv[num_pv, :, :] = data_set_update_iso

            self.temp_end[num_pv] = data_set_update_iso[0, -1]

        return cell_data
