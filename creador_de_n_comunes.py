#paths = ['g_primera_vez','g_segunda_vez','g_f_amarillo','g_f_naranja','g_f_rojo','g_f_verde','g_ResCer','g_ScannC','g_RadiogT','g_Lab','g_get_tipo_im','g_get_color',
#		'g_tiempo_triage','g_tiempo_medico_FT','g_tiempo_espera_enfermera','g_get_se_hospitaliza','g_tiempos_examenes_1','g_tiempos_examenes_2',
#		'g_doble_examen','g_tiempo_hasta_otro_paciente','g_fast_amarillo','g_uniforme_hospitalizacion']
from numpy.random import gamma, triangular, uniform, weibull as w, lognormal
from random import triangular,  expovariate as exponential
max_esperar_bording = 5*60
max_esperar_examen = 2*60
from math import log, sqrt

def tiempo_triage():
	return triangular(3,5,3)

def tiempo_medico_FT():
	return triangular(15,20,21)

def tiempo_espera_enfermera():
	return triangular(4, 5, 5)

def get_se_hospitaliza():
	return round(uniform(0, 1), 6)

def tiempos_examenes_1():
	return round(uniform(0, 1), 6)

def tiempos_examenes_2():
	return round(uniform(0, 1), 6)

def doble_examen():
	return uniform(0,1)

#def tiempo_hasta_otro_paciente(t_llegada):
#	return exponential((t_llegada/60))

def fast_amarillo():
	return uniform(0,1)

def uniforme_hospitalizacion():
	return uniform(0, 1)
		
def primera_vez(): 
	return triangular(12, 15, 20)

def segunda_vez():
	return triangular(12, 16, 20)

def f_amarillo():
	return min(gamma(1.5,128),max_esperar_bording)

def f_naranja():
	return min(gamma(1.15,101),max_esperar_bording)

def f_rojo(): 
	return min(gamma(0.75,111),max_esperar_bording)

def f_verde():
	return min(gamma(1.72,139),max_esperar_bording)

def ResCer():
	return min( 82 + 209*w(0.953),2*max_esperar_examen)

def ScannC():  
	mu = 95.4
	sig = 84.7
	xi2 = log((sig/mu)**2+1)
	cambio_lambda = log(mu)-0.5*xi2
	return min(18 + lognormal(cambio_lambda, sqrt(xi2)), max_esperar_examen)

def RadiogT(): 
	return min(19 + 78*w(1.97),max_esperar_examen)  

def Lab():
	return triangular(25, 45, 60)

def get_tipo_im():
	return round(uniform(0,1),6)

def get_color():
	return round(uniform(0,1),6)


listas = {
	'g_tiempo_medico_FT': tiempo_medico_FT,
	'tiempo_triage':tiempo_triage,
	'tiempo_espera_enfermera':tiempo_espera_enfermera,
	'get_se_hospitaliza':get_se_hospitaliza,
	'tiempos_examenes_1':tiempos_examenes_1,
	'tiempos_examenes_2':tiempos_examenes_2,
	'doble_examen':doble_examen,
	'fast_amarillo':fast_amarillo,
	'uniforme_hospitalizacion':uniforme_hospitalizacion,
	'primera_vez':primera_vez,
	'segunda_vez':segunda_vez,
	'f_amarillo':f_amarillo,
	'f_naranja':f_naranja,
	'f_rojo':f_rojo,
	'f_verde':f_verde,
	'ResCer':ResCer,
	'ScannC':ScannC,
	'RadiogT':RadiogT,
	'Lab':Lab,
	'get_tipo_im':get_tipo_im,
	'get_color':get_color,

}

for path in listas:
	with open("n_comunes/"+path+".txt","w") as document:
		for i in range(9000000):
			document.write("{}\n".format(listas[path]()))
