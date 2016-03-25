import sys
from PyQt4 import QtGui, QtCore
import os
import subprocess 



class Interfaz(QtGui.QWidget):
    
    def __init__(self):
        super(Interfaz, self).__init__()
        self.n_boxs = "0"
        self.n_fast =  "0"
        self.n_camas =  "0"
        self.packs = []
        self.setWindowIcon(QtGui.QIcon('Recursos/icon.png'))        
        self.initUI()
        self.aleatorios_comunes = True
        self.dias_a_monitorear = "7"

    def initUI(self):      

        self.lbl = QtGui.QLabel("Comentario :", self)
        self.lbl.move(840, 35)
        self.edit = QtGui.QTextEdit(self)
        self.edit.setFixedWidth(200)
        self.edit.setFixedHeight(50)
        self.edit.move(840,55)
        self.edit.setText("Este es el caso base")

        self.num = QtGui.QCheckBox('Números aleatorios comunes', self)
        self.num.move(340,50+30+30)
        self.num.stateChanged.connect(self.changeTitle)
        self.num.setCheckState(QtCore.Qt.Checked)
       
        self.monit = QtGui.QLabel("Monitorear :", self)
        self.monitorear = QtGui.QComboBox(self)
        for i in range(0,8):
            self.monitorear.addItem("{}".format(i))#(340,)
        self.monitorear.setCurrentIndex(7)  
        self.monitorear.move(420, 60+50+45)
        self.monit.move(340,50+30+30+50)
        self.monitorear.activated[str].connect(self.onMonitorear)   


        self.lbl = QtGui.QLabel("Número de Box :", self)
        self.box = QtGui.QComboBox(self)
        for i in range(0,16):
            self.box.addItem("{}".format(i))
        self.box.move(200, 45+30+30)
        self.lbl.move(50, 50+30+30)
        self.box.setCurrentIndex(11)      
         
        self.lbl = QtGui.QLabel("Fast-Track", self)
        self.lbl.move(50, 50+30+30+25+30)

        self.turnos_fastTrack = []       
        
        #forma = [0 ,50+50+150+50+60+80 +150]
        #forma = [0 ,50+50+150+50+60+80 +150]
        self.horarios([0])


        self.lbl = QtGui.QLabel("Número de camas de espera :", self)
        self.camas = QtGui.QComboBox(self)
        for i in range(0,6):
            self.camas.addItem("{}".format(i))#(340,)
        self.camas.move(540, 60)
        self.lbl.move(340, 35+30)
        self.camas.activated[str].connect(self.onCamas)        

        self.lbl = QtGui.QLabel("Número de réplicas :", self)
        self.lbl.move(50, 35+30)
        self.replicas = QtGui.QLineEdit(self)
        self.replicas.setText("100")
        self.replicas.setFixedWidth(80)
        self.replicas.move(200, 30+30)
        #qle.textChanged[str].connect(self.onChanged)

        self.lbl = QtGui.QLabel("Turnos Médicos", self)
        self.lbl.move(50+50+150+50+60+80 +250, 50+30+30+25+30)

        pal = 0
        for pa in [("l,m,w,j,v,s,d",0,1,3),("l,m,w,j,v,s,d",1,9,2),("l,m,w,j,v,s,d",9,24,3)]:
        	for cos in range(len(pa)):
        		self.packs[pal][cos].setText("{}".format(pa[cos]))
        	pal+=1

        self.setGeometry(50, 100, 1150, 600)
        self.setWindowTitle('Parámetros Simulación Urgencia UC')
        

        btn = QtGui.QPushButton('Simular', self)
        btn.setStyleSheet("background-color: lightgreen")
        btn.clicked.connect(self.onButton)
        btn.move(350+80+95, 5)   #500+200+130
        #btn = QtGui.QPushButton('Simular', self)
        #btn.setStyleSheet("background-color: lightgreen")
        #btn.clicked.connect(self.onButton)
        #btn.move(350+80+95, 500+200+130)   #

        btn2 = QtGui.QPushButton('Otro Escenario', self)
        btn2.setStyleSheet("background-color: orange")
        btn2.clicked.connect(self.otra)
        btn2.move(350+75, 5)  

        #self.btn3 = QtGui.QPushButton('Agregar Cupos Horarios', self)
        #self.btn3.setStyleSheet("background-color: orange")
        #self.btn3.clicked.connect(self.mas_horarios)
        #self.btn3.move(270.9, 5) 

        self.show()
        self.out = QtGui.QLabel("", self)
        self.ou = QtGui.QLabel("", self)


    def otra(self):
        subprocess.Popen("python Interfaz.py", shell=True)

    def mas_horarios(self):
    	self.btn3.hide()
    	self.horarios([50+50+150+50+60+80 +150])

    def horarios(self,forma):
        self.setGeometry(600, 100, 550+80+forma[0], 750+130)
        labels = ["Días","Hora inicio","Hora fin","Cantidad","Núm Médic","Prop Amarillos"]
        tam = [50,50+50+50+50,50+50+80+50+50,50+50+150+50+60,50+50+150+50+60+80, 5+50+50+150+50+60+80+80]
        for doble in forma:
            for i in range(len(labels)):
                self.lbl = QtGui.QLabel(labels[i], self)
                self.lbl.move(tam[i]+doble, 50+30+70+15+30)
                self.lbl.show()
            for i in range(12):
                dias = QtGui.QLineEdit(self)
                dias.move(50+doble, 50+30+90+i*30+15+30)
                dias.setFixedWidth(110)
                dias.show()

                inicio = QtGui.QLineEdit(self)
                inicio.move(50+50+50+50+doble, 50+30+90+i*30+15+30)
                inicio.setFixedWidth(60)
                inicio.show()

                fin = QtGui.QLineEdit(self)
                fin.move(50+50+50+50+80+doble, 50+30+90+i*30+15+30)
                fin.setFixedWidth(60)
                fin.show()

                cantid = QtGui.QLineEdit(self)
                cantid.move(50+50+150+50+60+doble, 50+30+90+i*30+15+30)
                cantid.setFixedWidth(60)
                cantid.show()

                medic = QtGui.QLineEdit(self)
                medic.move(50+50+150+50+60+80+doble, 50+30+90+i*30+15+30)
                medic.setFixedWidth(60)
                medic.show()

                amarill = QtGui.QLineEdit(self)
                amarill.move(50+50+150+50+60+80+85+doble, 50+30+90+i*30+15+30)
                amarill.setFixedWidth(60)
                amarill.show()

                self.turnos_fastTrack.append([dias,inicio,fin,cantid,medic,amarill])

        labels = ["Días","Hora inicio","Hora fin","Cantidad"]
        tam = [50,50+50+50+50, 50+50+80+50+50, 50+50+150+50+60]
        forma = [50+150+50+60+80 +150+100]
        for doble in forma:
            for i in range(len(labels)):
                self.lbl = QtGui.QLabel(labels[i], self)
                self.lbl.move(tam[i]+doble, 50+30+70+15+30)
                self.lbl.show()

            for i in range(12):
                dias = QtGui.QLineEdit(self)
                dias.move(50+doble, 50+30+90+i*30+15+30)
                dias.setFixedWidth(110)
                dias.show()

                inicio = QtGui.QLineEdit(self)
                inicio.move(50+50+50+50+doble, 50+30+90+i*30+15+30)
                inicio.setFixedWidth(60)
                inicio.show()

                fin = QtGui.QLineEdit(self)
                fin.move(50+50+50+50+80+doble, 50+30+90+i*30+15+30)
                fin.setFixedWidth(60)
                fin.show()

                cantid = QtGui.QLineEdit(self)
                cantid.move(50+50+150+50+60+doble, 50+30+90+i*30+15+30)
                cantid.setFixedWidth(60)
                cantid.show()

                self.packs.append([dias,inicio,fin,cantid])

    def changeTitle(self, state):
        if state == QtCore.Qt.Checked:
            self.setWindowTitle('Parámetros Simulación Urgencia UC - núm comunes')
            self.aleatorios_comunes = True
        else:
            self.setWindowTitle('Parámetros Simulación Urgencia UC')
            self.aleatorios_comunes = ""

    def onButton(self):
        self.out.hide()
        self.ou.hide()


        if not self.replicas.text().isdigit():
            raise TypeError("El numero de replicas no es un numero")
        if int(self.replicas.text()) < 2:
            raise ValueError("El numero de replicas debe ser mayor a 1")

        reply = QtGui.QMessageBox.question(self, 'Inicio de Simulación',
            "¿Estás seguro de iniciar la Simulación?", "Si", "No")

        if reply == 0:
            newpath = r'OUTPUTS {}'.format(len(os.listdir())) 
            if not os.path.exists(newpath): os.makedirs(newpath)
            self.out = QtGui.QLabel("Los Outputs de esta simulación se guardan en la carpeta {}".format(newpath), self)
            self.out.move(50, 500+260+60)
            self.out.show()

            with open("temp.txt".format(newpath),"w") as temp:
                temp.write("{}\n".format(newpath))
                temp.write(self.replicas.text()+"\n")
                temp.write("{}\n".format(self.box.currentIndex()))
                temp.write("{}\n".format(self.n_camas))
                temp.write("{}\n".format(self.edit.toPlainText().replace("\n"," || ")))
                temp.write("{}\n".format(self.aleatorios_comunes))
                temp.write("{}\n".format(self.dias_a_monitorear))

            with open("{}/temp1.txt".format(newpath),"w") as temp:
                for i in self.packs:
                    if len(i[0].text())>0:
                        if int(i[2].text())<int(i[1].text()):
                            raise ValueError("Turnos Medicos : La hora de fin no puede ser menor a la hora de inicio")
                        temp.write("{}\t{}\t{}\t{}\n".format(i[0].text(),i[1].text(),i[2].text(),i[3].text()))

            with open("{}/temp2.txt".format(newpath),"w") as temp:
                for i in self.turnos_fastTrack:
                    if len(i[0].text())>0:
                        if int(i[2].text())<int(i[1].text()):
                            raise ValueError("FastTrack : La hora de fin no puede ser menor a la hora de inicio")
                        temp.write("{}\t{}\t{}\t{}\t{}\t{}\n".format(i[0].text(),i[1].text(),i[2].text(),i[3].text(),i[4].text(),i[5].text()))
            

            self.ou = QtGui.QLabel("Ha finalizado la simulación", self)
            self.ou.move(50, 500+340)
            self.ou.show()

            os.system('python ensayo.py')


            #__SIMULAR__(int(self.replicas.text()), n_boxs, n_camas, n_fast, turnos)
           

    def onCamas(self, text):
        self.n_camas = text

    def onMonitorear(self, text):
        self.dias_a_monitorear = text
        


def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Interfaz()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

