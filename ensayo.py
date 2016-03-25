from SimPy.Simulation import *
from random import expovariate as exponential,  triangular,  uniform
from cambiar_formato import cambiar
from borrar import borrar_transiente

from funciones import (ID, Scheduler as INDEX, leer_informacion, get_color, f_amarillo, f_azul, 
                        f_naranja, f_rojo, f_verde, ResCer, ScannC, RadiogT, bording_time,  
                        prob_hospitalizacion, tiempos_examen, prob_imagen, get_tipo_im, prob_laboratorio,
                        tiempo_medico_atencion, cola_promedio, prob_doble, tiempo_triage, tiempo_medico_FT,
                        tiempo_espera_enfermera, get_se_hospitaliza, tiempos_examenes_1, tiempos_examenes_2,
                        doble_examen, tiempo_hasta_otro_paciente, fast_amarillo, uniforme_hospitalizacion)


import time
start_time = time.time()

#from Script_Eliminar_Reportes import crear
import scipy.stats as st
from scipy import mean
import matplotlib.pyplot as plt

from numpy import isnan
def nan_to_numero(array):
    #print(array)
    return [0 if isnan(a) else a for a in array]

"""

SIEMPRE LEER EL MAIN PRIMERO

Dudas :  FastTrack
¿en qué influyen las camas?

Cada vez que dice "self" se hace referencia a una instancia de la CLASE donde se está diciendo self

"""




"""
Esta llamada crea un archivo con la copia de este 
pero con código más corto ya que elimina todas las
opciones de reporte 
"""
#crear("Main - CORRER ESTE")


"""
Aquí se escribe un comentario de la corrida por si al 
imprimir el reporte queremos dejar registro de alguna
característica en especial de la corrida
"""
COMENTARIO = ""


"""
Estos margenes es por si queremos monitorear tiempos 
entre eventos que estén entre esos maargenes
"""


