import h5py
import numpy as np


class CellDataPrep:
    def __init__(self, minute, days, num_data_per_day, num_data_per_test):
        self.Minute = minute
        self.Days = days
        self.NumDataPerDay = num_data_per_day
        self.NumDataPerTest = num_data_per_test


    def data_reorganization(self, cell):
        fh5 = h5py.File("Data/C%02d_QM_1Wires_Data.hdf5"%(cell), "a")

        for num_pv in range(len(list(fh5.keys()))):
            wire_pv = list(fh5.keys())[num_pv]
            wire_data = fh5[wire_pv][...]
            num_del = []

            for i in range(len(wire_data[0, :])):
                if wire_data[0, i] == 0:
                    num_del.append(i)

            update_wire_data = np.delete(wire_data, num_del, 1)
            del fh5[wire_pv]
            fh5[wire_pv] = update_wire_data

        for num_pv in range(4, len(list(fh5.keys()))):
            wire_pv = list(fh5.keys())[num_pv]
            wire_data = fh5[wire_pv][...]
            stp_len = int(60 * self.Minute)
            time_slots = int((86400 // stp_len) * self.Days)

            new_time_index = np.arange(time_slots)
            new_time = np.zeros(time_slots)
            new_time_true = np.zeros(time_slots)
            new_value = np.zeros(time_slots)
            wire_data_pool = wire_data

            new_time[0] = 0
            new_time_true[0] = wire_data[1, 0]
            new_value[0] = wire_data[0, 0]
            wire_data_pool = np.delete(wire_data_pool, 0, 1)

            for i in range(1, time_slots):
                new_time[i] = i * stp_len
                new_time_true[i] = wire_data[1, 0] + i * stp_len
                del_num = []
                new_value_add = []

                if wire_data_pool.any():
                    if wire_data_pool[1, 0] <= new_time_true[i]:
                        new_value_add = wire_data_pool[0, 0]
                        del_num = [0]
                        for j in range(1, len(wire_data_pool[0, :])):
                            if wire_data_pool[1, j] <= new_time_true[i]:
                                new_value_add = wire_data_pool[0, j]
                                del_num.append(j)
                            else:
                                break
                        wire_data_pool = np.delete(wire_data_pool, del_num, 1)
                    else:
                        new_value_add = new_value[i - 1]
                else:
                    new_value_add = new_value[i - 1]
                new_value[i] = new_value_add

            update_wire_data = np.empty((3, new_time_index.shape[0]))
            update_wire_data[0, :] = new_value[:]
            update_wire_data[1, :] = new_time[:]
            update_wire_data[2, :] = new_time_true[:]
            del fh5[wire_pv]
            fh5[wire_pv] = update_wire_data

        fh5.close()


    def data_transfer(self, cell, cell_data):
        fh5 = h5py.File("Data/C%02d_QM_1Wires_Data.hdf5"%(cell), "a")

        for num_pv in range(4, len(list(fh5.keys()))):
            wire_pv = list(fh5.keys())[num_pv]
            wire_data = fh5[wire_pv][...]
            num = num_pv - 4

            cell_pv_matrix_data = cell_data.data_matrix_pv[num, :, :]

            for i in range(self.NumDataPerTest):
                cell_pv_matrix_data[0, i] = wire_data[0, i]
                cell_pv_matrix_data[1, i] = wire_data[1, i]
                cell_pv_matrix_data[2, i] = wire_data[2, i]

            cell_data.data_matrix_pv[num, :, :] = cell_pv_matrix_data

        fh5.close()

        return cell_data
