# coding=utf-8
import random as rnd
import numpy as np
import cmath
import matplotlib
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

#plot settings
params = {
    'figure.figsize'    : [10, 7.5],
    'text.usetex'       : True,
    'legend.fontsize'   : 12
}
matplotlib.rcParams.update(params)


def round_complex(x,precision=0):
    return complex(round(x.real,precision),round(x.imag,precision))

def entangle(tauA,tauB,gamma):
    
    # Den tau werden ihre Entscheidungswinkel (theta, phi) zugeordnet.
    # Klassische Strategien liegen zwischen 0 <= tau <= 1
    # und Quantenstrategien zwischen       -1 <= tau <  0
    if tauA >= 0.0 and tauA <= 1.0:
        thetaA=tauA*cmath.pi
        phiA=0.0
    elif tauA < 0.0 and tauA >= -1.0:
        thetaA=0.0
        phiA=tauA*cmath.pi/2.0
    else:
        print("tauA needs to be between [-1,1]")
    if tauB >= 0.0 and tauB <= 1.0:
        thetaB=tauB*cmath.pi
        phiB=0.0
    elif tauB < 0.0 and tauB >= -1.0:
        thetaB=0.0
        phiB=tauB*cmath.pi/2.0
    else:
        print("tauB needs to be between [-1,1]")
        
    # Basisvektoren des vierdimensionalen Hilbertraums
    AB = np.array([
        [1.0,0.0,0.0,0.0],  # A1B1
        [0.0,-1.0,0.0,0.0], # A1B2
        [0.0,0.0,-1.0,0.0], # A2B1
        [0.0,0.0,0.0,1.0]
        ])
        
    # Die nachfolgenden Operatoren werden mittels interner Python-Funktionen
    # initialisiert deren Implementierung derart ist dass sie für entsprechende
    # Variablen einen Wert ungleich 0 erzeugen. Um dies zu vermeiden, runden 
    # wir auf eine bestimmte Nachkommastelle, da der hierdurch verursachte Fehler
    # aufgrund der geringen Zahl an aufeinander folgenden Rechenoperationen
    # im Endergebnis von vernachlaessigbarer Groessenordung ist.
    precision = 10
    
    # Entscheidungsoperatoren der Spieler
    UA = [[round_complex(cmath.exp(phiA*1j)*cmath.cos(thetaA/2.0),precision), round_complex(-cmath.sin(thetaA/2.0),precision)],
          [round_complex(cmath.sin(thetaA/2.0),precision), round_complex(cmath.exp(-phiA*1j)*cmath.cos(thetaA/2.0),precision)]]
    UB = [[round_complex(cmath.exp(phiB*1j)*cmath.cos(thetaB/2.0),precision), round_complex(-cmath.sin(thetaB/2.0),precision)],
          [round_complex(cmath.sin(thetaB/2.0),precision), round_complex(cmath.exp(-phiB*1j)*cmath.cos(thetaB/2.0),precision)]]

    
    # Gemeinsamer 4x4 Entscheidungsoperator
    UA_T_UB = np.array([
        [UA[0][0]*UB[0][0],UA[0][0]*UB[0][1],UA[0][1]*UB[0][0],UA[0][1]*UB[0][1]],
        [UA[0][0]*UB[1][0],UA[0][0]*UB[1][1],UA[0][1]*UB[1][0],UA[0][1]*UB[1][1]],
        [UA[1][0]*UB[0][0],UA[1][0]*UB[0][1],UA[1][1]*UB[0][0],UA[1][1]*UB[0][1]],
        [UA[1][0]*UB[1][0],UA[1][0]*UB[1][1],UA[1][1]*UB[1][0],UA[1][1]*UB[1][1]]
        ])
    
    # Verschränkungsoperator
    J_gamma = np.array([
        [round_complex(cmath.cos(gamma/2.0),precision),0j,0j,round_complex(cmath.sin(gamma/2.0)*1j,precision)],
        [0j,round_complex(cmath.cos(gamma/2.0),precision),round_complex(-cmath.sin(gamma/2.0)*1j,precision),0j],
        [0j,round_complex(-cmath.sin(gamma/2.0)*1j,precision),round_complex(cmath.cos(gamma/2.0),precision),0j],
        [round_complex(cmath.sin(gamma/2.0)*1j,precision),0j,0j,round_complex(cmath.cos(gamma/2.0),precision)]
        ])
    J_gamma_dagger = np.array([
        [round_complex(cmath.cos(gamma/2.0),precision),0j,0j,round_complex(-cmath.sin(gamma/2.0)*1j,precision)],
        [0j,round_complex(cmath.cos(gamma/2.0),precision),round_complex(cmath.sin(gamma/2.0)*1j,precision),0j],
        [0j,round_complex(cmath.sin(gamma/2.0)*1j,precision),round_complex(cmath.cos(gamma/2.0),precision),0j],
        [round_complex(-cmath.sin(gamma/2.0)*1j,precision),0j,0j,round_complex(cmath.cos(gamma/2.0),precision)]
        ])
    
    # Berechnung des verschraenkten Endzustand des Spiels und den daraus
    # resultierenden Wahrscheinlichkeiten der Strategiekombinationen
    psi = np.matmul(J_gamma_dagger,np.matmul(UA_T_UB,np.matmul(J_gamma,AB[0])))
    probs = [
        abs(np.matmul(AB[0],psi))**2,
        abs(np.matmul(AB[1],psi))**2,
        abs(np.matmul(AB[2],psi))**2,
        abs(np.matmul(AB[3],psi))**2
        ]
    
    return probs
    