class Paciente(Process) : 
    """
    Proceso que simula el comportamiento de cada Paciente
    """

    def __init__(self,  color) : 
        Process.__init__(self)
        self.id = next(ID.paciente)
        self.color = color
        self.medico = None
        self.tiempo_entra_a_cola = -1
        self.t_esperando = 0
        self.atendido = None
        self.condicion_de_salud = 0         #este valor es para poder determinar más tarde a qué paciente 
        self.tiempo_entra_box = -1                                   #dejar salir si es que se necesita un box para un paciente rojo
        self.tiempo_entra_box_ft = -1
        self.quiere_hospital = False
        self.examenes_realizados = []
        self.esperando_doc = False

        self.esperandoft = False
        self.esperandomed = False

        self.boxft = SimEvent()
        self.medft = SimEvent()

        self.en_bording_time = False
        self.entra_a_bording_time = 0

        self.es_fastrack = False

        self.Triageado = False

    def Entrar_a_Emergencia_FT(self, permitido = False):
        #if arg:
        #print("parte")

        if not self.Triageado:
            if len(Triage.waitQ)>=5 and Triage.n==1 : 
                Triage.n=2
            elif len(Triage.waitQ)<=1 and Triage.n==2 : 
                Triage.n=1
            if dias_transiente*24*60<=now()<=(dias_a_simular+dias_transiente)*24*60 and INDEX.dia(now()) in dias_monitoreados:
                monitor_Triage.tally(int(Triage.n==1))
            yield request, self, Triage
            if REPORTEAR :
                reporte.append("{} Entra a Triage {}".format(self, now()))
            yield hold,  self,  tiempo_triage() 
            yield release,  self,  Triage
            if REPORTEAR :
                reporte.append("{} Sale de Triage {}".format(self,now()))
            self.Triageado = True

        #print(BoxFT.n, proceso_fastt.hay_FastTrack)
        if not proceso_fastt.hay_FastTrack and not permitido:
            self.es_fastrack = False
            cola_por_box.append(self)

        else:

            if REPORTEAR :
                reporte.append("{} Entra a cola por box Fast-Track {}".format(self,now()))


            if dias_transiente*24*60<=now()<=(dias_a_simular+dias_transiente)*24*60 and INDEX.dia(now()) in dias_monitoreados and self.tiempo_entra_a_cola<0:
                monitor_cola.observe(len(cola_por_box)+len(cola_por_box.rojos)+len(BoxFT.waitQ)+1)

            if self.tiempo_entra_a_cola < 0:
                self.tiempo_entra_a_cola = now()

            self.experandoft = True
            proceso_fastt.cola.append(self)
            yield request, self, BoxFT
         #print(INDEX.dia(now()),INDEX.hora(now()), len(BoxFT.waitQ), len(cola_por_box))
            proceso_fastt.cola.remove(self)
            self.esperandoft = False
            

            self.tiempo_entra_box = now()
            if dias_transiente*24*60<=now()<=(dias_a_simular+dias_transiente)*24*60:
                personas_por_hora[INDEX.dia(now())][self.color]+=1
            
            if dias_transiente*24*60<=now()<=(dias_a_simular+dias_transiente)*24*60 and INDEX.dia(now()) in dias_monitoreados and INDEX.dia(now()) in dias_monitoreados:
                monitor_cola.observe(len(cola_por_box)+len(cola_por_box.rojos)+len(BoxFT.waitQ))
                dif_de_tiempo = self.tiempo_entra_box-self.tiempo_entra_a_cola
                tiempo_hasta_box.observe(dif_de_tiempo)
                tiempos_por_color[self.color].observe(dif_de_tiempo)
                proporciones[self.color].observe(int(dif_de_tiempo<optimo[self.color]))
                proporciones_total.observe(int(dif_de_tiempo<optimo[self.color]))
                #print(proporciones_total)

            if REPORTEAR :
                reporte.append("{} Entra a box Fast-Track {}".format(self,now()))

            proceso_fastt.cola_medico.append(self)
            yield request, self, MedFT
            proceso_fastt.cola_medico.remove(self)

            proceso_fastt.atendiendose.append(self)
            yield hold, self, tiempo_medico_FT()
            proceso_fastt.atendiendose.remove(self)


            yield release, self, MedFT
            #print("\na",BoxFT.capacity, self, INDEX.hora(now()), len(BoxFT.waitQ), len(proceso_fastt.cola))
            yield release, self, BoxFT
            #print("b",BoxFT.capacity, self, INDEX.hora(now()), len(BoxFT.waitQ), len(proceso_fastt.cola))

            if proceso_fastt.disminuir_medicos > 0:
                proceso_fastt.disminuir_medicos-=1
                MedFT.n-=1

            if proceso_fastt.disminuir_box > 0:
                BoxFT.n-=1
                proceso_fastt.disminuir_box-=1
                

            #print("dia:",INDEX.dia(now()),"hora:",INDEX.hora(now()),now()-ex)
            


            if self.color == 'Verde' or self.color == 'Amarillo':
                veces, examenes_por_vista_doc = self.visitas_de_revision(FT = True)
                if veces>1:
                    if REPORTEAR :
                        reporte.append("{} Es necesario hacer examenes {}".format(self,now()))

                    for vez in range(len(examenes_por_vista_doc)):          
                        self.condicion_de_salud += 1  
                        self.t_esperando = now()
                        if REPORTEAR and len(examenes_por_vista_doc[vez])>0:
                            reporte.append("{} Comienza exámenes {}".format(self,self.t_esperando))

                        tiempos_examenes = [tiempos_examen[ex]() for ex in examenes_por_vista_doc[vez]]
                        minimo = min(tiempos_examenes)
                        esperar = max(tiempos_examenes) + 0.45*int(len(tiempos_examenes)>1)*minimo
                        yield hold,  self,  esperar
                        if REPORTEAR:
                            reporte.append("{} Termina {} {}".format(self, random.choice(examenes_por_vista_doc[vez]),now()))

                        if vez == 0:
                            self.es_fastrack = True
                            cola_por_box.append(self)
                            if not (Boxs.n == 0 or len(cola_por_box)+len(cola_por_box.desde_fast_track)+len(cola_por_box.rojos)>1):
                                cola_por_box.pop()
                            else:
                                yield waitevent,  self,  cola_por_box.evento_disponible[self]
                            medicos.asignar_medico(self)

                            #print(self.tiempo_entra_box)
                            yield request,  self,  Boxs
                        
                        if not self.medico.disponible: 
                            self.esperando_doc = True
                            self.t_esperando = now()
                            yield waitevent,  self,  self.medico.evento_atender[self]          
                        
                        self.medico.inicia_atencion(self)
                        yield hold, self, tiempo_medico_atencion[vez]()
                        
                        if self.interrupted(): 
                            self.interruptReset()
                            if REPORTEAR :
                                reporte.append("{} INTERRUMPIDO por paciente ROJO {}".format(self, now()))
                        else:   
                            self.medico.termina_atencion(self)
                        self.condicion_de_salud += 1
                        

                    if self.se_hospitaliza : 
                        self.en_bording_time = (self.color != "Rojo")
                        self.entra_a_bording_time = now()
                        self.condicion_de_salud += 1
                        tiem = bording_time[self.color]()
                        if uniforme_hospitalizacion() < 0.07:
                            tiem = 0
                        bording_times[self.color].tally(tiem)

                        if self.color != "Rojo" and CamasHospitalizacion.n>0 and tiem >0:
                            '''
                            Si hay cama de espera va a la cama, si no , espera en el Box
                            Los pacientes solo esperarán en una, es decir, no se cambiarán de esperar un rato en Box y otro en Cama
                            '''
                            if REPORTEAR :
                                reporte.append("{} Se traslada a cama de espera {}".format(self, now()))                  
                            yield request, self, CamasHospitalizacion
                            self.medico.libera_paciente(self)
                            yield release,  self,  Boxs
                            yield hold, self, tiem
                            yield release, self, CamasHospitalizacion
                            self.proximo_a_cama()

                        else:
                            if REPORTEAR :
                                reporte.append("{} Comienza espera en box {}".format(self,now()))
                            yield hold, self, tiem
                            self.medico.libera_paciente(self)
                            yield release,  self,  Boxs
                            if self.interrupted():
                                if REPORTEAR :
                                    reporte.append("{} Se traslada a cama de espera {}".format(self, now()))
                                yield request, self, CamasHospitalizacion
                                yield hold, self, self.interruptLeft #lo que me queda del tiempo
                                yield release, self, CamasHospitalizacion
                                self.proximo_a_cama()

                        if REPORTEAR :
                            reporte.append("{} Se hospitaliza {}".format(self,now()))
                        if dias_transiente*24*60<=now()<=(dias_a_simular+dias_transiente)*24*60 and INDEX.dia(now()) in dias_monitoreados:
                            #print("1",now()-self.tiempo_entra_box_ft)
                            tiempos_desde_box[self.color].observe(now()-self.tiempo_entra_box)

                    else:
                        if dias_transiente*24*60<=now()<=(dias_a_simular+dias_transiente)*24*60 and INDEX.dia(now()) in dias_monitoreados:
                            #print("2",now()-self.tiempo_entra_box_ft)
                            tiempo_box_no_hospitaliza[self.color].tally(now()-self.tiempo_entra_box)
                        if REPORTEAR :
                            reporte.append("{} Alta sin hospitalización {}".format(self,now()))  
                        self.medico.libera_paciente(self) #liberar médico (eliminar a paciente de su lista)
                        yield release,  self,  Boxs #libera el box

                    #Cambiar a box normal -> se tiene que ir a examenes y si vuelve se pone a la cola por fastTrack
                   
                else:
                    if REPORTEAR :
                        reporte.append("{} Alta sin hospitalización {}".format(self,now()))
                    if dias_transiente*24*60<=now()<=(dias_a_simular+dias_transiente)*24*60 and INDEX.dia(now()) in dias_monitoreados:
                        #print("3",now()-self.tiempo_entra_box_ft)
                        tiempo_box_no_hospitaliza[self.color].tally(now()-self.tiempo_entra_box)
            else:
                if REPORTEAR :
                    reporte.append("{} Alta sin hospitalización {}".format(self,now()))
                if dias_transiente*24*60<=now()<=(dias_a_simular+dias_transiente)*24*60 and INDEX.dia(now()) in dias_monitoreados:
                    #print("4",now()-self.tiempo_entra_box_ft)
                    tiempo_box_no_hospitaliza[self.color].tally(now()-self.tiempo_entra_box)



    def Entrar_a_Emergencia(self) : 
        if not self.Triageado:
            if len(Triage.waitQ)>=5 and Triage.capacity==1 : 
                Triage.capacity=2
            elif len(Triage.waitQ)<=1 and Triage.capacity==2 : 
                Triage.capacity=1
            if dias_transiente*24*60<=now()<=(dias_a_simular+dias_transiente)*24*60 and INDEX.dia(now()) in dias_monitoreados:
                monitor_Triage.tally(int(Triage.capacity==1))
            if self.color != "Rojo":
                yield request, self, Triage
                if REPORTEAR :
                    reporte.append("{} Entra a Triage {}".format(self, now()))
                yield hold,  self,  tiempo_triage()  
                yield release,  self,  Triage
                if REPORTEAR :# or True:
                    reporte.append("{} Sale de Triage {}".format(self,now()))
            self.Triageado = True
        
        cola_por_box.append(self)
        
        if not (Boxs.n == 0 or len(cola_por_box)+len(cola_por_box.desde_fast_track)+len(cola_por_box.rojos)>1):
            cola_por_box.pop()
        else:
            if self.color == "Rojo":
                if REPORTEAR:
                    reporte.append("{} ROJO NO ENCUENTRA BOX {}".format(self,now()))
                rojo_necesita_box.signal()
            yield waitevent,  self,  cola_por_box.evento_disponible[self]

        yield request,  self,  Boxs #toma un box
        veces_necesita_medico , examenes_por_vista_doc = self.visitas_de_revision()
        yield hold, self, tiempo_espera_enfermera() #tiempo enfermera + en caminar doc
        self.esperando_doc = True
        medicos.asignar_medico(self)

        for vez in range(veces_necesita_medico) :     
            self.condicion_de_salud += 1
            
            if not self.medico.disponible: 
                self.esperando_doc = True
                self.t_esperando = now()
                yield waitevent,  self,  self.medico.evento_atender[self] #espera a que su médico asignado esté disponible para él          
            
            if dias_transiente*24*60<=now()<=(dias_a_simular+dias_transiente)*24*60 and INDEX.dia(now()) in dias_monitoreados:
                if vez == 0:
                    espera_por_doc.tally(now()-self.tiempo_entra_box)

            self.medico.inicia_atencion(self)
            yield hold, self, tiempo_medico_atencion[vez]() #tiempo que demora en atender al pacient
            
            if self.interrupted():  #el paciente puede habre sido interrumpido ya que llegó un paciente rojo que solicitó a su médico
                self.interruptReset()
                if REPORTEAR :
                    reporte.append("{} INTERRUMPIDO por paciente ROJO {}".format(self, now()))
            else:   
                self.medico.termina_atencion(self)
            self.condicion_de_salud += 1
            self.t_esperando = now()
            if vez<len(examenes_por_vista_doc):               
                if REPORTEAR and len(examenes_por_vista_doc[vez])>0:
                    reporte.append("{} Comienza exámenes {}".format(self,self.t_esperando))
                tiempos_examenes = [tiempos_examen[ex]() for ex in examenes_por_vista_doc[vez]]
                #print(self.color , tiempos_examenes)
                minimo = min(tiempos_examenes)
                esperar = max(tiempos_examenes) + 0.45*int(len(tiempos_examenes)>1)*minimo
                yield hold,  self,  esperar #tiempo de examenes, se espera el tiempo que toma su examen más largo
                if REPORTEAR:
                    reporte.append("{} Termina {} {}".format(self, random.choice(examenes_por_vista_doc[vez]),now()))
     
        if self.se_hospitaliza : 
            self.en_bording_time = (self.color != "Rojo")
            self.entra_a_bording_time = now()
            self.condicion_de_salud += 1
            tiem = bording_time[self.color]()
            if uniforme_hospitalizacion() < 0.07:
                tiem = 0
            bording_times[self.color].tally(tiem)

            if self.color != "Rojo" and CamasHospitalizacion.n>0 and tiem >0:
                '''
                Si hay cama de espera va a la cama, si no , espera en el Box
                Los pacientes solo esperarán en una, es decir, no se cambiarán de esperar un rato en Box y otro en Cama
                '''
                if REPORTEAR :
                    reporte.append("{} Se traslada a cama de espera {}".format(self, now()))                  
                yield request, self, CamasHospitalizacion
                self.medico.libera_paciente(self)
                yield release,  self,  Boxs
                yield hold, self, tiem
                yield release, self, CamasHospitalizacion
                self.proximo_a_cama()

            else:
                if REPORTEAR :
                    reporte.append("{} Comienza espera en box {}".format(self,now()))
                yield hold, self, tiem
                self.medico.libera_paciente(self)
                yield release,  self,  Boxs
                if self.interrupted():
                    if REPORTEAR :
                        reporte.append("{} Se traslada a cama de espera {}".format(self, now()))
                    yield request, self, CamasHospitalizacion
                    yield hold, self, self.interruptLeft #lo que me queda del tiempo
                    yield release, self, CamasHospitalizacion
                    self.proximo_a_cama()

            if REPORTEAR :
                reporte.append("{} Se hospitaliza {}".format(self,now()))
            if dias_transiente*24*60<=now()<=(dias_a_simular+dias_transiente)*24*60 and INDEX.dia(now()) in dias_monitoreados:
                tiempos_desde_box[self.color].observe(now()-self.tiempo_entra_box)

        else:
            if dias_transiente*24*60<=now()<=(dias_a_simular+dias_transiente)*24*60 and INDEX.dia(now()) in dias_monitoreados:
                tiempo_box_no_hospitaliza[self.color].tally(now()-self.tiempo_entra_box)
            if REPORTEAR :
                reporte.append("{} Alta sin hospitalización {}".format(self,now()))       
            self.medico.libera_paciente(self) #liberar médico (eliminar a paciente de su lista)
            yield release,  self,  Boxs #libera el box
        
    def proximo_a_cama(self):
        candidatos = [paciente for paciente in Boxs.activeQ if paciente.en_bording_time]
        #print(candidatos)
        candidatos.sort(key = lambda x: x.entra_a_bording_time, reverse = True)
        candidatos.sort(key = lambda x: optimo[x.color], reverse = True)

        if len(candidatos)>0:
        	self.interrupt(candidatos[0])
        

    @property
    def se_hospitaliza(self) : 
        u = get_se_hospitaliza()
        bol = u <= prob_hospitalizacion[self.color]
        if REPORTEAR and bol:
            reporte.append("{} Se hospitalizará {}".format(self,now()))

        self.quiere_hospital = bol
        return bol

    
    def examenes(self, FT = False) : 
        """
        Se genera el pack de examenes que se realizará el paciente
        en una de las veces que le toque hacerse examenes
        """
        Fast = 1
        if FT and self.color == 'Verde' and len(self.examenes_realizados) == 0:
        	Fast = 2
        elif FT and self.color == 'Amarillo':
        	self.color = 'Verde'

        examenes = []
        u = tiempos_examenes_1()    # tengo que generar 2 ??
        if u < prob_imagen[self.color]/Fast:
            tipo = get_tipo_im()
            if tipo not in self.examenes_realizados: 
                examenes.append(tipo)
        u = tiempos_examenes_2()
        if u < prob_laboratorio[self.color]/Fast and "Lab" not in self.examenes_realizados: 
            examenes.append("LAB")
        self.examenes_realizados+=examenes
        return examenes

    @property
    def coeficiente(self):
        return round((now()-self.tiempo_entra_a_cola)/optimo[self.color],2)

    def visitas_de_revision(self, FT = False) :
        """
        Calcula cuántas veces va a necesitar al doctor:
            Lo necesita por lo menos una vez, luego depende de los examenes

        *Si se realiza examenes entonces debemos sumar una ves para su revisión: int(len(examenes)>0)
        *Luego si se realizó examenes con un 10% de probabilidad necesitará una segunda revisión extra: int(len(examenes)>0)*int(uniform(0,1)<=0.1)

        Nota: el int(expresion booleana) corresponde a 0:False, 1:True

        """
        examenes = self.examenes(FT)
        pack = []
        if len(examenes)>0:
            pack.append(examenes)
        veces = 1 + int(len(examenes)>0) + int(len(examenes)>0)*int(doble_examen()<=prob_doble[self.color])
        if veces == 3:
            nuevos = self.examenes()
            while len(nuevos)==0:
                nuevos = self.examenes()
            pack.append(nuevos)
        return veces, pack

    def __repr__(self) : 
        return "Paciente"+str(self.id)+" : "

    def __str__(self) : 
        return self.__repr__()


