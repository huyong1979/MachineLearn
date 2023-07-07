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
dbLoadTemplate("./db/MLrun.substitutions")

# initialize the IOC with Access security control, autosave, caPutLog, etc. 
#</epics/iocs/elauncher/commonInitWithAutoSave.cmd
</epics/iocs/MachineLearn/Init.cmd
