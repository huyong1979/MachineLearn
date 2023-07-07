# derived from Feng Bai's OneTimeCheckProgress.py

import sys
if len(sys.argv) != 2:
    print("Cell number is required, i.e. python %s 01"%sys.argv[0])
    sys.exit()

cell = int(sys.argv[1])
assert 1 <= cell <= 30, "Cell number is out of range [1, 30]"

import time
t0 = time.time()
from datetime import datetime

from cothread.catools import caget, caput
import os
os.environ["EPICS_CA_ADDR_LIST"]="10.0.153.255"
os.environ["EPICS_CA_AUTO_ADDR_LIST"]="no"

import h5py
import numpy as np
from carchive.untwisted import arget, EXACT
import shutil

# settings
Minute = int(caget('SR:OPS-ML{1time}Time-SP' )) # 5 mins to get data
TestPeriodCoef = int(caget('SR:OPS-ML{1time}Coef-SP')) # Coefficient of Test Period: 1
NumDataPerPeriod = int(caget('SR:OPS-ML{1time}DataAmnt-SP' )) # number of data in cleaning period: 48
NumDayPerOperation = int(caget('SR:OPS-ML{1time}MeasLen-SP')) # operation days: 14
NumDayPerPrediction = int(caget('SR:OPS-ML{1time}PredictLen-SP')) # prediction days: 30
MLMethod = int(caget('SR:OPS-ML{1time}MLMethod-SP' )) # ML methods: 1. Least Squires; 2. Lasso;
lambda_reg = int(caget('SR:OPS-ML{1time}LamdaReg-SP')) # regularization parameter: 1
NumDataPerDay = int(24 * 3600 / (60 * Minute))  # 86400 / (60 * 5) = 288
NumDataPerOperation = int(NumDataPerDay * NumDayPerOperation) # 288 * 14
#Days = TestPeriodCoef  # Days Per Test
TW = 45  # Warning Temperature
TH = 60  # Hot Temperature

# get different lists of PVs
temp_pvs = [] # one-wire temperature PVs
slope_pvs = [] # slope PVs
rate_pvs = [] # rate PVs
predict_temp_pvs = [] # predict temperature PVs
predict_time_pvs = [] # predict long-time PVs

temp_pvs += ["SR:C%02d-MG{PS:QM1A}I:Ps1DCCT1-I"%cell, "SR:C%02d-MG{PS:QM1B}I:Ps1DCCT1-I"%cell,
             "SR:C%02d-MG{PS:QM2A}I:Ps1DCCT1-I"%cell, "SR:C%02d-MG{PS:QM2B}I:Ps1DCCT1-I"%cell]

if cell == 3:
    n_wires = list(range(55, 75))
elif cell == 13 or cell == 23:
    n_wires = list(range(37, 57))
elif cell == 17: # 24 PVs
    n_wires = list(range(36, 60))
elif cell == 18 or cell == 19: # 24 PVs
    n_wires = list(range(33, 57))
else:
    n_wires = list(range(33, 53))

temp_pvs += ["SR:C%02d-MTM{1wire:%02d}T-I"%(cell, n_wire) for n_wire in n_wires]
slope_pvs += ["SR:OPS-C%02d-ML{1wire:%02d}Slope-I"%(cell, n_wire) for n_wire in n_wires]
rate_pvs += ["SR:OPS-C%02d-ML{1wire:%02d}Rate-I"%(cell, n_wire) for n_wire in n_wires]
predict_temp_pvs += ["SR:OPS-C%02d-ML{1wire:%02d}Predict_Temp-I"%(cell, n_wire) for n_wire in n_wires]
predict_time_pvs += ["SR:OPS-C%02d-ML{1wire:%02d}Predict_Time-I"%(cell, n_wire) for n_wire in n_wires]
print(temp_pvs)

#retrieve the archived history data and save them in a file (per cell)
end_time = None
with h5py.File("Data/C%02d_QM_1Wires_Data.hdf5"%cell, "w") as fh5:
    data = arget(temp_pvs, start="-%d days"%NumDayPerOperation, end=end_time, match=EXACT)
    if len(temp_pvs) != len(data):
        print("[WARNING] no history data retrieved for some PVs")

    for pv_name, (V, M) in data.items():
        vals = np.empty((3, V.shape[0]))
        vals[0, :] = V[:, 0]
        vals[1, :] = M['sec']
        vals[2, :] = M['ns']
        fh5[pv_name] = vals

# Data/Cxx_QM_1Wires_Data.hdf5 will be changed. So save a copy of it ...
shutil.copy2("Data/C%02d_QM_1Wires_Data.hdf5"%cell, "Data/C%02d_QM_1Wires_Data_Orig.hdf5"%cell)
t1 = time.time()
print("it takes %f-sec to retrieve %d-day history data"%(t1-t0, NumDayPerOperation))

# Initialize the data preparation; Transfer HDF5 to Variables
from CellDataPreparation import CellDataPrep
prep = CellDataPrep(Minute, NumDayPerOperation, NumDataPerDay, NumDataPerOperation)

from CellData import CellVariableData
from ResultsDataOneTimeCell import CellResultsData
if 16 <= cell <= 18:
    cell_data = CellVariableData(NumDataPerOperation, 24)
    cell_results = CellResultsData(24)
else:
    cell_data = CellVariableData(NumDataPerOperation, 20)
    cell_results = CellResultsData(20)

prep.data_reorganization(cell)
cell_data = prep.data_transfer(cell, cell_data)
#print(cell_data.data_matrix_pv.shape)
t2 = time.time()
print("it takes %f-sec to re-organize and transfer data"%(t2-t1))
#print(cell_data.data_matrix_pv)

# Establish the ML Model based on the Given Operational Period
from OneTimeCheckMLAlgorithms import ML_and_Prediction_One_Time_Check
MLSystem = ML_and_Prediction_One_Time_Check(Minute, NumDataPerDay, NumDataPerOperation, 
                                NumDataPerPeriod, MLMethod, lambda_reg, TW, TH, NumDayPerPrediction)
  
# One Time Check ML Model and Prediction
_, _, CellOutput = MLSystem.one_time_ml_check_cell(cell_data, cell_results)
print("Results of Cell %02d: "%cell)
print("The slopes parameters are: ", *CellOutput.slope)
print("The rate parameters are: ", *CellOutput.rate)
print("The predict temperature parameters are: ", *CellOutput.predict_temp)
print("The predict long time parameters are: ", *CellOutput.predict_time)
t3 = time.time()
print("it takes %f-sec to process data and get results"%(t3-t2))

caput(slope_pvs, CellOutput.slope)
caput(rate_pvs, CellOutput.rate)
caput(predict_temp_pvs, CellOutput.predict_temp)
caput(predict_time_pvs, CellOutput.predict_time)
#t4 = time.time()
#print("it takes %f-sec to caput the results\n"%(t4-t3))