class Llegada_Pacientes(Process) : 
    """
    Proceso de llegada :  crea cada Paciente y lo hace entrar a la Emergencia
    """
    def Llegar(self) : 
        while True : 
            hora,  dia = INDEX.hora(now()),   INDEX.dia(now())
            t_llegada = tasas[hora][dia]                            
            yield hold,  self,  tiempo_hasta_otro_paciente(t_llegada)
            p = Paciente( get_color( probabilidades[dia][hora] ) )
            if REPORTEAR  :
                reporte.append("{} Llegada a Urgencia UC {}".format(p,now()))
            if proceso_fastt.determinar_fastt(p):
                activate(p, p.Entrar_a_Emergencia_FT())
            else:
                activate(p, p.Entrar_a_Emergencia())

class ListMedicos(list) : 
    """
    Clase especializada para manejar a los medicos
    """    
    def iniciar(self, n_medicos_iniciales):
        self.n_medicos_iniciales = n_medicos_iniciales
        for i in range(n_medicos_iniciales) : 
            self.append(Medico())
        self.debe_entrar = True
        self.debe_salir = True

    def asignar_medico(self,  paciente, evento = False, entra = False) : 
        """
        En primer lugar se ordenan los médicos por cantidad de pacientes atendiendo
        Luego por si tiene un rojo o no -> si ya atiende a un rojo es menos probable que le toque otro
        Luego se ordenan por si está disponible o no

        Se selecciona el que tenga menos pacientes a su cargo y esté disponible. 
        En caso de que no haya ninguno diponible se le asigna el que tenga menos a su cargo.
        """

        self.sort(key = lambda x :  int(x.disponible), reverse = True)
        self.sort(key = lambda x :  len([p for p in x.pacientes if p.color == "Rojo"]))
        self.sort(key = lambda x :  len([p for p in x.pacientes if not p.en_bording_time]))
        cual = self[0]
        cual.pacientes.append(paciente)

        if evento:
            cual.evento_atender.update({paciente : evento})
        else:
            cual.evento_atender.update({paciente :SimEvent("Le toca atender a Paciente : "+str(paciente.id))})

        paciente.medico = cual

        if REPORTEAR :
            reporte.append("{} Es asignado para atender {} {}".format(cual, paciente, now()))
        """
        Si se le acaba de asignar un paciente y está atendiendo a alguien,
        se interrumpe la atención al paciente actual -> lo deja de atender y va a atender al rojo
        (suponemos que los becados o la enfermera lo siguen atendiendo)
        """
        if  paciente.color == "Rojo" and cual.paciente_actual and (len(cual.evento_atender[paciente].waits)>0 or paciente.esperando_doc):
            paciente.interrupt(cual.paciente_actual)
            cual.termina_atencion(cual.paciente_actual)

        if not entra:
            cual.elegir_paciente()

    @property
    def disponibles(self) : 
        disponibles = len(self)
        for medico in self : 
            if medico.atendiendo : 
                disponibles-=1
        return disponibles
    
