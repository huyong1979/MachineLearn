#!/epics/iocs/elauncher/bin/linux-x86_64/scriptlaunch

epicsEnvSet("IOCNAME","MachineLearn")
epicsEnvSet("HOSTNAME","physics3")
epicsEnvSet("PWD","/epics/iocs/MachineLearn")

#the line above (#!...) is not a comment: it actually executes the IOC binary  
# load common settings, including conda/python environment 
</epics/iocs/elauncher/commonSt.cmd
#</epics/iocs/elauncher-debian/commonSt.cmd

# other environment variable(s), including the person who is in charge
epicsEnvSet("ENGINEER","smithr x7385")

## Load record instances

dbLoadRecords("./db/MLinput.db")
dbLoadRecords("./db/MLoutput_03.db")
dbLoadRecords("./db/MLoutput_17.db")
dbLoadRecords("./db/MLoutput_13_23.db", "CELL=13")
dbLoadRecords("./db/MLoutput_13_23.db", "CELL=23")
dbLoadRecords("./db/MLoutput_18_19.db", "CELL=18")
dbLoadRecords("./db/MLoutput_18_19.db", "CELL=19")
dbLoadRecords("./db/MLoutput_default.db", "CELL=01")
dbLoadRecords("./db/MLoutput_default.db", "CELL=02")
dbLoadRecords("./db/MLoutput_default.db", "CELL=04")
dbLoadRecords("./db/MLoutput_default.db", "CELL=05")
dbLoadRecords("./db/MLoutput_default.db", "CELL=06")
dbLoadRecords("./db/MLoutput_default.db", "CELL=07")
dbLoadRecords("./db/MLoutput_default.db", "CELL=08")
dbLoadRecords("./db/MLoutput_default.db", "CELL=09")
dbLoadRecords("./db/MLoutput_default.db", "CELL=10")
dbLoadRecords("./db/MLoutput_default.db", "CELL=11")
dbLoadRecords("./db/MLoutput_default.db", "CELL=12")
dbLoadRecords("./db/MLoutput_default.db", "CELL=14")
dbLoadRecords("./db/MLoutput_default.db", "CELL=15")
dbLoadRecords("./db/MLoutput_default.db", "CELL=16")
dbLoadRecords("./db/MLoutput_default.db", "CELL=20")
dbLoadRecords("./db/MLoutput_default.db", "CELL=21")
dbLoadRecords("./db/MLoutput_default.db", "CELL=22")
dbLoadRecords("./db/MLoutput_default.db", "CELL=24")
dbLoadRecords("./db/MLoutput_default.db", "CELL=25")
dbLoadRecords("./db/MLoutput_default.db", "CELL=26")
dbLoadRecords("./db/MLoutput_default.db", "CELL=27")
dbLoadRecords("./db/MLoutput_default.db", "CELL=28")
dbLoadRecords("./db/MLoutput_default.db", "CELL=29")
dbLoadRecords("./db/MLoutput_default.db", "CELL=30")


#dbLoadRecords("./db/opSum.db")
#dbLoadRecords("./db/opMessages.db")
#dbLoadRecords("./db/slitAlarm.db")
#dbLoadRecords("./db/FEalarms.db")
#dbLoadRecords("./db/linacAlarms.db")
#dbLoadRecords("./db/radMon.db")
#dbLoadRecords("./db/alarmEnable.db")
#dbLoadRecords("./db/injectionEfficiency.db")
#dbLoadRecords("./db/alSumBR-VAC.db")
#dbLoadRecords("./db/alSumBR-RF.db")
#dbLoadRecords("./db/psAlarms.db")
#dbLoadRecords("./db/psCellAlarms.db")
#dbLoadRecords("./db/iocAdminSoft.db", "IOC=OP-CT{IOC:opsum}")
#dbLoadRecords("./db/BR_BTS_VAC_Sum.db")
#dbLoadRecords("./db/LN_Vac_Alarm_Sum_PVs.db")
#dbLoadRecords("./db/LTB_Vac_Alarm_Sum_PVs.db")
#dbLoadRecords("./db/SR_VacSum.db")
#dbLoadRecords("./db/SR_VacSumShort.db")
#dbLoadRecords("./db/SR_VacSumBM.db")
#dbLoadRecords("./db/SR_VacSumOutlier.db")
#dbLoadRecords("./db/SR_EPS_flow_warn.db")
#dbLoadRecords("./db/SR_EPS_flow_trip.db")
#dbLoadRecords("./db/SR_MG_1wire62.db")
#dbLoadRecords("./db/SR_MG_1wire66.db")
#dbLoadRecords("./db/ahu.db")
#dbLoadRecords("./db/BPMsum.db")
#dbLoadRecords("./db/BPMalarm6.db")
#dbLoadRecords("./db/BPMalarm8.db")
#dbLoadRecords("./db/BPMalarm9.db")
#dbLoadRecords("./db/BPMalarm10.db")
#dbLoadRecords("./db/UPSalarms.db")
#dbLoadRecords("./db/WaterAlarms.db")
#dbLoadRecords("./db/DW-SumAlarm.db")
#dbLoadRecords("./db/DW-AlarmsSub.db")
#dbLoadRecords("./db/ID_Gap_AlarmsSub.db")
#dbLoadRecords("./db/SR_SteamTunnel.db")
#dbLoadRecords("./db/MiscAlarms.db")
#dbLoadRecords("./db/c23_CantPhas.db")
#dbLoadRecords("./db/RTMSmax.db")
#dbLoadRecords("./db/IDmpsSum.db")

# initialize the IOC with Access security control, autosave, caPutLog, etc. 
#</epics/iocs/elauncher/commonInitWithAutoSave.cmd
</epics/iocs/MachineLearn/Init.cmd
