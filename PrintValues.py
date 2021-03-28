import numpy as np

## Arguments
import argparse
parser = argparse.ArgumentParser(description='L in kilometer, E in GeV')
parser.add_argument('--Variable',dest='Variable',
help='1) If L/E, put LoE,nbin,min,max 2) If E, put E,nbin,min,max,L 3) If L, put L,nbin,min,max,E')
parser.add_argument('-f',dest='Flavors',help='e=0/m=1/t=2, and put 0,1 if you want e to mu probability. You can put multiples; 0,1,0,0')
parser.add_argument('-o',dest='outputName',default='output')
parser.add_argument('--hierarchy',dest='hierarchy',default='N',help='N for normal, I for inveted')
parser.add_argument('--DeltaCP',dest='DeltaCP',default='0',help='DeltaCP/PI')
parser.add_argument('--Params',dest='Params',default='params_Default.py', help='python file which contains oscillation parameter values')
args = parser.parse_args()

## Parse args.Variable
drawMode = -1 # 0 : L/E, 1 : E, 2 : L
words_Variable = args.Variable.split(',')
if words_Variable[0]=='LoE':
  drawMode = 0
elif words_Variable[0]=='E':
  drawMode = 1
elif words_Variable[0]=='L':
  drawMode = 2
else:
  print('## Wrong Variable')
  exit()
## Parse args.Flavors
words_Flavors = args.Flavors.split(',')
if len(words_Flavors)%2!=0:
  print('## Wrong Flavors')
flav_is = []
flav_fs = []
for i in range(0,int(len(words_Flavors)/2)):
  flav_i = int(words_Flavors[2*i])
  flav_f = int(words_Flavors[2*i+1]) 
  print('Calculating %d -> %d'%(flav_i, flav_f))
  flav_is.append(flav_i)
  flav_fs.append(flav_f)

## Parameters

exec('from %s import *'%(args.Params.replace('.py','')))

## 12
S2_12 = S2_12__
m2_12 = m2_12__
Theta_12 = np.arcsin( np.sqrt(S2_12) )

## 23
S2_23 = S2_23_NH__
m2_32 = m2_32_HN__
if args.hierarchy=='I':
  S2_23 = S2_23_IH__
  m2_32 = m2_32_IN__
Theta_23 = np.arcsin( np.sqrt(S2_23) )

## 13
S2_13 = S2_13__
Theta_13 = np.arcsin( np.sqrt(S2_13) )

from math import pi
DeltaCP = float(args.DeltaCP)*pi ## Radian

print('''## Parameters :
## Theta_12 = %1.3f
## Theta_23 = %1.3f
## Theta_13 = %1.3f
## m_12^2 = %.3e eV2
## m_32^2 = %.3e eV2
'''%(Theta_12, Theta_23, Theta_13, m2_12, m2_32)
)

M23 = np.zeros( (3,3), dtype=complex)
M13 = np.zeros( (3,3), dtype=complex)
M12 = np.zeros( (3,3), dtype=complex)

def C(t):
  return np.cos(t)
def S(t):
  return np.sin(t)

M23[0,0] = 1.
M23[1,1] = C(Theta_23)
M23[1,2] = S(Theta_23)
M23[2,1] = -S(Theta_23)
M23[2,2] = C(Theta_23)

M13[0,0] = C(Theta_13)
M13[0,2] = S(Theta_13)*np.exp(-1j*DeltaCP)
M13[1,1] = 1.
M13[2,0] = -S(Theta_13)*np.exp(1j*DeltaCP)
M13[2,2] = C(Theta_13)

M12[0,0] = C(Theta_12)
M12[0,1] = S(Theta_12)
M12[1,0] = -S(Theta_12)
M12[1,1] = C(Theta_12)
M12[2,2] = 1.

print('## M23 = '),
print(M23)
print('## M13 = '),
print(M13)
print('## M12 = '),
print(M12)