class Medico: 

    def __init__(self) : 
        self.id = next(ID.medico)
        self.atendiendo = False
        self.evento_atender = {}    
        self.pacientes = [] #Lista con los pacientes que está actualmente atendiendo
        self.paciente_actual = None

    def inicia_atencion(self,  paciente) : 
        self.atendiendo = True
        paciente.esperando_doc = False
        self.paciente_actual = paciente
        if REPORTEAR :
            reporte.append("{} Comienza a atender {} {}".format(self, self.paciente_actual, now()))

    def termina_atencion(self,  pac = None) :
        """
        Cuando termina de atender un paciente debe ir a atender 
        a alguno de los otros que le corresponde.

        En primer lugar revisa si tiene rojos por atender y atiende a un rojo
        Si no, atiende al que lleve más tiempo esperándolo                          -> esto podría variar al que tiene menor estado de salud ???
        """
        self.atendiendo = False
        if REPORTEAR and pac:
            reporte.append("{} Termina de atender {} {}".format(self, pac, now()))

        self.elegir_paciente()

    def elegir_paciente(self):
        if self.disponible:
            esperandolo = [paciente for paciente in self.pacientes if len(self.evento_atender[paciente].waits)>0 or paciente.esperando_doc]
            rojos = [paciente for paciente in esperandolo if paciente.color == "Rojo"]
            if len(esperandolo)>0:
                if len(rojos)>0:
                    rojos.sort(key = lambda x :  (now()-x.t_esperando),  reverse= True)
                    proximo = rojos[0]
                else:
                    esperandolo.sort(key = lambda x :  (now()-x.t_esperando),  reverse= True)
                    proximo = esperandolo[0]

                self.evento_atender[proximo].signal()
                if REPORTEAR:
                    reporte.append("{} Va a atender {} {}".format(self, proximo, now()))
            else:
                self.paciente_actual = None
                if REPORTEAR:
                    reporte.append("{} Desocupado {}".format(self, now()))
        

    def entrar_al_turno(self):
        reasignar = []
        for medico in medicos:
            if len(medico.pacientes)>2:
                if NUMEROS_ALEATORIOS_COMUNES:
                    paciente_reasignado = medico.pacientes[0]
                else:
                    paciente_reasignado = random.choice(medico.pacientes)
                if paciente_reasignado:
                    reasignar.append([paciente_reasignado,medico.evento_atender[paciente_reasignado]])
                    medico.pacientes.remove(paciente_reasignado)
                    medico.evento_atender.pop(paciente_reasignado)
        medicos.append(self)
        for paciente, event in reasignar:
            medicos.asignar_medico(paciente, evento = event, entra = True)
        if REPORTEAR :
            reporte.append("{} Entra al turno {}".format(self, now()))
        self.elegir_paciente()

        

    def sale_del_turno(self):
        if REPORTEAR :
            reporte.append("{} Sale del turno {}".format(self, now()))
        medicos.remove(self)
        for paciente in self.pacientes:
            medicos.asignar_medico(paciente, evento = self.evento_atender[paciente])
        del self

    def libera_paciente(self,  paciente, rojo = False) : 
        """
        Al liberar un paciente manda una señal de que se ha desocupado un Box
        """
        self.pacientes.remove(paciente)
        self.evento_atender.pop(paciente)

        if len(cola_por_box)+len(cola_por_box.rojos)+len(cola_por_box.desde_fast_track)>0:
            a = cola_por_box.pop()
            cola_por_box.evento_disponible.pop(a).signal()         

        if REPORTEAR :
            reporte.append("{} Da de alta {} {}".format(self, paciente, now()))
        
        self.elegir_paciente()

    @property
    def disponible(self) : 
        return not self.atendiendo

    def __repr__(self) : 
        return "Medico"+str(self.id)+" :"

    def __str__(self) : 
        return self.__repr__()

class SupervisorRojo(Process):
    """
    Proceso de Supervisor por si llega un Rojo :  
        Si llega un rojo y no hay box disponible se debe desocupar uno

    *Primero se ve todos los pacientes que no son Rojos y que están usando un box
    *Luego, estos se ordenan por color, es decir, de menos importante a más importante
    *Si hay más de uno del mismo color se debe ir el que tenga mejor estado de salud (i.e: el que ha pasado por más etapas)
    """

    def desocupar_box(self):
        while True:
            yield waitevent, self, rojo_necesita_box
            candidatos = []
            todos = []
            for medico in medicos:
                for atendiendose in medico.pacientes:
                    todos.append(atendiendose.color)
                    if atendiendose.color != "Rojo":#and not atendiendose.quiere_hospital:
                        candidatos.append(atendiendose)
            #print(candidatos)
            #print(todos)

            candidatos.sort(key = lambda x: optimo[x.color], reverse = True)
            if len(candidatos)>0:
                candidatos = [c for c in candidatos if c.color == candidatos[0].color]
                candidatos.sort(key = lambda x: x.condicion_de_salud, reverse = True)


                se_debe_ir = candidatos[0]
                
                Boxs.activeQ.remove(se_debe_ir)
                Boxs.n+=1
                se_debe_ir.medico.libera_paciente(se_debe_ir, True)
                self.cancel(se_debe_ir)
                
                if REPORTEAR :
                    reporte.append("{} Se debe ir por paciente ROJO {}".format(se_debe_ir, now()))
                del se_debe_ir
                

class Horario:

    def __init__(self, horario_inicio, horario_fin, cantidad_medicos, cantidad_camas = 0, amarillos = 0):
        self.horario_inicio = horario_inicio
        self.horario_fin = horario_fin
        self.cantidad_medicos = cantidad_medicos
        self.cantidad_camas = cantidad_camas
        self.porcentaje_am = amarillos

    def __repr__(self):
        return "({}, {}, {}, {})".format(self.horario_inicio, self.horario_fin, self.cantidad_medicos,self.cantidad_camas,self.porcentaje_am)

class Turno(Process):

    def __init__(self):
        Process.__init__(self)

        dias = ["l","m","w","j","v","s","d"]
        esquemas = {d:[] for d in dias}

        with open(CARPETA+"/temp1.txt","r") as file:
            for line in file:

                spl = line.replace("\n","").split("\t")
                horario_inicio = int(spl[1])
                horario_fin = int(spl[2])
                cantidad_medicos = int(spl[3])

                for d in dias:
                    if d in line:
                        esquemas[d].append(Horario(horario_inicio, horario_fin, cantidad_medicos))

        for dia in esquemas:
            esquemas[dia].sort(key = lambda x :  x.horario_inicio)

        self.horarios = {i:esquemas[dias[i]] for i in range(len(dias))}

    def revisar_cambio_de_turno(self, medicos):
        n_medicos_iniciales = -1
        semana = []
        for lis in range(7):
        	semana+=self.horarios[lis]
        #print(semana)



        contador = -1
        while True:
            contador += 1
            contador = contador%len(semana)
            
            horario = semana[contador]
            #print(INDEX.dia(now()),INDEX.hora(now()),horario,len(medicos))

            if n_medicos_iniciales<0:
                medicos.iniciar(horario.cantidad_medicos)
                n_medicos_iniciales = len(medicos)

            if dias_transiente*24*60<=now()<=(7+dias_transiente)*24*60:
                medicos_cantidad.observe(len(medicos))

            yield hold, self, abs(horario.horario_fin-horario.horario_inicio)*60

            if semana[(contador+1)%len(semana)].cantidad_medicos > horario.cantidad_medicos:
                for i in range(semana[(contador+1)%len(semana)].cantidad_medicos-horario.cantidad_medicos):
                    nuevo = Medico()
                    nuevo.entrar_al_turno()
            elif semana[(contador+1)%len(semana)].cantidad_medicos < horario.cantidad_medicos:
                #print("salen",semana[(contador+1)%len(semana)].cantidad_medicos, horario.cantidad_medicos)
                for i in range(horario.cantidad_medicos-semana[(contador+1)%len(semana)].cantidad_medicos):
                    if NUMEROS_ALEATORIOS_COMUNES:
                        medicos[0].sale_del_turno()
                    else:
                        random.choice(medicos).sale_del_turno()

            if dias_transiente*24*60<=now()<=(7+dias_transiente)*24*60:
                medicos_cantidad.observe(len(medicos))

            

