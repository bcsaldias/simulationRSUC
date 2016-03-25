NUMEROS_ALEATORIOS_COMUNES = "False"
with open("temp.txt") as file:
	lineas = []
	for line in file:
		lineas.append(line)
	NUMEROS_ALEATORIOS_COMUNES = lineas[5]
NUMEROS_ALEATORIOS_COMUNES = bool(NUMEROS_ALEATORIOS_COMUNES.replace("\n",""))
#print(NUMEROS_ALEATORIOS_COMUNES)

import matplotlib.pyplot as plt

def cola_promedio(tiempos,colas, media, replicas,box,medi, trans, dias_s, CARPETA, n_camas_hospitalizacion):
	colas.sort(key = lambda x: len(x))
	cuantas = 10
	minimo = len(colas[0])

	cola_media = []
	for i in range(minimo):
		suma = 0
		cuantos = 0
		j = 0
		for cola in colas[:cuantas]:
			if len(cola)>i and tiempos[j][i]>=trans*60*24:
				suma+= cola[i]
				cuantos+=1
				j+=1
		cola_media.append(suma/cuantos)

	tiempos_medios = []
	for i in range(minimo):
		suma = 0
		cuantos = 0
		for tiempo in tiempos[:cuantas]:
			if len(tiempo)>i and tiempo[i]>=trans*60*24:
				suma+= tiempo[i]
				cuantos+=1
		tiempos_medios.append(suma/cuantos)

	plt.figure()
	plt.xlabel('Transcurso del tiempo en minutos')
	plt.ylabel('Cola media')
	plt.plot(tiempos_medios,cola_media, color='pink')
	path = "Cola espera por Box - mu: {} - r_im: {} - box: {} - med_i: {} - camas_e: {}".format(round(media,2),cuantas,box,medi, n_camas_hospitalizacion)
	plt.title(path)
	plt.savefig("{}/ {} ".format(CARPETA,next(ID.paciente))+" "+"Cola media en el tiempo",transparent = False)
	#plt.show()
	plt.close()


class ID:
	def id_paciente():
		i = 0
		while True:
			yield i
			i+=1
	
	def id_medico():
		i = 0
		while True:
			yield i
			i+=1
	medico = id_medico()
	paciente = id_paciente()


"""
IMPORTAR SOLO SI QUIERO CON COMUNES !!!
"""

from generadores import (generador_primera_vez,generador_segunda_vez,generador_f_amarillo,generador_f_naranja,
						generador_f_rojo,generador_f_verde,generador_ResCer,generador_ScannC,generador_RadiogT,generador_Lab,
						generador_get_tipo_im,generador_get_color,
						generador_tiempo_triage,generador_tiempo_medico_FT,generador_tiempo_espera_enfermera,generador_get_se_hospitaliza,
						generador_tiempos_examenes_1,generador_tiempos_examenes_2,generador_doble_examen,generador_tiempo_hasta_otro_paciente,
						generador_fast_amarillo,generador_uniforme_hospitalizacion)


from math import log, sqrt
import scipy.stats as st
from numpy.random import gamma, triangular, uniform, weibull as w, lognormal
from random import triangular,  expovariate as exponential
max_esperar_bording = 5*60
max_esperar_examen = 2*60



def tiempo_triage():
	if not NUMEROS_ALEATORIOS_COMUNES:
		return triangular(3,5,3)
	else:
		return next(generador_tiempo_triage)

def tiempo_medico_FT():
	if not NUMEROS_ALEATORIOS_COMUNES:
		return triangular(15,20,21)
	else:
		return next(generador_tiempo_medico_FT)

def tiempo_espera_enfermera():
	if not NUMEROS_ALEATORIOS_COMUNES:
		return triangular(4, 5, 5)
	else:
		return next(generador_tiempo_espera_enfermera)

def get_se_hospitaliza():
	if not NUMEROS_ALEATORIOS_COMUNES:
		return round(uniform(0, 1), 6)
	else:
		return next(generador_get_se_hospitaliza)

def tiempos_examenes_1():
	if not NUMEROS_ALEATORIOS_COMUNES:
		return round(uniform(0, 1), 6)
	else:
		return next(generador_tiempos_examenes_1)

def tiempos_examenes_2():
	if not NUMEROS_ALEATORIOS_COMUNES:
		return round(uniform(0, 1), 6)
	else:
		return next(generador_tiempos_examenes_2)

def doble_examen():
	if not NUMEROS_ALEATORIOS_COMUNES:
		return uniform(0,1)
	else:
		return next(generador_doble_examen)

def tiempo_hasta_otro_paciente(t_llegada):
	#if not NUMEROS_ALEATORIOS_COMUNES:
		return exponential((t_llegada/60))
	#else:
		#return next(generador_tiempo_hasta_otro_paciente)


def fast_amarillo():
	if not NUMEROS_ALEATORIOS_COMUNES:
		return uniform(0,1)
	else:
		return next(generador_fast_amarillo)


def uniforme_hospitalizacion():
	if not NUMEROS_ALEATORIOS_COMUNES:
		return uniform(0, 1)
	else:
		return next(generador_uniforme_hospitalizacion)



def primera_vez(): 
	#if not NUMEROS_ALEATORIOS_COMUNES:
		return triangular(12, 20, 25)
	#else:		#return next(generador_primera_vez)



