#!/epics/iocs/elauncher/bin/linux-x86_64/scriptlaunch

epicsEnvSet("IOCNAME","MachineLearn")
epicsEnvSet("HOSTNAME","physics3")
epicsEnvSet("PWD","/epics/iocs/MachineLearn")

#the line above (#!...) is not a comment: it actually executes the IOC binary  
# load common settings, including conda/python environment 
#</epics/iocs/elauncher/commonSt.cmd
</epics/iocs/MachineLearn/commonSt.cmd

# other environment variable(s), including the person who is in charge
epicsEnvSet("ENGINEER","smithr x7385")

## Load record instances
dbLoadRecords("./db/MLtimes.db")
dbLoadRecords("./db/MLinput.db", "MODE=1time")
dbLoadRecords("./db/MLinput.db", "MODE=live")

dbLoadRecords("./db/MLoutputMAX_03.db")
dbLoadRecords("./db/MLoutputMAX_17.db")
dbLoadRecords("./db/MLoutputMAX_13_23.db", "CELL=13")
dbLoadRecords("./db/MLoutputMAX_13_23.db", "CELL=23")
dbLoadRecords("./db/MLoutputMAX_18_19.db", "CELL=18")
dbLoadRecords("./db/MLoutputMAX_18_19.db", "CELL=19")
dbLoadRecords("./db/MLoutputMAX_default.db", "CELL=01")
dbLoadRecords("./db/MLoutputMAX_default.db", "CELL=02")
dbLoadRecords("./db/MLoutputMAX_default.db", "CELL=04")
dbLoadRecords("./db/MLoutputMAX_default.db", "CELL=05")
dbLoadRecords("./db/MLoutputMAX_default.db", "CELL=06")
dbLoadRecords("./db/MLoutputMAX_default.db", "CELL=07")
dbLoadRecords("./db/MLoutputMAX_default.db", "CELL=08")
dbLoadRecords("./db/MLoutputMAX_default.db", "CELL=09")
dbLoadRecords("./db/MLoutputMAX_default.db", "CELL=10")
dbLoadRecords("./db/MLoutputMAX_default.db", "CELL=11")
dbLoadRecords("./db/MLoutputMAX_default.db", "CELL=12")
dbLoadRecords("./db/MLoutputMAX_default.db", "CELL=14")
dbLoadRecords("./db/MLoutputMAX_default.db", "CELL=15")
dbLoadRecords("./db/MLoutputMAX_default.db", "CELL=16")
dbLoadRecords("./db/MLoutputMAX_default.db", "CELL=20")
dbLoadRecords("./db/MLoutputMAX_default.db", "CELL=21")
dbLoadRecords("./db/MLoutputMAX_default.db", "CELL=22")
dbLoadRecords("./db/MLoutputMAX_default.db", "CELL=24")
dbLoadRecords("./db/MLoutputMAX_default.db", "CELL=25")
dbLoadRecords("./db/MLoutputMAX_default.db", "CELL=26")
dbLoadRecords("./db/MLoutputMAX_default.db", "CELL=27")
dbLoadRecords("./db/MLoutputMAX_default.db", "CELL=28")
dbLoadRecords("./db/MLoutputMAX_default.db", "CELL=29")
dbLoadRecords("./db/MLoutputMAX_default.db", "CELL=30")

dbLoadRecords("./db/MLoutMAX_03.db","MODE=lls")
dbLoadRecords("./db/MLoutMAX_17.db" "MODE=lls")
dbLoadRecords("./db/MLoutMAX_13_23.db", "CELL=13, MODE=lls")
dbLoadRecords("./db/MLoutMAX_13_23.db", "CELL=23, MODE=lls")
dbLoadRecords("./db/MLoutMAX_18_19.db", "CELL=18, MODE=lls")
dbLoadRecords("./db/MLoutMAX_18_19.db", "CELL=19, MODE=lls")
dbLoadRecords("./db/MLoutMAX_default.db", "CELL=01, MODE=lls")
dbLoadRecords("./db/MLoutMAX_default.db", "CELL=02, MODE=lls")
dbLoadRecords("./db/MLoutMAX_default.db", "CELL=04, MODE=lls")
dbLoadRecords("./db/MLoutMAX_default.db", "CELL=05, MODE=lls")
dbLoadRecords("./db/MLoutMAX_default.db", "CELL=06, MODE=lls")
dbLoadRecords("./db/MLoutMAX_default.db", "CELL=07, MODE=lls")
dbLoadRecords("./db/MLoutMAX_default.db", "CELL=08, MODE=lls")
dbLoadRecords("./db/MLoutMAX_default.db", "CELL=09, MODE=lls")
dbLoadRecords("./db/MLoutMAX_default.db", "CELL=10, MODE=lls")
dbLoadRecords("./db/MLoutMAX_default.db", "CELL=11, MODE=lls")
dbLoadRecords("./db/MLoutMAX_default.db", "CELL=12, MODE=lls")
dbLoadRecords("./db/MLoutMAX_default.db", "CELL=14, MODE=lls")
dbLoadRecords("./db/MLoutMAX_default.db", "CELL=15, MODE=lls")
dbLoadRecords("./db/MLoutMAX_default.db", "CELL=16, MODE=lls")
dbLoadRecords("./db/MLoutMAX_default.db", "CELL=20, MODE=lls")
dbLoadRecords("./db/MLoutMAX_default.db", "CELL=21, MODE=lls")
dbLoadRecords("./db/MLoutMAX_default.db", "CELL=22, MODE=lls")
dbLoadRecords("./db/MLoutMAX_default.db", "CELL=24, MODE=lls")
dbLoadRecords("./db/MLoutMAX_default.db", "CELL=25, MODE=lls")
dbLoadRecords("./db/MLoutMAX_default.db", "CELL=26, MODE=lls")
dbLoadRecords("./db/MLoutMAX_default.db", "CELL=27, MODE=lls")
dbLoadRecords("./db/MLoutMAX_default.db", "CELL=28, MODE=lls")
dbLoadRecords("./db/MLoutMAX_default.db", "CELL=29, MODE=lls")
dbLoadRecords("./db/MLoutMAX_default.db", "CELL=30, MODE=lls")

dbLoadTemplate("./db/MLoutput.substitutions")
dbLoadTemplate("./db/MLout.substitutions")

dbLoadTemplate("./db/MLRun.substitutions")
dbLoadRecords("./db/MLWireData.db")
dbLoadRecords("./db/MLMisc.db")

# initialize the IOC with Access security control, autosave, caPutLog, etc. 
#</epics/iocs/elauncher/commonInitWithAutoSave.cmd
</epics/iocs/MachineLearn/Init.cmd
