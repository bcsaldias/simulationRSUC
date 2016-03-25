def gen_primera_vez():
	with open("n_comunes/g_primera_vez.txt",'r') as file:
		for line in file:
			yield float(line.replace("\n","").strip())

def gen_segunda_vez():
	with open("n_comunes/g_segunda_vez.txt",'r') as file:
		for line in file:
			yield float(line.replace("\n","").strip())

def gen_f_amarillo():
	with open("n_comunes/g_f_amarillo.txt",'r') as file:
		for line in file:
			yield float(line.replace("\n","").strip())
		
def gen_f_naranja():
	with open("n_comunes/g_f_naranja.txt",'r') as file:
		for line in file:
			yield float(line.replace("\n","").strip())
			
def gen_f_rojo():
	with open("n_comunes/g_f_rojo.txt",'r') as file:
		for line in file:
			yield float(line.replace("\n","").strip())
			
def gen_f_verde():
	with open("n_comunes/g_f_verde.txt",'r') as file:
		for line in file:
			yield float(line.replace("\n","").strip())
			
def gen_ResCer():
	with open("n_comunes/g_ResCer.txt",'r') as file:
		for line in file:
			yield float(line.replace("\n","").strip())
			
def gen_ScannC():
	with open("n_comunes/g_ScannC.txt",'r') as file:
		for line in file:
			yield float(line.replace("\n","").strip())
			
def gen_RadiogT():
	with open("n_comunes/g_RadiogT.txt",'r') as file:
		for line in file:
			yield float(line.replace("\n","").strip())
			
def gen_Lab():
	with open("n_comunes/g_Lab.txt",'r') as file:
		for line in file:
			yield float(line.replace("\n","").strip())
			
def gen_get_tipo_im():
	with open("n_comunes/g_get_tipo_im.txt",'r') as file:
		for line in file:
			yield float(line.replace("\n","").strip())
			
def gen_get_color():
	with open("n_comunes/g_get_color.txt",'r') as file:
		for line in file:
			yield float(line.replace("\n","").strip())
			

generador_primera_vez = gen_primera_vez()
generador_segunda_vez = gen_segunda_vez()
generador_f_amarillo = gen_f_amarillo()
generador_f_naranja = gen_f_naranja()
generador_f_rojo = gen_f_rojo()
generador_f_verde = gen_f_verde()
generador_ResCer = gen_ResCer()
generador_ScannC = gen_ScannC()
generador_RadiogT = gen_RadiogT()
generador_Lab = gen_Lab()
generador_get_tipo_im = gen_get_tipo_im()
generador_get_color = gen_get_color()




def gen_tiempo_triage():
	with open("n_comunes/g_tiempo_triage.txt",'r') as file:
		for line in file:
			yield float(line.replace("\n","").strip())
			
def gen_tiempo_medico_FT():
	with open("n_comunes/g_tiempo_medico_FT.txt",'r') as file:
		for line in file:
			yield float(line.replace("\n","").strip())
			
def gen_tiempo_espera_enfermera():
	with open("n_comunes/g_tiempo_espera_enfermera.txt",'r') as file:
		for line in file:
			yield float(line.replace("\n","").strip())
			
def gen_get_se_hospitaliza():
	with open("n_comunes/g_get_se_hospitaliza.txt",'r') as file:
		for line in file:
			yield float(line.replace("\n","").strip())
			
def gen_tiempos_examenes_1():
	with open("n_comunes/g_tiempos_examenes_1.txt",'r') as file:
		for line in file:
			yield float(line.replace("\n","").strip())
			
def gen_tiempos_examenes_2():
	with open("n_comunes/g_tiempos_examenes_2.txt",'r') as file:
		for line in file:
			yield float(line.replace("\n","").strip())
			
def gen_doble_examen():
	with open("n_comunes/g_doble_examen.txt",'r') as file:
		for line in file:
			yield float(line.replace("\n","").strip())
			
def gen_tiempo_hasta_otro_paciente():
	with open("n_comunes/g_tiempo_hasta_otro_paciente.txt",'r') as file:
		for line in file:
			yield float(line.replace("\n","").strip())
			
def gen_fast_amarillo():
	with open("n_comunes/g_fast_amarillo.txt",'r') as file:
		for line in file:
			yield float(line.replace("\n","").strip())
			
def gen_uniforme_hospitalizacion():
	with open("n_comunes/g_uniforme_hospitalizacion.txt",'r') as file:
		for line in file:
			yield float(line.replace("\n","").strip())
			
generador_tiempo_triage = gen_tiempo_triage()
generador_tiempo_medico_FT = gen_tiempo_medico_FT()
generador_tiempo_espera_enfermera = gen_tiempo_espera_enfermera()
generador_get_se_hospitaliza = gen_get_se_hospitaliza()
generador_tiempos_examenes_1 = gen_tiempos_examenes_1()
generador_tiempos_examenes_2 = gen_tiempos_examenes_2()
generador_doble_examen = gen_doble_examen()
generador_tiempo_hasta_otro_paciente = gen_tiempo_hasta_otro_paciente()
generador_fast_amarillo = gen_fast_amarillo()
generador_uniforme_hospitalizacion = gen_uniforme_hospitalizacion()