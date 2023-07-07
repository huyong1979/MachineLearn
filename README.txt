This application depends on /epics/iocs/elauncher: it uses bin (dbd, etc.) 
from elauncher.

So, if /epics/iocs/elauncher does not exist, go to /epics/iocs/, then
git clone https://gitlab.nsls2.bnl.gov/accelerator/hla/elauncher.git    
and build elauncher in /epics/iocs (type "make" in /epics/iocs/elauncher)
