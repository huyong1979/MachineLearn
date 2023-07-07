#autosave
#dbLoadRecords("$(EPICS_BASE)/db/save_restoreStatus.db", "P=OP-CT{IOC:$(IOCNAME)}")
#save_restoreSet_status_prefix("OP-CT{IOC:$(IOCNAME)}")
set_savefile_path("${PWD}/as","/save")
set_requestfile_path("${PWD}/as","/req")
system("install -m 777 -d ${PWD}/as/save")
system("install -m 777 -d ${PWD}/as/req")
# 3 types of info node: autosaveFields_pass0, autosaveFields_pass1, autosaveFields
set_pass0_restoreFile("settings_pass0.sav")
set_pass1_restoreFile("settings_pass1.sav")
set_pass1_restoreFile("settings.sav")

# Access security control 
#asSetFilename("/cf-update/acf/default.acf")

# IOC initialization
iocInit()

# Log when, where and who changed PV values
#caPutLogInit("ioclog.cs.nsls2.local:7004", 1)

# dump PVs to a file
dbl > /cf-update/$(HOSTNAME).$(IOCNAME).dbl

#autosave
makeAutosaveFileFromDbInfo("${PWD}/as/req/settings_pass0.req", "autosaveFields_pass0")
create_monitor_set("settings_pass0.req", 15, "")
makeAutosaveFileFromDbInfo("${PWD}/as/req/settings_pass1.req", "autosaveFields_pass1")
create_monitor_set("settings_pass1.req", 15, "")
makeAutosaveFileFromDbInfo("${PWD}/as/req/settings.req", "autosaveFields")
create_monitor_set("settings.req", 15, "")