class BoxFastTrack(Process):

    def __init__(self):
        Process.__init__(self)

        self.porcentaje = 0
        self.hay_FastTrack = False

        self.evento_siguiente = []
        self.evento_medico_siguiente = []

        dias = ["l","m","w","j","v","s","d"]
        esquemas = {d:[] for d in dias}

        with open(CARPETA+"/temp2.txt","r") as file:
            for line in file:
                spl = line.replace("\n","").split("\t")
                ahorario_inicio = int(spl[1])
                ahorario_fin = int(spl[2])
                acantidad_camas = int(spl[3])
                acantidad_medicos = int(spl[4])
                aporcentaje_am = float(spl[5])
                
                for d in dias:
                    if d in line:
                        esquemas[d].append(Horario(ahorario_inicio, ahorario_fin, acantidad_medicos, acantidad_camas, aporcentaje_am))

        for dia in esquemas:
            esquemas[dia].sort(key = lambda x :  x.horario_inicio)

        self.horarios = {i:esquemas[dias[i]] for i in range(len(dias))}
        self.disminuir_box = 0
        self.disminuir_medicos = 0
        self.cola = []
        self.cola_medico = []
        self.atendiendose = []
        #print(self.horarios)
        #print(5/0)

    def determinar_fastt(self, paciente, permitido = False):
       
    	if (self.hay_FastTrack or permitido ) and ( paciente.color in ['Azul','Verde'] or (paciente.color == 'Amarillo' and fast_amarillo()<self.porcentaje) ):
            paciente.es_fastrack = True
            return True
    	return False


    def revisar_cambio_de_turno(self, BoxFT, MedFT):
        if len(self.horarios[0]) == 0 :
            return False

        n_iniciales = -1
        semana = []
        for lis in range(7):
        	semana+=self.horarios[lis]
        #print(semana)


        hor = -1
        while True:
            hor += 1
            hor = hor%len(semana)            
            horario = semana[hor]


            if n_iniciales<0:
                if (horario.cantidad_medicos > 0 and horario.cantidad_camas >0):
                    self.hay_FastTrack = True
                    BoxFT.n = horario.cantidad_camas
                    MedFT.n = horario.cantidad_medicos

                n_iniciales = 0

            

            self.porcentaje = horario.porcentaje_am
        

            if (horario.cantidad_medicos == 0 or horario.cantidad_camas == 0) and self.hay_FastTrack == True:

                self.hay_FastTrack = False

                aux = []
                for paciente in self.cola:
                    if (paciente in BoxFT.waitQ or paciente.esperandoft):
                        aux.append(paciente)

                for paciente in aux:
                    if paciente in BoxFT.waitQ:
                        BoxFT.waitQ.remove(paciente)
                    self.cola.remove(paciente)

                for paciente in aux:
                    paciente.es_fastrack = False
                    paciente.esperandoft = False
                    activate(paciente, paciente.Entrar_a_Emergencia())

            #print("\n",INDEX.dia(now()),"Sacar a los pacientes\n ******************", len(aux))


            elif self.hay_FastTrack == False and (horario.cantidad_medicos > 0 and horario.cantidad_camas >0):
                

                indices = [p for p in cola_por_box if proceso_fastt.determinar_fastt(p, permitido = True)]
                for indice in indices:
                    cola_por_box.remove(indice)
                    #cola_por_box.evento_disponible.remove(indice)

               
                for indice in indices:
                    activate(indice, indice.Entrar_a_Emergencia_FT(permitido = True))

                self.hay_FastTrack = True

             #print("\n",INDEX.dia(now()),"Meter a los pacientes\n ******************", len(indices))

            yield hold, self, abs(horario.horario_fin-horario.horario_inicio)*60
            
            if semana[(hor+1)%len(semana)].cantidad_camas > horario.cantidad_camas:
                variacion = abs(semana[(hor+1)%len(semana)].cantidad_camas-horario.cantidad_camas)
                self.disminuir_box = 0
       
                #print("boxees 0", BoxFT.n)
                BoxFT.capacity=semana[(hor+1)%len(semana)].cantidad_camas
                BoxFT.n+=variacion
                #print("boxees 1", BoxFT.n)

            elif semana[(hor+1)%len(semana)].cantidad_camas < horario.cantidad_camas:
                variacion = abs(semana[(hor+1)%len(semana)].cantidad_camas-horario.cantidad_camas) 
                BoxFT.capacity=semana[(hor+1)%len(semana)].cantidad_camas

                self.disminuir_box = variacion

                for c in range(variacion - len(self.cola_medico) - len(self.atendiendose)):
                	BoxFT.n-=1
                	self.disminuir_box-=1

                
               

            if semana[(hor+1)%len(semana)].cantidad_medicos > horario.cantidad_medicos:
                variacion = abs(semana[(hor+1)%len(semana)].cantidad_medicos-horario.cantidad_medicos)
                self.disminuir_medicos = 0
                
                MedFT.capacity=semana[(hor+1)%len(semana)].cantidad_medicos
                MedFT.n+=variacion

            elif semana[(hor+1)%len(semana)].cantidad_medicos < horario.cantidad_medicos:
                variacion = abs(semana[(hor+1)%len(semana)].cantidad_medicos-horario.cantidad_medicos)
                MedFT.capacity=semana[(hor+1)%len(semana)].cantidad_medicos

                self.disminuir_medicos = variacion

                for c in range(variacion - len(self.cola_medico) - len(self.atendiendose)):
                	MedFT.n-=1
                	self.disminuir_medicos-=1

                

class ColaBox(list) : 
    """
    Clase especializada para manejar la cola de espera desde el Triage hasta el Box
    """
    def __init__(self) :
        list.__init__(self)
        self.evento_disponible = {}
        self.rojos = []
        self.desde_fast_track = []
        

    def append(self, paciente) : 
        if paciente.color == "Rojo":
            self.rojos.append(paciente)
        elif paciente.es_fastrack:
        	self.desde_fast_track.append(paciente)
        else:
            list.append(self, paciente)

        nuevo = False
        if paciente.tiempo_entra_a_cola < 0:
            nuevo = True
            paciente.tiempo_entra_a_cola = now()
        cola_por_box.evento_disponible.update({paciente :SimEvent("Le toca box a Paciente : "+str(paciente))})

        if REPORTEAR and not paciente.es_fastrack and nuevo:
            reporte.append("{} Entra a cola de espera {}".format(paciente, now()))
        if dias_transiente*24*60<=now()<=(dias_a_simular+dias_transiente)*24*60 and INDEX.dia(now()) in dias_monitoreados and not paciente.es_fastrack and nuevo:
            monitor_cola.observe(len(self)+len(self.rojos)+len(BoxFT.waitQ))
   

    def elegir_por_color(self, lista):
        lista.sort(key = lambda x: optimo[x.color])
        return lista[0]

    def elegir_por_tiempo(self, lista):
        lista.sort(key = lambda x: now()-x.tiempo_entra_a_cola)
        return lista[-1]

    def pop(self) :
        """
        Siempre que alguien deba salir de la cola, en primer lugar se revisará si hay un rojo esperando

        Si no hay rojos entonces se selecciona el que tenga el mayor coeficiente de espera
        * si hay dos con el mismo coeficiente (redondeado a 2 decimales) se puede elegir por tiepo o por colorsys
                                                                         actualmente estoy eligiendo por tiempo.
        """

        lista_paciente = None
        if len(self.rojos)>0:
            self.rojos.sort(key = lambda x :  now()-x.tiempo_entra_a_cola)
            proximo_en_pasar = self.rojos[-1]
            lista_paciente = self.rojos

        elif len(self.desde_fast_track)>0:
            lista_paciente = self.desde_fast_track
            proximo_en_pasar = lista_paciente[0]
        else:
            self.sort(key = lambda x :  x.coeficiente, reverse = True)
            candidatos = self[:5]
            candidatos = [c for c in candidatos if c.coeficiente == candidatos[0].coeficiente]
            if len(candidatos)>1:
                proximo_en_pasar = self.elegir_por_tiempo(candidatos)
            else: 
                proximo_en_pasar = candidatos[0]
            lista_paciente = self

        #if proximo_en_pasar.tiempo_entra_box_ft < 0:
        if not proximo_en_pasar.es_fastrack:
            proximo_en_pasar.tiempo_entra_box = now()
            if dias_transiente*24*60<=now()<=(dias_a_simular+dias_transiente)*24*60:
                personas_por_hora[INDEX.dia(now())][proximo_en_pasar.color]+=1

        dif_de_tiempo = proximo_en_pasar.tiempo_entra_box-proximo_en_pasar.tiempo_entra_a_cola
        if dias_transiente*24*60<=now()<=(dias_a_simular+dias_transiente)*24*60 and INDEX.dia(now()) in dias_monitoreados and not proximo_en_pasar.es_fastrack:
            tiempo_hasta_box.observe(dif_de_tiempo)
            tiempos_por_color[proximo_en_pasar.color].observe(dif_de_tiempo)
            proporciones[proximo_en_pasar.color].observe(int(dif_de_tiempo<optimo[proximo_en_pasar.color]))
            proporciones_total.observe(int(dif_de_tiempo<optimo[proximo_en_pasar.color]))
            

        if REPORTEAR:
            reporte.append("{} Es llamado a un box {}".format(proximo_en_pasar, now()))

        
        lista_paciente.remove(proximo_en_pasar)
        if dias_transiente*24*60<=now()<=(dias_a_simular+dias_transiente)*24*60 and INDEX.dia(now()) in dias_monitoreados and not proximo_en_pasar.es_fastrack:
            monitor_cola.observe(len(self)+len(self.rojos)+len(BoxFT.waitQ))
        return proximo_en_pasar
        