# Auszahlung für gemischte Strategien 
def mixed_payment(tauA,tauB,gamma,a,b,c,d):
    probs = entangle(tauA,tauB,gamma)
    return a*probs[0] + b*probs[1] + c*probs[2] + d*probs[3]

# Wahl der reinen Strategien im Quantenspiel
def choose(tauA,tauB,gamma):
    probs = entangle(tauA,tauB,gamma)
    normierung = sum(probs)
    probs[:] /= normierung
    choice = rnd.random()
    if choice <= probs[0]:
        return [0, 0]
    elif choice > probs[0] and choice <= probs[0] + probs[1]:
        return [0, 1]
    elif choice > probs[0] + probs[1] and choice <= probs[0] + probs[1] + probs[2]:
        return [1, 0]
    elif choice > probs[0] + probs[1] + probs[2] and choice <= 1.0:
        return [1, 1]
    else:
        print("Fehler bei Auszahlung nach Kollaps des Quantenzustandes.")
    
    



# Der folgende Test demonstriert, dass bis hierhin richtig gerechnet wurde:

# Parameter für dominantes Spiel
a=10
b=12
c=4
d=5

# Verschraenkung
gamma=0.0#cmath.pi/2

N=100

tauA = np.linspace(-1.0,1.0,N)
tauB = np.linspace(-1.0,1.0,N)

TA, TB = np.meshgrid(tauA,tauB)

AusA=np.zeros([N,N])

for m in range(0,N):
    for n in range(0,N):
        AusA[m][n] = auszahlung(tauA[m],tauB[n],gamma,a,b,c,d)

fig = plt.figure()
ax = plt.axes(projection='3d')
ax.plot_surface(TA, TB, AusA, rstride=1, cstride=1,cmap='viridis',edgecolor='none')
ax.set_xlabel(r'$\tau_A$')
ax.set_ylabel(r'$\tau_B$')
ax.set_zlabel(r'$\textdollar$');
#saveFig="./dominantes.jpg"
#plt.savefig(saveFig, dpi=200,bbox_inches="tight",pad_inches=0.05,format="jpg")
plt.show()
#plt.gcf().clear()
