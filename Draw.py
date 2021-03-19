import tdrstyle,ROOT
from array import array
import numpy as np

def IntToFlavString(iflav):
  if iflav==0:
    return 'e'
  elif iflav==1:
    return '#mu'
  elif iflav==2:
    return '#tau'
  else:
    return ''

## Arguments
import argparse
parser = argparse.ArgumentParser(description='intput filename')
parser.add_argument('-i',dest='inputName',default='intput filename')
parser.add_argument('-o',dest='outputName',default='output')
args = parser.parse_args()

exec('from %s import *'%(args.inputName.replace('.py','')))

tdrstyle.setTDRStyle()

c1 = ROOT.TCanvas('c1', '', 1200, 800)
c1.SetRightMargin(0.3)
c1.cd()

drawMode = -1
list_xaxis = []
xtitle = ''
if len(list_LoE)!=0:
  drawMode = 0
  list_xaxis = list_LoE
  xtitle = 'L/E (km/GeV)'
elif len(list_E)!=0:
  drawMode = 1
  list_xaxis = list_E
  xtitle = 'E (GeV)'

h_dummy = ROOT.TH1D('h_dummy', '', len(list_xaxis)-1, array("d",list_xaxis))
h_dummy.GetXaxis().SetTitle(xtitle)
h_dummy.GetYaxis().SetRangeUser(0., 1.3)
h_dummy.GetYaxis().SetTitle("Probability")
h_dummy.Draw('histsame')
h_dummy.GetXaxis().SetLabelSize(0.030)

Colors = [
ROOT.kBlack,
ROOT.kRed,
ROOT.kBlue,
ROOT.kGreen,
]

gr_dict = dict()
lg = ROOT.TLegend(0.25, 0.8, 0.5, 0.93)
lg.SetNColumns(2) 
for iflav in range(0, len(flav_is)):
  gr_Prob = ROOT.TGraph(len(list_xaxis), array("d", list_xaxis), array("d", list_Probs[iflav]))
  gr_Prob.SetLineColor(Colors[iflav])
  gr_dict[iflav] = gr_Prob
  gr_Prob.Draw('lsame')

  lg.AddEntry( gr_Prob, '#font[42]{'+IntToFlavString(flav_is[iflav])+'#rightarrow'+IntToFlavString(flav_fs[iflav])+'}', 'l' )

lg.Draw()

## Parameters
from math import pi
tL = ROOT.TLatex()
tL.SetNDC()
tL.SetTextSize(0.04)

tlatexsToDraw = [
"#font[42]{sin#theta^{2}_{12}="+ ( "%.2e}"%(pow( np.sin(Theta_12),2 )) ).replace('e','#times10^{')+'}',
"#font[42]{sin#theta^{2}_{23}="+ ( "%.2e}"%(pow( np.sin(Theta_23),2 )) ).replace('e','#times10^{')+'}',
"#font[42]{sin#theta^{2}_{13}="+ ( "%.2e}"%(pow( np.sin(Theta_13),2 )) ).replace('e','#times10^{')+'}',
"#font[42]{#Delta m^{2}_{12}="+ ( "%.2e}"%( m2_12 ) ).replace('e','#times10^{')+' eV^{2}}',
"#font[42]{#Delta m^{2}_{32}="+ ( "%.2e}"%( m2_32 ) ).replace('e','#times10^{')+' eV^{2}}',
"#font[42]{%sH}"%(massHierarchy),
"#font[42]{#delta_{CP}=%1.1f#pi}"%(DeltaCP),
]

if drawMode==1:
  tlatexsToDraw.append( "#font[42]{L=%1.3f km}"%(Linput) )

tlYTop = 0.91
dtlY = 0.07
for tlatex in tlatexsToDraw:
  print tlatex
  tL.DrawLatex(0.75, tlYTop, tlatex)
  tlYTop -= dtlY

c1.SaveAs(args.outputName+'.pdf')

