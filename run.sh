#!/bin/bash
for dcp in -1 -0.8 -0.6 -0.4 -0.2 0 0.2 0.4 0.6 0.8 1.0
do
  dcpstring=${dcp/"-"/"m"}
  dcpstring=${dcpstring/"."/"p"}

  ## NH
  python3 PrintValues.py --Variable LoE,1000,0.,30000. -f 1,0,1,1,1,2 --DeltaCP ${dcp} -o output_LoE_0_to_30000_dcp_${dcpstring}_NH
  python Draw.py -i output_LoE_0_to_30000_dcp_${dcpstring}_NH.py -o output_LoE_0_to_30000_dcp_${dcpstring}_NH
  ## IH
  python3 PrintValues.py --Variable LoE,1000,0.,30000. -f 1,0,1,1,1,2 --DeltaCP ${dcp} -o output_LoE_0_to_30000_dcp_${dcpstring}_IH --hierarchy "I"
  python Draw.py -i output_LoE_0_to_30000_dcp_${dcpstring}_IH.py -o output_LoE_0_to_30000_dcp_${dcpstring}_IH

done
