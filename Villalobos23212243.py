"""
Práctica 3: Modelado y control del sistema musculoesquelético

Departamento de Ingeniería Eléctrica y Electrónica, Ingeniería Biomédica
Tecnológico Nacional de México [TecNM - Tijuana]
Blvd. Alberto Limón Padilla s/n, C.P. 22454, Tijuana, B.C., México

Nombre del alumno: Emiliano Villalobos García
Número de control: 23212243
Correo institucional: l23212243@tectijuana.edu.mx

Asignatura: Modelado de Sistemas Fisiológicos
Docente: Dr. Paul Antonio Valle Trujillo; paul.valle@tectijuana.edu.mx
"""
# Instalar librerias en consola
# pip install numpy control matplotlib

#Librerias
import numpy as np
import control as ctrl 
import matplotlib.pyplot as plt

#Datos generales de la simulacion
x0,t0,tend,dt,w,h = 0,0,10,1E-3,7,3.5
N = round(tend/dt)+1
t = np.linspace (t0,tend,N)
u = np.zeros(N); u[round(1/dt) : round(2/dt)] = 1

def musculo(alpha,Cs,Cp,R):
    num = [R*Cs,1-alpha]
    den = [R*(Cp+Cs),1]
    sys = ctrl.tf(num,den)
    L = np.roots(den)
    return sys,L

#Función de transferencia: Control
alpha,Cs,Cp,R = 0.25,10E-6,100E-6,100
sysctrl, L = musculo(alpha,Cs,Cp,R)
print(f'Función de transferencia del control: {sysctrl}')
print(f"Polo del sistema: L1 = {L[0]:.3e}\n")

#Función de transferencia: Caso
alpha,Cs,Cp,R = 0.25,10E-6,100E-6,10E3
syscaso, L = musculo(alpha,Cs,Cp,R)
print(f'Función de transferencia del caso: {syscaso}')
print(f"Polo del sistema: L1 = {L[0]:.3e}\n")

# Respuestas en lazo abierto
_,Fsx = ctrl.forced_response(sysctrl,t,u,x0)
_,Fsy = ctrl.forced_response(syscaso,t,u,x0)

def controlador(kP,kI,kD,sys):
    Cr = 1e-6
    Re = 1/(kI*Cr)
    Rr = kP*Re
    Ce = kD/Rr
    numPID = [Re*Rr*Ce*Cr,(Re*Ce + Rr*Cr),1]
    denPID = [Re*Cr,0]
    PID = ctrl.tf(numPID,denPID)
    sysPID = ctrl.feedback(ctrl.series(PID,sys),1,sign=-1)
    return sysPID

casoPID = controlador(477.1555564974,1204530.19400615,0.00626997867136255,syscaso)
print(f'Función de transferencia del caso en lazo cerrado: {casoPID}')

# Respuesta del sistema de control en lazo cerrado
_,PIDy = ctrl.forced_response(casoPID,t,Fsx,x0)

clr1 = np.array([46, 41, 16])/255
clr2 = np.array([44, 87, 69])/255
clr3 = np.array([235, 227, 167])/255
clr4 = np.array([166, 77, 55])/255

fg = plt.figure()
fg.set_size_inches(w,h)
plt.rcParams['font.size'] = 11
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman']
plt.plot(t,u,'-',color=clr4,label='F(t)')
plt.plot(t,Fsx,'-',color=clr1,label='Fs(t): Control')
plt.plot(t,Fsy,'--',color=clr2,label='Fs(t): Caso')
plt.plot(t,PIDy,':',linewidth=2.5,color=clr3,label='PID(t): Tratamiento')
plt.xlim(0,10); plt.xticks(np.arange(0,11,1))
plt.ylim(-0.1,1.1); plt.yticks(np.arange(-0.1,1.2,0.1))
plt.xlabel('t [s]')
plt.ylabel('Fi(t) [V]')
plt.legend(bbox_to_anchor=(0.5,-0.25),loc='center',ncol=4,frameon=False)
plt.show()
fg.savefig('caso_python.pdf',bbox_inches='tight')