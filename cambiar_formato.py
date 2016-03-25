
def cambiar(path, path_out = "REPORTE APTO PARA DISCO.txt"):
	lineas = []

	with open(path,"r") as file:
		for line in file:
			l = line.split("	")
			IDM = ""
			if "Medico" in l[5]:
				IDM = int(l[5][6])
				l[5] = "Medico"+l[5][7:]
			if "Paciente" in l[5]:
				desde =l[5].index("Paciente")+8
				hasta = desde
				while hasta < len(l[5]):
					if l[5][hasta].isdigit():
						hasta+=1
					else:
						break
				ID = int(l[5][desde:hasta])
				l[5] = l[5][:desde]+ l[5][hasta:]

			if "Medico" in l[5] and l[5].index("Medico") == 0:
				recurso = "Medico"
			else:
				recurso = "Paciente"
			l[5] = l[5].split()[1:]

			if " ".join(l[5])[-4].isdigit():
				l[5] = l[5][:-2]
			l[5] =" ".join(l[5])
			if "," in l[5]:
				indice = l[5].index(",")
				hasta = indice
				desde = hasta-1
				while desde >0:
					if l[5][desde].isdigit() or l[5][desde]==".":
						desde-=1
					else:
						break
				l[5] = l[5][:desde]+ l[5][hasta:]
			if IDM != "":
				IDM = ID
				ID = ""
			lineas.append("{}	{}	{}	{}	{}\n".format(ID,IDM,recurso,l[0],"".join(l[5])))


	with open(path_out,"w") as file:
		for linea in lineas:
			file.write(linea)
"""
for i in range(1):
	cambiar("belen.txt","belen DISCO.txt")
"""