U = np.matmul( M23, np.matmul(M13,M12) )

print('## U = '),
print(U)

def MassSquared(i,j):
  if i==j:
    return 0
  elif (i==0 and j==1) or (i==1 and j==0):
    return m2_12
  else:
    return m2_32

def NeutrinoMixingProb(alpha, beta, LoE):

  # L : meter
  # E : MeV

  mixprob = 1 if (alpha==beta) else 0 # delta

  for i in range(0,2):
    for j in range(i+1,3):

      Mabij = np.conjugate( U[alpha,i] ) * U[beta,i] * U[alpha,j] * np.conjugate( U[beta,j] )
      Xij = 1.267 * MassSquared(i,j) * LoE

      term1 = -4.*np.real( Mabij ) * pow(np.sin(Xij), 2)
      term2 = 2.*np.imag( Mabij ) * np.sin( 2*Xij )

      #print('(i,j,Mij2) = (%d,%d,%.2e) -> L/E =  %.2e, term1 = %.2e, term2 = %.2e'%(i,j,MassSquared(i,j),LoE,term1,term2))

      mixprob += term1
      mixprob += term2


  return mixprob


list_LoE = []
list_E = []
list_L = []
list_Probs = []
Linput = -1
Einput = -1

if drawMode==0:

  nLoE = int(words_Variable[1])
  LoEmin = float(words_Variable[2])
  LoEmax = float(words_Variable[3])
  dLoE = (LoEmax-LoEmin)/float(nLoE)

  for ifalv in range(0,len(flav_is)):

    list_Prob = []

    flav_i = flav_is[ifalv]
    flav_f = flav_fs[ifalv]

    for iLoE in range(0,nLoE):
      LoE = LoEmin + float(iLoE) * dLoE
      if ifalv==0:
        list_LoE.append(LoE)
      list_Prob.append( NeutrinoMixingProb(flav_i, flav_f, LoE) )

    list_Probs.append(list_Prob)

elif drawMode==1:

  nE = int(words_Variable[1])
  Emin = float(words_Variable[2])
  Emax = float(words_Variable[3])
  dE = (Emax-Emin)/float(nE)
  Linput = float(words_Variable[4])

  for ifalv in range(0,len(flav_is)):

    list_Prob = []

    flav_i = flav_is[ifalv]
    flav_f = flav_fs[ifalv]

    for iE in range(0,nE):
      this_E = Emin + float(iE) * dE
      if this_E==0:
        continue
      if ifalv==0:
        list_E.append(this_E)
      list_Prob.append( NeutrinoMixingProb(flav_i, flav_f, Linput/this_E) )

    list_Probs.append(list_Prob)

out = open(args.outputName+'.py','w')

out.write('''Theta_12 = %1.3f
Theta_23 = %1.3f
Theta_13 = %1.3f
m2_12 = %.3e
m2_32 = %.3e
'''%(Theta_12, Theta_23, Theta_13, m2_12, m2_32)
)


out.write('massHierarchy = "%s"\n'%(args.hierarchy))
out.write('Linput = %f\n'%(Linput))
out.write('Einput = %f\n'%(Einput))
out.write('DeltaCP = %s # should be multiplied by pi to get values in radian\n'%(args.DeltaCP))

out.write('flav_is = [')
for e in flav_is:
  out.write('%d,'%(e))
out.write(']\n')

out.write('flav_fs = [')
for e in flav_fs:
  out.write('%d,'%(e))
out.write(']\n')

out.write('list_LoE = [')
for e in list_LoE:
  out.write('%f,'%(e))
out.write(']\n')

out.write('list_E = [')
for e in list_E:
  out.write('%f,'%(e))
out.write(']\n')

out.write('list_Probs = [\n')
for list_Prob in list_Probs:
  out.write('  [')
  for e in list_Prob:
    out.write('%.3e,'%(e))
  out.write('],\n')
out.write(']\n')