if __name__ == '__main__' : 
    t = []
    colores = ["Amarillo","Azul","Naranja","Verde"]
    prop = {color:[] for color in colores}

    cola_media = []
    todas_las_colas = []
    todos_los_tiempos = []

    todos_tiempos_desde_box = {color:[] for color in colores+['Rojo']}
    todos_tiempos_por_color = {color:[] for color in colores+['Rojo']}
    todos_tiempo_box_no_hospitaliza = {color:[] for color in colores+['Rojo']}
    todos_bording_times = {color:[] for color in colores+['Rojo']}

    todos_monitor_Triage = []
    todos_espera_por_doc = []

    optimo = {"Amarillo" : 60, "Azul" : 60*4 ,  "Naranja" : 10,  "Rojo" : 1 ,  "Verde" : 60*2}    #¿qué haremos con el ROJO ?

    probabilidades,  tasas = leer_informacion()



    inputs = []
    with open("temp.txt","r") as temp:
        lineas = 0
        for line in temp:
            inputs.append(line.replace("\n","").strip())
            lineas+=1
    #print(inputs)

    CARPETA = inputs[0]
    k = int(inputs[1])
    n_boxs = int(inputs[2])
    COMENTARIO_gen = inputs[4]+"\n"
    n_camas_hospitalizacion = int(inputs[3])

    NUMEROS_ALEATORIOS_COMUNES = bool(inputs[5].replace("\n",""))

    monitoreados = int(inputs[6].replace("\n",""))

    if monitoreados < 7:
    	dias_monitoreados = [monitoreados]
    else:
    	dias_monitoreados = [di for di in range(int(monitoreados))]

    todas_PROP = []

    uso_camasHospitalizacion = []
    uso_boxFastTrack = []

    todas_las_personas_por_hora = {i:{color:[] for color in colores+['Rojo']} for i in range(7)}

   # n_fasttrack

    imprimir = 0
    i = 0
    while i < k: 
        print(i)
        reporte = []
        REPORTEAR = i == imprimir#i==imprimir#True  #solo guarda los eventos de la primera corrida
        grafico = True#True
        
        n_triage = 1
        
        personas_por_hora = {i:{color:0 for color in colores+['Rojo']} for i in range(7)} #personas_por_hora[INDEX.hora(now())][paciente.color]+=1


        tiempo_hasta_box = Monitor()
        monitor_cola = Monitor()
        medicos_cantidad = Monitor()
        proporciones = {color:Monitor() for color in colores+['Rojo']}
        proporciones_total = Monitor()

        tiempos_desde_box = {color:Monitor() for color in colores+['Rojo']}
        tiempos_por_color = {color:Monitor() for color in colores+['Rojo']}
        tiempo_box_no_hospitaliza = {color:Monitor() for color in colores+['Rojo']}
        bording_times = {color:Monitor() for color in colores+['Rojo']}
        monitor_Triage = Monitor()
        espera_por_doc = Monitor()

        #Tenemos n_boxs cantidad de Boxs disponibles
        Boxs = Resource(capacity = n_boxs)
        CamasHospitalizacion = Resource(capacity = n_camas_hospitalizacion, monitored = True, monitorType=Monitor)

        #Tenemos n_triage cantidad de Triage habilitado
        Triage = Resource(capacity = n_triage)

        #Se crea una cola con los pacientes a la espera de Box
        cola_por_box = ColaBox()

        #Se crea una lista especializada de Médicos
        medicos = ListMedicos()
        
        #Se crea el evento de que llegue un rojo y necesite desocupar un box
        rojo_necesita_box = SimEvent("ROJO NECESITA BOX")

        #Se inicializa el escenario para la simulación
        initialize()


        proceso_fastt = BoxFastTrack()
        BoxFT = Resource(capacity = 0, monitored = True, monitorType=Monitor )
        MedFT = Resource(capacity = 0)
        activate(proceso_fastt, proceso_fastt.revisar_cambio_de_turno(BoxFT,MedFT))

        turno = Turno()
        activate(turno, turno.revisar_cambio_de_turno(medicos))

        #Se inicializa la llegada de pacientes
        l = Llegada_Pacientes()
        activate(l, l.Llegar(), at = 0.0001)

        supervisor = SupervisorRojo()
        activate(supervisor, supervisor.desocupar_box())

        #print("Simulacion Iniciada")
        #Se inicia la simulación
        dias_transiente = 14
        dia_extra = 0
        dias_a_simular = 31

        COMENTARIO = "sim {} dias - transiente {} dias -  Funciones de examenes acotadas".format(dias_a_simular,dias_transiente)
        simulate(until=(dias_transiente+dias_a_simular+dia_extra)*24*60)   #> *60 simular una semana antes y un día después
                                            # 
        #print("Simulacion Terminada")
        n_medicos_iniciales = medicos.n_medicos_iniciales
        #monitor_cola.timeAverage() < 30

        if len(CamasHospitalizacion.actMon[-1]) >1 and CamasHospitalizacion.actMon[-1][0] > 0:
	        ta = 0
	        for indice in range(1,len(CamasHospitalizacion.actMon)):
	            ta+= (CamasHospitalizacion.actMon[indice][0]-CamasHospitalizacion.actMon[indice-1][0])*CamasHospitalizacion.actMon[indice-1][1]
	        uso_camasHospitalizacion.append(ta/CamasHospitalizacion.actMon[-1][0])

        if len(BoxFT.actMon[-1]) >1 and BoxFT.actMon[-1][0] > 0:
	        ta = 0
	        for indice in range(1,len(BoxFT.actMon)):
	            ta+= (BoxFT.actMon[indice][0]-BoxFT.actMon[indice-1][0])*BoxFT.actMon[indice-1][1]
	        uso_boxFastTrack.append(ta/BoxFT.actMon[-1][0])

        for key1 in todas_las_personas_por_hora:
            for key2 in todas_las_personas_por_hora[key1]:
                todas_las_personas_por_hora[key1][key2].append(personas_por_hora[key1][key2])


        valido = True
        if max(monitor_cola.yseries())>120:
        	valido = False 
        	
        if valido:
            u = [a[1] for a in tiempo_hasta_box]
            
            if len(u)>1:
                u = st.bayes_mvs(nan_to_numero(u), alpha=0.95)
                t.append(u[0][0])

            for color in colores:
                if len(proporciones[color])>1:
                    u = [a[1] for a in proporciones[color]]
                    u = st.bayes_mvs(nan_to_numero(u), alpha=0.95)
                    prop[color].append(u[0][0])

            todas_las_colas.append(monitor_cola.yseries())
            todos_los_tiempos.append(monitor_cola.tseries())
            cola_media.append(monitor_cola.timeAverage())


            if len(proporciones_total)>1:
                u = [a[1] for a in proporciones_total]
                u = st.bayes_mvs(nan_to_numero(u), alpha=0.95)
                todas_PROP.append(u[0][0])


            for color in colores+['Rojo']:
                if len(tiempos_desde_box[color])>1:
                    u = [a[1] for a in tiempos_desde_box[color]]
                    u = st.bayes_mvs(nan_to_numero(u), alpha=0.95)
                    todos_tiempos_desde_box[color].append(u[0][0])

            for color in colores:
                if len(tiempos_por_color[color])>1:
                    u = [a[1] for a in tiempos_por_color[color]]
                    u = st.bayes_mvs(nan_to_numero(u), alpha=0.95)
                    todos_tiempos_por_color[color].append(u[0][0])

            for color in colores+['Rojo']:
                if len(tiempo_box_no_hospitaliza[color])>1:
                    u = [a[1] for a in tiempo_box_no_hospitaliza[color]]
                    u = st.bayes_mvs(nan_to_numero(u), alpha=0.95)
                    todos_tiempo_box_no_hospitaliza[color].append(u[0][0])

            for color in colores+['Rojo']:
                if len(bording_times[color])>1:
                    u = [a[1] for a in bording_times[color]]
                    u = st.bayes_mvs(nan_to_numero(u), alpha=0.95)
                    todos_bording_times[color].append(u[0][0])


            if i == imprimir:
                linea_inicial = 0
                with open("{}/iteracion {} REPORTE.txt".format(CARPETA,i),"w") as file :
                    contad = -1
                    for evento in reporte :
                        contad+=1
                        detalle = evento.replace(":","").split()
                        tie = detalle[-1][ :7]
                        if float(tie)>=20160 and linea_inicial<1:
                            linea_inicial = contad
                        ev = tie+"		" + "dia :"+ str(INDEX.dia(float(detalle[-1])))+ "	hora :"+ str(INDEX.hora(float(detalle[-1])))+"		"+ " ".join(detalle[0 :-1])
                        file.write(ev+"\n")

                cambiar("{}/iteracion {} REPORTE.txt".format(CARPETA,i), path_out = "{}/iteracion {} REPORTE DISCO.txt".format(CARPETA,i))
                borrar_transiente("{}/iteracion {} REPORTE DISCO.txt".format(CARPETA,i), "{}/iteracion {} REPORTE DISCO - SIN TRANSCIENTE.txt".format(CARPETA,i), linea_inicial)

                xs, ys, zs = [],[],[]
                for x,y in medicos_cantidad: 
                    xs.append(INDEX.hora(x))
                    ys.append(y)
                    zs.append(x)

                plt.figure()
                plt.xlabel('Transcurso del tiempo en minutos')
                plt.ylabel('Cantidad de medicos')
                plt.plot(zs,ys, color='blue')
                plt.title("it {} Numero de medicos - n_box = {} - n_medicos_iniciales = {}".format(i,n_boxs,n_medicos_iniciales))
                plt.savefig(CARPETA+"/it {} Comportamiento de cada dia".format(i))
                plt.close()

                plt.figure()
                plt.xlabel('Comportamiento de cada dia')
                plt.ylabel('Cantidad de medicos')
                plt.hist(ys, color='red')
                plt.title("it {} Numero de medicos - n_box = {} - n_medicos_iniciales = {}".format(i,n_boxs,n_medicos_iniciales))
                plt.savefig(CARPETA+"/it {} Numero de medicos - n_box = {} - n_medicos_iniciales = {}".format(i,n_boxs,n_medicos_iniciales))
                plt.close()

            #print("correcta - out")

        else:
        	i-=1
        	#print("error - out")

        i+=1

        
        if grafico and False:
            plt.figure()
            plt.xlabel('Transcurso del tiempo en minutos')
            plt.ylabel('Largo ColaBox')
            plt.plot(xs,ys, color='pink')
            plt.title("Largo Cola de espera por Box"+"\n\nmedia de la iteracion {} = {} - n_box = {} - med_i = {} - c_espera {}".format(i,cm,n_boxs,n_medicos_iniciales,n_camas_hospitalizacion))
            
            if REPORTEAR or True:
                plt.savefig("{}/iteracion {} = {} - n_box = {} - n_medicos_iniciales = {}".format(CARPETA,i,cm,n_boxs,n_medicos_iniciales),transparent = False)
            #plt.show()
            plt.close()

        

        """
        El siguiente pedazo de código solo imprime reportes
             En todo el código, cada vez que se evalua el valor de "REPORTEAR" es para saber si quiero guardar los eventos o no.
        """
    


    """
    if imprimir and False:

        quienes = list(set([registro.split(" :")[0] for registro in reporte]))
        seleccionados = [persona for persona in quienes if "Medico" in persona or "Rojo" in persona or (int(persona.split("e")[-1]) in list(range(20))+list(range(len(quienes)-30,len(quienes)-20)))]
        for j in range(len(seleccionados)) :
            with open("Reportes/"+seleccionados[j]+".txt","w") as file :
                for evento in reporte :
                    if seleccionados[j] == evento.split(" :")[0] or seleccionados[j]+" " in evento :
                        detalle = evento.replace(":","").split()
                        ev = detalle[-1][ :7]+"     "+ "dia :"+ str(INDEX.dia(float(detalle[-1])))+ "   hora :"+ str(INDEX.hora(float(detalle[-1])))+ "     "+" ".join(detalle[0 :-1]) 
                        file.write(ev+"\n")
    """

        #print(i)
    if True:
        import numpy as np
        from pylab import *

        co = {'Azul':'blue','Naranja':'orange','Rojo':'red','Amarillo':'yellow', 'Verde':'green'}

        graficarx = []
        graficary = []
        graficartitulos = []
        medio_intervalo = [{},{},{},{}]
        __colores = []

        promedios = {}
        for color in colores+['Rojo']:
            if len(todos_tiempos_desde_box[color])>1:
                u = st.bayes_mvs(nan_to_numero(todos_tiempos_desde_box[color]), alpha=0.95)
                promedios.update({color:u[0][0]})
                medio_intervalo[0].update({color:(u[0][1][1]-u[0][1][0])})
            else:
                promedios.update({color:0})
                medio_intervalo[0].update({color:0})
        col = tuple(sorted([color for color in promedios if color != 'Azul']))
        medias = tuple([promedios[c] for c in col])
        __colores.append(col)
        graficarx.append(medias)
        graficary.append(col)
        graficartitulos.append('Tiempo medio Box - Hospital')

        tiempo_colores="\n\n tiempo medio hasta box desde que se mete a la cola: "
        promedios = {}
        for color in colores+['Rojo']:
            if len(todos_tiempos_por_color[color])>1:
                com0 = st.bayes_mvs(nan_to_numero(todos_tiempos_por_color[color]), alpha=0.95)
                promedios.update({color:com0[0][0]})
                tiempo_colores+="\n + {} : {} - S^2: {} - S: {}".format(color, com0[0],com0[1][0],com0[2][0])
                medio_intervalo[1].update({color:(com0[0][1][1]-com0[0][1][0])})
            else:
                promedios.update({color:0})
                medio_intervalo[1].update({color:0})
        tiempo_colores+="\n"
        col = tuple(sorted([color for color in promedios]))
        medias = tuple([promedios[c] for c in col])
        __colores.append(col)
        graficarx.append(medias)
        graficary.append(col)
        graficartitulos.append('Tiempo medio Triage - Box')

        tiempo_colores_nh="\n\n tiempo desde que llega a box hasta que se va sin hospitalizar: "
        promedios = {}
        for color in colores+['Rojo']:
            if len(todos_tiempo_box_no_hospitaliza[color])>1:
                com1 = st.bayes_mvs(nan_to_numero(todos_tiempo_box_no_hospitaliza[color]), alpha=0.95)
                promedios.update({color:com1[0][0]})
                tiempo_colores_nh+="\n + {} : {} - S^2: {} - S: {}".format(color, com1[0], com1[1][0], com1[2][0])
                medio_intervalo[2].update({color:(com1[0][1][1]-com1[0][1][0])})
        col = tuple(sorted([color for color in promedios]))
        medias = tuple([promedios[c] for c in col])
        __colores.append(col)
        graficarx.append(medias)
        graficary.append(col)
        graficartitulos.append('Tiempo medio Box - Alta sin hospitalización')

        comentario_bording="\n\n tiempo boarding time: "
        promedios = {}
        for color in colores+['Rojo']:
            if len(todos_bording_times[color])>1:
                com2 = st.bayes_mvs(nan_to_numero(todos_bording_times[color]), alpha=0.95)
                promedios.update({color:com2[0][0]})
                comentario_bording+="\n + {} : {} - S^2: {} - S: {}".format(color, com2[0], com2[1][0], com2[2][0])
                medio_intervalo[3].update({color:(com2[0][1][1]-com2[0][1][0])})
        col = tuple(sorted([color for color in promedios]))
        medias = tuple([promedios[c] for c in col])
        __colores.append(col)
        graficarx.append(medias)
        graficary.append(col)
        graficartitulos.append('Boardingtime medio')

        #cols = sorted(colores+['Rojo'])
        for i in range(len(graficartitulos)):
            cols = __colores[i]
            posicion_y = np.arange(len(graficarx[i]))
            rects = plt.barh(posicion_y, graficarx[i], align = "center", color = [co[c] for c in cols if c in co], xerr=[medio_intervalo[i][c] for c in cols if c in medio_intervalo[i]],  ecolor='black')
            plt.yticks(posicion_y, graficary[i])
            plt.xlabel(graficartitulos[i]+" - minutos")
            plt.title(graficartitulos[i]+" - rép: {} - box: {} - med_i: {} - c_esp: {}".format(k,n_boxs,n_medicos_iniciales,n_camas_hospitalizacion))
            
            for rect in rects:
                try:
                    width = int(rect.get_width())
                except:
                    width = 0
                zero = ""
                if width%60 < 10:
                    zero = 0
                suffix = 'm={}'.format(width//60)+":{}{}h".format(zero,width%60)
                rankStr = str(width) + suffix
                if (width < 50):        
                    xloc = width + 3    
                    align = 'left'
                    clr = 'black'
                else:
                    xloc = 0.95*width      
                    align = 'right' 
                    clr = 'black'

                yloc = rect.get_y()+rect.get_height()/1.4
                plt.text(xloc, yloc, rankStr, horizontalalignment=align,
                        verticalalignment='center', color=clr)#, weight='bold')

            plt.savefig("{}/ {} ".format(CARPETA,next(ID.paciente))+" "+graficartitulos[i]+"",transparent = False)
            #plt.show()
            plt.close()


        triage="\n triage abiertos: "
        tria = []
        for x,tiempo in monitor_Triage: 
            tria.append(tiempo)
        if len(tria)> 1:
            com2 = st.bayes_mvs(nan_to_numero(tria), alpha=0.95)

        tiempos = []
        comentario="\n espera por doctor primera vez: "
        for x, tiempo in espera_por_doc:
            tiempos.append(tiempo)
        if len(tiempos)>1:
            com3 = st.bayes_mvs(nan_to_numero(tiempos), alpha=0.95)

    with open(CARPETA+"/Replica [autogenerado].txt","w") as file:

        impr2 = ""
        com = st.bayes_mvs(nan_to_numero(cola_media), alpha=0.95)
        impr= "{} replicas con {} Box - {} camas de espera \n".format(k,n_boxs,n_camas_hospitalizacion)
        if len(t)>1:
            u = st.bayes_mvs(nan_to_numero(t), alpha=0.95)
            impr2="\n--\ttiempo medio de espera {} - S^2: {} - S:{}\n--\tcola_media {} - S^2: {} - S: {}\n".format(u[0],u[1][0],u[2][0],com[0],com[1][0],com[2][0])

        cola_promedio(todos_los_tiempos,todas_las_colas,media = com[0][0], replicas = k,box = n_boxs, medi=n_medicos_iniciales, trans = dias_transiente , dias_s = dias_a_simular, CARPETA = CARPETA, n_camas_hospitalizacion= n_camas_hospitalizacion) 
        file.write("\n -------------------------------------------- \n")
        file.write(impr)
        file.write("\n\n** Trunos Médicos : **\n")
        with open(CARPETA+"/temp1.txt","r") as file2:
            for line in file2:
                file.write(line)
        file.write("\n\n** FastTrack : **\n")
        with open(CARPETA+"/temp2.txt","r") as file2:
            contando = 0
            for line in file2:
                file.write(line)
                contando +=1
            if contando == 0:
                file.write("Sin FastTrack\n")

        file.write("\nDías monitoreados : {}\n".format(dias_monitoreados))
        file.write("\n\Comentario: "+COMENTARIO+"\n--- tiempo ejecucion: %s seconds ---\n" % (time.time() - start_time))
        file.write("\nComentario manual: "+COMENTARIO_gen)
        file.write("\nNúmeros NUMEROS_ALEATORIOS_COMUNES: {}".format(NUMEROS_ALEATORIOS_COMUNES))
        file.write(impr2)
        file.write(tiempo_colores_nh)
        file.write(tiempo_colores+"\n")

        #uso_camasHospitalizacion
        file.write("personas por dia y por color que ENTRAN A BOX\n")
        file.write("dia\t\tamarillo\tazul\tnaranja\t\trojo\t\tverde\t\tTOTAL_mes\tPorSemana\n")
        en_una_semana = {kei:0 for kei in ['Amarillo','Azul','Naranja','Rojo','Verde']}


        if len(uso_camasHospitalizacion)>1:
        	cam = st.bayes_mvs(nan_to_numero(uso_camasHospitalizacion), alpha=0.95)
        	file.write("\n\nUso camas de hospitalización: {} - S^2: {} - S: {}\n".format(cam[0],cam[1][0],cam[2][0]))

        if len(uso_boxFastTrack)>1:
        	_fast = st.bayes_mvs(uso_boxFastTrack, alpha=0.95)
        	file.write("Uso camas Box FastTrack: {} - S^2: {} - S: {}\n".format(_fast[0],_fast[1][0],_fast[2][0]))

        if len(todas_PROP)>1:
            prop_total_a_tiempo = st.bayes_mvs(nan_to_numero(todas_PROP), alpha=0.95)
            file.write("\nProporcion a tiempo todos los colores {} - S^2: {} - S: {}\n".format(prop_total_a_tiempo[0],prop_total_a_tiempo[1][0],prop_total_a_tiempo[2][0]))

        for color in  colores:
            if(len(prop[color])>1):
                pro = st.bayes_mvs(nan_to_numero(prop[color]), alpha=0.95)
                file.write("--\tProporcion color {} a tiempo {} - S^2: {} - S: {}\n".format(color,pro[0],pro[1][0],pro[2][0]))
        file.write(triage+" {} - S^2: {} - S: {}".format(com2[0],com2[1][0],com2[2][0]))
        file.write(comentario_bording)
        file.write("\n")

    with open("Replicas [autogenerado].txt","a") as file:
    	with open(CARPETA+"/Replica [autogenerado].txt","r") as file2:
    		for line in file2:
    			file.write(line)

