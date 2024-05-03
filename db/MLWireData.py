# generate MLmisc.db
# record(waveform, "SR:C01-MTM{1wire:33}T-I_Wf_") {
#    field(DESC,"archived data")
#    field(NELM,"4032")
#    field(FTVL,"DOUBLE")
#    field(EGU, "Celsius")
#    field(PREC, "1")
#}
with open('MLWireData.db', 'w') as fd:
  fd.write('record(waveform, "SR-OPS{}Mode-Sts_Wf") {\n')
  fd.write('    field(DESC,"OP Status")\n')
  #fd.write('    field(NELM,"17280")\n')
  fd.write('    field(NELM,"207360")\n')
  fd.write('    field(FTVL,"UCHAR")\n')
  fd.write('}\n')

  for cell in range(1, 31):
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

    for n_wire in n_wires:
            #fd.write(f'record(waveform, "SR:C{C:02d}-MTM'+'{1wire:'+f'{N:02d}'+'}T-I_Wf_")\n')
            fd.write('record(waveform, "SR:C%02d-MTM{1wire:%02d}T-I_Wf_") {\n'%(cell, n_wire))
            fd.write('    field(DESC,"resampled history data")\n')
            fd.write('    field(NELM,"207360")\n')
            fd.write('    field(FTVL,"DOUBLE")\n')
            fd.write('    field(EGU, "Celsius")\n')
            fd.write('}\n')

            fd.write('record(waveform, "SR:C%02d-MTM{1wire:%02d}T-I_Wf") {\n'%(cell, n_wire))
            fd.write('    field(DESC,"stitched data")\n')
            fd.write('    field(NELM,"207360")\n')
            fd.write('    field(FTVL,"DOUBLE")\n')
            fd.write('    field(EGU, "Celsius")\n')
            fd.write('}\n')

