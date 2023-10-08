# derived from Feng Bai's OneTimeCheckProgress.py

import sys
import time
from datetime import datetime
from cothread.catools import caget, caput
import os
import h5py
import numpy as np
from carchive.untwisted import arget, EXACT
import shutil
import pandas as pd

if len(sys.argv) < 2:
    sys.exit("Cell number is required, i.e. python %s 01"%sys.argv[0])

cell = int(sys.argv[1])
assert 1 <= cell <= 30, "Cell number is out of range [1, 30]"

os.environ["EPICS_CA_ADDR_LIST"]="10.0.153.255"
os.environ["EPICS_CA_AUTO_ADDR_LIST"]="no"

print("%s: processing Cell %d ..."%(datetime.now(), cell))
t0 = time.time()

# settings
Minute = int(caget('SR:OPS-ML{1time}Time-SP' )) # 5 mins to get data
TestPeriodCoef = int(caget('SR:OPS-ML{1time}Coef-SP')) # Coefficient of Test Period: 1
NumDataPerPeriod = int(caget('SR:OPS-ML{1time}DataAmnt-SP' )) # number of data in cleaning period: 48
NumDayPerOperation = int(caget('SR:OPS-ML{1time}MeasLen-SP')) # operation days: 14
NumDayPerPrediction = int(caget('SR:OPS-ML{1time}PredictLen-SP')) # prediction days: 30
NumDayPerPrediction_1 = int(caget('SR:OPS-ML{}T1-SP')) # 3 days
NumDayPerPrediction_2 = int(caget('SR:OPS-ML{}T2-SP')) # 7 days
NumDayPerPrediction_3 = int(caget('SR:OPS-ML{}T3-SP')) # 14 days
NumDayPerPrediction_4 = int(caget('SR:OPS-ML{}T4-SP')) # 30 days
MLMethod = int(caget('SR:OPS-ML{1time}MLMethod-SP' )) # ML methods: 1. Least Squires; 2. Lasso;
lambda_reg = int(caget('SR:OPS-ML{1time}LamdaReg-SP')) # regularization parameter: 1
NumDataPerDay = int(24 * 3600 / (60 * Minute))  # 86400 / (60 * 5) = 288
NumDataPerOperation = int(NumDataPerDay * NumDayPerOperation) # 288 * 14
# Days = TestPeriodCoef  # Days Per Test
TW = int(caget('SR:OPS-ML{1time}ThreshTemp-SP')) # Warning Temperature: 40
TH = int(caget('SR:OPS-ML{1time}WarnTemp-SP')) # Hot Temperature: 60

if cell == 3:
    n_wires = list(range(55, 75))
    #n_wires = list(range(58, 60))
elif cell == 13 or cell == 23:
    n_wires = list(range(37, 57))
elif cell == 17: # 24 PVs
    n_wires = list(range(36, 60))
elif cell == 18 or cell == 19: # 24 PVs
    n_wires = list(range(33, 57))
else:
    n_wires = list(range(33, 53))

# different lists of PVs
temp_pvs = ["SR:C%02d-MTM{1wire:%02d}T-I"%(cell, n_wire) for n_wire in n_wires]
slope_pvs = ["SR:OPS-C%02d-ML{1wire:%02d}Slope-I"%(cell, n_wire) for n_wire in n_wires]
rate_pvs = ["SR:OPS-C%02d-ML{1wire:%02d}Rate-I"%(cell, n_wire) for n_wire in n_wires]
predict_temp_pvs = ["SR:OPS-C%02d-ML{1wire:%02d}Predict_Temp-I"%(cell, n_wire) for n_wire in n_wires]
predict_time_pvs = ["SR:OPS-C%02d-ML{1wire:%02d}Predict_Time-I"%(cell, n_wire) for n_wire in n_wires]
#print(temp_pvs)

from CellData import CellVariableData
from ResultsDataOneTimeCell import CellResultsData
if 17 <= cell <= 19:
    cell_data = CellVariableData(NumDataPerOperation, 24)
    cell_results = CellResultsData(24)
else:
    cell_data = CellVariableData(NumDataPerOperation, 20)
    cell_results = CellResultsData(20)

# retrieve archived history data, then resample
def resample_data(origin_data, ts, pv, num):
    origin_data.append(caget(pv))
    ts.append(time.time())  # have to add the current timestamp
    ts[0] = ts[-1] - num * 5 * 60
    dtime = pd.to_datetime(ts, unit='s')
    series = pd.Series(origin_data, dtime)
    return series.resample('5Min').ffill().dropna()

