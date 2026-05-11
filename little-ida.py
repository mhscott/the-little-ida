import openseespy.opensees as ops
import matplotlib.pyplot as plt

g = 386.4

W = 500
m = W/g
Tn = 1.0
wn = 2*3.14159/Tn
k = m*wn**2
Fy = 300

ops.wipe()
ops.model('basic','-ndm',1,'-ndf',1)

ops.node(1,0); ops.fix(1,1)
ops.node(2,0); ops.mass(2,m)

ops.timeSeries('Path',1,'-dt',0.02,'-filePath','tabasFN.txt','-factor',g)

ops.uniaxialMaterial('Hardening',1,k,Fy,0,0)

ops.element('zeroLength',1,1,2,'-mat',1,'-dir',1)

ops.analysis('Transient','-noWarnings')


Tf = 40.0
dt = 0.01
Nsteps = int(Tf/dt)

Uplot = []
gmPlot = []

dgm = 0.05
gmFact = 0.0
while gmFact < 2.0:

    gmFact += dgm
    gmPlot.append(gmFact)

    ops.remove('loadPattern',1)

    ops.reset()

    ops.pattern('UniformExcitation',1,1,'-accel',1,'-factor',gmFact)

    Umax = 0
    for i in range(Nsteps):
        ops.analyze(1,dt)
        U = ops.nodeDisp(2,1)
        if abs(U) > Umax:
            Umax = abs(U)

    Uplot.append(Umax)

plt.subplot(2,2,1)
plt.plot(Uplot,gmPlot,'-k')
plt.xlim(left=0)
plt.ylim(bottom=0)
plt.xlabel('Displacement (in)')
plt.ylabel('Scale Factor')
plt.grid()

plt.tight_layout()
plt.savefig('little-ida.png',bbox_inches='tight')
