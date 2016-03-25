def borrar_transiente(origen, destino, linea):
	with open(origen,"r") as file:
		i = 0
		with open(destino,"w") as file1:
			for line in file:
				if i>linea:
					file1.write(line)
				i+=1

