from random import expovariate as exponential
from SimPy.Simulation import *
from funciones import Scheduler as INDEX, leer_informacion

class Llegada_Pacientes(Process) :
    def Llegar(self) : 
        
        with open("n_comunes/g_tiempo_hasta_otro_paciente.txt","a") as document:
            while True : 
                hora,  dia = INDEX.hora(now()),   INDEX.dia(now())
                t_llegada = tasas[hora][dia]          
                tiempo = exponential((t_llegada/60))     
                document.write("{}\n".format(tiempo))             
                yield hold,  self,  tiempo



probabilidades,  tasas = leer_informacion()
for i in range(3000):
    initialize()
    l = Llegada_Pacientes()
    activate(l, l.Llegar())
    dias_transiente = 14
    dia_extra = 0
    dias_a_simular = 31
    simulate(until=(dias_transiente+dias_a_simular+dia_extra)*24*60)