def segunda_vez():
	#if not NUMEROS_ALEATORIOS_COMUNES:
		return triangular(12, 16, 20)
	#else:
		#return next(generador_segunda_vez)


def f_amarillo():
	if not NUMEROS_ALEATORIOS_COMUNES:
		return min(gamma(1.5,128),max_esperar_bording)
	else:
		return next(generador_f_amarillo)

def f_azul(): return 0

def f_naranja():
	if not NUMEROS_ALEATORIOS_COMUNES:
		return min(gamma(1.15,101),max_esperar_bording)
	else:
		return next(generador_f_naranja)


def f_rojo(): 
	if not NUMEROS_ALEATORIOS_COMUNES:
		return min(gamma(0.75,111),max_esperar_bording)
	else:
		return next(generador_f_rojo)


def f_verde():
	if not NUMEROS_ALEATORIOS_COMUNES:
		return min(gamma(1.72,139),max_esperar_bording)
	else:
		return next(generador_f_verde)


def ResCer():
	if not NUMEROS_ALEATORIOS_COMUNES:
		return min( 82 + 209*w(0.953),2*max_esperar_examen)
	else:
		return next(generador_ResCer)

def ScannC():  
	if not NUMEROS_ALEATORIOS_COMUNES:
		mu = 95.4
		sig = 84.7
		xi2 = log((sig/mu)**2+1)
		cambio_lambda = log(mu)-0.5*xi2
		return min(18 + lognormal(cambio_lambda, sqrt(xi2)), max_esperar_examen)
	else:
		return next(generador_ScannC)


def RadiogT(): 
	if not NUMEROS_ALEATORIOS_COMUNES:
		return min(19 + 78*w(1.97),max_esperar_examen)  
	else:
		return next(generador_RadiogT)


def Lab():
	if not NUMEROS_ALEATORIOS_COMUNES:
		return triangular(25, 60, 60)
	else:
		return next(generador_Lab)




tiempo_medico_atencion = {0:primera_vez ,1:segunda_vez, 2:segunda_vez}
prob_imagen = {"Amarillo":0.2628,"Azul":0.0607 , "Naranja":0.5458 , "Rojo":0.5972, "Verde":0.0749}
prob_tipo_imagen= [("ResCer",0.27714),("ScannC",0.162357),("RadiogT",0.56049)]
prob_laboratorio = {"Amarillo":0.2842,"Azul":0.0477 , "Rojo":0.7222, "Naranja": 0.5816, "Verde":0.0966}

tiempos_examen = {"ResCer":ResCer,"ScannC":ScannC,"RadiogT":RadiogT, "LAB":Lab}

prob_hospitalizacion = {"Amarillo":0.13616213,"Azul":0 , "Naranja":0.31754422 , "Rojo":0.61111111, "Verde":0.0252513}
bording_time = {"Amarillo":f_amarillo,"Azul":f_azul , "Naranja":f_naranja , "Rojo":f_rojo, "Verde":f_verde}

prob_doble = {"Amarillo":0.2,"Azul":0 , "Naranja":0.3 , "Rojo":0.05, "Verde":0.2}




def get_tipo_im(probs = prob_tipo_imagen):
	if not NUMEROS_ALEATORIOS_COMUNES:
		u = round(uniform(0,1),6)
	else:
		u = next(generador_get_tipo_im)

	if u <= probs[0][1]:
		return probs[0][0]
	if u <= probs[0][1] + probs[1][1]:
		return probs[1][0]
	return probs[2][0]

def get_color(probs):
	if not NUMEROS_ALEATORIOS_COMUNES:
		u = round(uniform(0,1),6)
	else:
		u = next(generador_get_color)

	if u <= probs[0]:
		return "Amarillo"
	if u <= sum(probs[0:2]):
		return "Azul"
	if u <= sum(probs[0:3]):
		return "Naranja"
	if u <= sum(probs[0:4]):
		return "Rojo"
	return "Verde"







import xlrd
def leer_informacion(path ="Recursos/Simulacion.xls"):
	book = xlrd.open_workbook(path)
	probabilidades = book.sheet_by_index(0)
	tasas = book.sheet_by_index(1)

	dias = [[],[],[],[],[],[],[]] 												#print(dias[6][1][4]) #domingo, 1-2, verde
	
	s = 1
	for dia in range(7):
		e = s+5
		for i in range(24):
		    p = probabilidades.row_slice(rowx=i+4,start_colx=s,end_colx=e)
		    valores = [v.value for v in p]
		    dias[dia].append(valores)
		s+=7
	
	tas = []																	#print(tas[23][5]) #23-00, sabado
	for i in range(24):
		x = tasas.row_slice(rowx=i+1,start_colx=1,end_colx=8)
		tas.append([a.value for a in x])
		
	return dias, tas



duracion_dia = 60*24
duracion_semana = 60*24*7
duracion_mes = 60*24*31

class Scheduler:
	
	def dia(time):
		time = time+1
		tiempo_semana = time%duracion_semana
		for i in range(7):
			if tiempo_semana-duracion_dia <= 0:
				return i
			tiempo_semana-=duracion_dia

	
	def hora(time):
		time = time +1
		tiempo_semana = time%duracion_semana
		tiempo_dia = tiempo_semana%duracion_dia
		for i in range(24):
			if tiempo_dia-60 <= 0:
				return i
			tiempo_dia-=60
