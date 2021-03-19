#!/bin/bash
for dcp in -1 -0.8 -0.6 -0.4 -0.2 0 0.2 0.4 0.6 0.8 1.0
#for dcp in 0
do
  dcpstring=${dcp/"-"/"m"}
  dcpstring=${dcpstring/"."/"p"}
  python3 PrintValues.py --Variable LoE,1000,0.,30000. -f 1,0,1,1,1,2 --DeltaCP ${dcp} -o output_LoE_0_to_30000_dcp_${dcpstring}
  python Draw.py -i output_LoE_0_to_30000_dcp_${dcpstring}.py -o output_LoE_0_to_30000_dcp_${dcpstring}
done
