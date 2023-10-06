# Run in physics03 with conda environment ap-2021-2.2
# e.g.
# ssh physics03
# conda activate ap-2021-2.2


import numpy as np
import math


# This is the regression learning with system, the whole times series analysis will be performed by the regression analysis

class MachineLearning:

    def __init__(self, minute, num_data_per_test, pvs):

        self.minute = minute
        self.num_data_per_test = num_data_per_test
        self.pvs = pvs

    def linear_regression_least_squares(self, cell_data, cell_results_data):

        num_data_per_test = int(self.num_data_per_test)
        theta_loss_matrix = cell_results_data

        for num_pv in range(self.pvs):
            data_set = cell_data.data_matrix_pv[num_pv, :, :]

            data_regression_per_test = data_set[0:2, 0:(num_data_per_test - 1)]
            data_matrix = np.transpose(data_regression_per_test)

            n = np.size(data_matrix[:, 1])
            #                     theta = theta_matrix[:, num_pv]
            one_vector = np.ones((n, 1))
            var_vector_init = np.delete(data_matrix, 0, 1)

            #             max_var_vector = max(var_vector_init)
            #             min_var_vector = min(var_vector_init)

            #             if abs(max_var_vector - min_var_vector) <= 0.125:
            #                 var_vector_init_mean = var_vector_init.mean
            #                 for j in range(len(var_vector_init)):
            #                    var_vector_init[j] = var_vector_init_mean

            var_vector_diff = var_vector_init - var_vector_init[0]
            # var_vector = var_vector_diff / (self.num_data_per_test * self.minute * 60)
            var_vector = var_vector_diff / 86400

            a_matrix_one = one_vector
            a_matrix = np.append(a_matrix_one, var_vector, axis=1)
            b_vector = np.delete(data_matrix, 1, 1)

            #             beta = np.linalg.pinv(np.dot(np.transpose(a_matrix), a_matrix)) + lambda_reg * np.eye(2)

            theta_compute = (np.linalg.pinv(np.dot(np.transpose(a_matrix), a_matrix))).dot(
                np.dot(np.transpose(a_matrix), b_vector))

            num_sol = a_matrix @ theta_compute
            res = (b_vector - num_sol) ** 2
            loss = math.sqrt((1 / n) * (np.sum(res)))

            theta_loss_matrix[0, num_pv] = b_vector[0]
            theta_loss_matrix[1, num_pv] = theta_compute[1]
            theta_loss_matrix[2, num_pv] = 0
            theta_loss_matrix[3, num_pv] = loss

        cell_results_data = theta_loss_matrix

        return cell_data, cell_results_data

    def quadratic_regression_least_squares(self, cell_data, cell_results_data):

        num_data_per_test = int(self.num_data_per_test)
        theta_loss_matrix = cell_results_data

        for num_pv in range(self.pvs):
            data_set = cell_data.data_matrix_pv[num_pv, :, :]

            data_regression_per_test = data_set[0:2, 0:(num_data_per_test - 1)]
            data_matrix = np.transpose(data_regression_per_test)

            n = np.size(data_matrix[:, 1])
            #                     theta = theta_matrix[:, num_pv]
            one_vector = np.ones((n, 1))
            var_vector_init = np.delete(data_matrix, 0, 1)

            #             max_var_vector = max(var_vector_init)
            #             min_var_vector = min(var_vector_init)

            #             if abs(max_var_vector - min_var_vector) <= 0.125:
            #                 var_vector_init_mean = var_vector_init.mean
            #                 for j in range(len(var_vector_init)):
            #                    var_vector_init[j] = var_vector_init_mean

            var_vector_diff = var_vector_init - var_vector_init[0]
            # var_vector = var_vector_diff / (self.num_data_per_test * self.minute * 60)
            var_vector = var_vector_diff / 86400
            var_vector_square = np.square(var_vector)

            a_matrix_one = one_vector
            a_matrix = np.append(a_matrix_one, var_vector, axis=1)
            a_matrix = np.append(a_matrix, var_vector_square, axis=1)
            b_vector = np.delete(data_matrix, 1, 1)

            #             beta = np.linalg.pinv(np.dot(np.transpose(a_matrix), a_matrix)) + lambda_reg * np.eye(2)

            theta_compute = (np.linalg.pinv(np.dot(np.transpose(a_matrix), a_matrix))).dot(
                np.dot(np.transpose(a_matrix), b_vector))

            num_sol = a_matrix @ theta_compute
            res = (b_vector - num_sol) ** 2
            loss = math.sqrt((1 / n) * (np.sum(res)))

            theta_loss_matrix[0, num_pv] = b_vector[0]
            theta_loss_matrix[1, num_pv] = theta_compute[1]
            theta_loss_matrix[2, num_pv] = theta_compute[2]
            theta_loss_matrix[3, num_pv] = loss

        cell_results_data = theta_loss_matrix

        return cell_data, cell_results_data

    def nonlinear_regression_exponential(self, cell_data, cell_results_data):

        num_data_per_test = int(self.num_data_per_test)
        theta_loss_matrix = cell_results_data

        for num_pv in range(self.pvs):

            data_set = cell_data.data_matrix_pv[num_pv, :, :]

            data_regression_per_test = data_set[0:2, 0:(num_data_per_test - 1)]
            data_matrix = np.transpose(data_regression_per_test)

            n = np.size(data_matrix[:, 1])
            #           theta = theta_matrix[:, num_pv]

            one_vector = np.ones((n, 1))
            var_vector_init = np.delete(data_matrix, 0, 1)

            # max_var_vector = max(var_vector_init)
            # min_var_vector = min(var_vector_init)

            # if abs(max_var_vector - min_var_vector) <= 0.125:

            #    var_vector_init_mean = var_vector_init.mean

            #    for j in range(len(var_vector_init)):
            #        var_vector_init[j] = var_vector_init_mean

            var_vector_diff = var_vector_init - var_vector_init[0]
            # var_vector = var_vector_diff / (self.num_data_per_test * self.minute * 60)
            var_vector = var_vector_diff / 86400

            a_matrix_one = one_vector
            a_matrix = np.append(a_matrix_one, var_vector, axis=1)
            y_vector = np.delete(data_matrix, 1, 1)
            b_vector = np.log(y_vector)

            theta_compute = (np.linalg.pinv(np.dot(np.transpose(a_matrix), a_matrix))).dot(
                np.dot(np.transpose(a_matrix), b_vector))

            num_sol = a_matrix @ theta_compute
            res = (y_vector - np.exp(num_sol)) ** 2
            loss = math.sqrt((1 / n) * (np.sum(res)))

            theta_loss_matrix[0, num_pv] = math.exp(b_vector[0])
            theta_loss_matrix[1, num_pv] = theta_compute[1]
            theta_loss_matrix[2, num_pv] = 0
            theta_loss_matrix[3, num_pv] = loss

        cell_results_data = theta_loss_matrix

        return cell_data, cell_results_data