op_status = arget("SR-OPS{}Mode-Sts", start="-%d days"%NumDayPerOperation, end=None, match=EXACT)
# resample the OP status history data up to 4032 points
status_data = list(op_status[0][:, 0])  # op_status is a tuple
status_ts = list(op_status[1]['sec'] + op_status[1]['ns'] / 10 ** 9)  # ns is needed
status_df = resample_data(status_data, status_ts, 'SR-OPS{}Mode-Sts', NumDataPerOperation)
#pd.set_option('display.max_rows', len(status_df))
#print(status_df)
caput("SR-OPS{}Mode-Sts_Wf", status_df.values[:NumDataPerOperation])

data = arget(temp_pvs, start="-%d days"%NumDayPerOperation, end=None, match=EXACT)
if len(temp_pvs) != len(data):
    print("[WARNING] no history data retrieved for some PVs")

data_matrix = []
for pv_name, (V, M) in data.items():
    vals = np.empty((3, V.shape[0]))
    vals[0, :] = V[:, 0]
    vals[1, :] = M['sec']
    #vals[2, :] = M['ns']  # ns resolution is not needed for temperature data

    # resample the temperature history data up to 4032 points
    temp_data = list(vals[0, :][:NumDataPerOperation])
    temp_ts = list(vals[1, :][:NumDataPerOperation])
    df = resample_data(temp_data, temp_ts, pv_name, NumDataPerOperation)
    caput(pv_name + '_Wf_', df.values[:NumDataPerOperation])

    # only keep machine-in-operation temperature data
    _data = [df.values[i] for i in range(NumDataPerOperation) if status_df.values[i] == 0]
    x_old = np.linspace(0, len(_data), len(_data))
    x_new = np.linspace(0, NumDataPerOperation, NumDataPerOperation)
    valid_temp_data = np.interp(x_new, x_old, _data)
    #print(len(valid_temp_data))
    caput(pv_name + '_Wf', valid_temp_data)

    _vals = np.empty((3, NumDataPerOperation))
    _vals[0, :] = valid_temp_data
    _vals[1, :] = df.index[:NumDataPerOperation]
    _vals[2, :] = [0] * NumDataPerOperation
    data_matrix.append(_vals)

cell_data.data_matrix_pv = np.stack(data_matrix)  # have to stack a list of 2-d array
print(cell_data.data_matrix_pv)

if caget('SR:OPS{ML}SaveFile-Cmd'):
    with h5py.File("python/Data/C%02d_QM_1Wires_Data.hdf5"%cell, "w") as fh5:
        for pv_name, (V, M) in data.items():
            vals = np.empty((3, V.shape[0]))
            vals[0, :] = V[:, 0]
            vals[1, :] = M['sec']
            vals[2, :] = M['ns']
            fh5[pv_name] = vals

t1 = time.time()
print("it takes %f-sec to retrieve and resample/re-org %d-day history data in Cell %d"%(t1-t0, NumDayPerOperation, cell))

# Establish the ML Model based on the Given Operational Period
from OneTimeCheckMLAlgorithms import ML_and_Prediction_One_Time_Check
MLSystem = ML_and_Prediction_One_Time_Check(Minute, NumDataPerDay, NumDataPerOperation, NumDataPerPeriod, MLMethod, TW, TH,
                                            NumDayPerPrediction_1, NumDayPerPrediction_2,
                                            NumDayPerPrediction_3, NumDayPerPrediction_4)
  
# One Time Check ML Model and Prediction
cell_data_cleaned, _, CellOutput = MLSystem.one_time_ml_check_cell(cell_data, cell_results)
#print("Results of Cell %02d: "%cell)
#print("The slopes parameters are: ", *CellOutput.slope)
##print("The rate parameters are: ", *CellOutput.rate)
##print("The predict temperature parameters are: ", *CellOutput.predict_temp)
##print("The predict long time parameters are: ", *CellOutput.predict_time)
t3 = time.time()
print("it takes %f-sec to process data and get results in Cell %d"%(t3-t1, cell))

caput(slope_pvs, CellOutput.slope)
# caput(rate_pvs, CellOutput.rate)
caput(predict_temp_pvs, CellOutput.predict_temp_1)
caput(predict_time_pvs, CellOutput.predict_time)
#t4 = time.time()
#print("it takes %f-sec to caput the results\n"%(t4-t3))
