##########################################
#           Author: TechOGR              #
#   Gmail: onelguilarte858@gmail.com     #
##########################################


# Import
import os, sys, time, segno, pyaimp, socket
import pyautogui as gui
import pyttsx3 as ttx
# From
from plyer import notification
from threading import Thread
from getpass import getuser
from PyQt5.QtWidgets import (
    QMainWindow,
    QLabel, 
    QPushButton,
    QLineEdit,
    QGraphicsDropShadowEffect,
    QDialog,
    QMessageBox,
    QApplication
)
from PyQt5.QtGui import (
    QIcon,
    QColor,
    QPixmap
)
from PyQt5.QtCore import (
    Qt,
    QRect
)

# Clase Encargada de manipular el AIMP
class AutoBot:
    # Metodo Constructor
    def __init__(self) -> None:
        self.comando = "tasklist"

        self.salida = os.popen(self.comando)
        self.datos_salida = str(self.salida.readlines())

        self.lista_procesos = self.datos_salida.split()

        self.bot_audio = ttx.init(debug=True)
        self.bot_audio.setProperty("rate",160)
        self.bot_audio.setProperty("volume",1.0)

        self.operations = Thread(target=self.operaciones,args=[0])
        self.operations.start()

        try:
            self.aimp = pyaimp.Client()
        except:
            pass

    # Operaciones
    def operaciones(self,n=None):
        if n == 1:
            self.aimp.pause()
            self.bot_audio.say("Reproduccion Pausada")
            self.bot_audio.runAndWait()
        elif n == 2:
            self.bot_audio.say("Reproduccion Iniciada")
            self.bot_audio.runAndWait()
            self.aimp.play()
            self.notify_info_songs()
        elif n == 3:
            self.aimp.stop()
            self.bot_audio.say("Reproduccion Detenido")
            self.bot_audio.runAndWait()
            self.notify_info_songs()
        elif n == 4:
            self.aimp.set_shuffled(True)
            self.bot_audio.say("Modo Aleatorio Activado")
            self.bot_audio.runAndWait()
        elif n == 5:
            self.aimp.set_shuffled(False)
            self.bot_audio.say("Modo Aleatorio Desactivado")
            self.bot_audio.runAndWait()
        elif n == 6:
            self.aimp.set_muted(True)
            self.bot_audio.say("Sin Sonido")
            self.bot_audio.runAndWait()
        elif n == 7:
            self.aimp.set_muted(False)
            self.bot_audio.say("Con Sonido")
            self.bot_audio.runAndWait()
        elif n == 8:
            self.aimp.next()
            self.bot_audio.say("Siguiente")
            self.bot_audio.runAndWait()
            self.notify_info_songs()
        elif n == 9:
            self.aimp.prev()
            self.bot_audio.say("Anterior")
            self.bot_audio.runAndWait()
            self.notify_info_songs()
        else:
            pass
        
    def notify_info_songs(self):
        info_song = list(self.aimp.get_current_track_info().values())
        titulo = info_song[12]
        
        if titulo == "":
            notification.notify(
                title = "Detenido",
                app_name = "Bot",
                message = "Subscribete a mi canal de YouTube 'TechOGR'",
                timeout = 10,
                app_icon = "D:/Fotos/Imagenes/Mi_Logo.ico"
            )
        else:
            notification.notify(
                title = "Reproduciendo...",
                app_name = "Bot",
                message = titulo,
                timeout = 2,
                app_icon = "D:/Fotos/Imagenes/Mi_Logo.ico"
            )

    # Metodo para buscar la musica
    def abrir_musica(self,nombre,velocidad):
        self.if_exist()

        vel = 0
        if velocidad == 1:
            vel = 2
        elif velocidad == 2:
            vel = 1
        elif velocidad == 3:
            vel = 0.5

        if self.if_exist() == True:
            gui.move(2000,50,vel)
            gui.move(0,120,vel)
            gui.click()
            time.sleep(1)
            gui.hotkey("ctrl","f")
            time.sleep(0.7)
            gui.write(nombre,vel-(vel/2))
            time.sleep(1)
            gui.hotkey("enter")
        else:
            sms = Mensajes_Emergentes()
            sms.sms_error("Verifique que el AIMP esté corriendo")

    def if_exist(self):
        for index, proceso in enumerate(self.lista_procesos):
            if "AIMP.exe" in proceso:
                return True
            elif (index == len(self.lista_procesos)):
                return False

# Ventana Principal
class Ventana(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        icono = QIcon("D:/Fotos/Imagenes/Mi_Logo.png")
        self.velocidad = 3
        self.setObjectName("Frame")
        self.setFixedSize(500,130)
        #Qt.WindowStaysOnTopHint
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowTitle("Find Music on AIMP")
        self.setVisible(True)
        self.setStyleSheet("#Frame{background-color: #181818;}")
        self.setWindowIcon(icono)
        self.init_components()

        self.bot_audio = ttx.init(debug=True)
        self.bot_audio.setProperty("rate",160)
        self.bot_audio.setProperty("volume",1.0)

        try:
            self.aimp = pyaimp.Client()
            self.aimp_opened()
        except:
            self.aimp_closed()
            sys.exit()

        #Clase para Mensajes Emergentes
        self.sms = Mensajes_Emergentes()

        #Obteniendo el nombre de usuario de la PC
        self.nombre_usuario = getuser()

        ########### Textos para decir al Inicio ###############
        self.primer_texto = f"""Hola, {self.nombre_usuario}, Primero, para evitar problemas espere a que yo termine de hablar,
        segundo, cuando yo hable, el foco de su ventana debe estar en este programa,
        tercero, fui creado por..."""
        
        self.segundo_texto = f"""Siguelo en Youtube, ahora si, empecemos.
        Hola, Bienvenido al centro de Aqui mismo,
        Puede ver las opciones con lo que escribiré allí,
        mantenga el foco en esta ventana,
        por ahora me voy, Guapo, pero luego nos veremos de nuevo."""
        ########################################################

        #Bot que actua
        self.bot = AutoBot();

        #Estableciendo Valores para la conexion
        self.host_server = socket.gethostbyname(socket.gethostname())
        self.puerto = 111
        self.direccion = f"{str(self.host_server)}"

        #Instanciando Socket
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #Creando e Iniciando Hilos
        self.create_server = Thread(target=self.servidor)
        self.say_intro = Thread(target=self.decir_intro)
        self.show_notify = Thread(target=self.create_notify, args=["Bienvenida","Iniciando Software"])
        self.create_server.daemon = True
        self.create_server.start()
        self.say_intro.daemon = True
        self.say_intro.start()
        self.show_notify.daemon = True
        self.show_notify.start()
        
        # Creando el codigo QR con la IP de la PC
        self.crear_qr()
        
        # Valor por defecto para cada cosa a Decir
        self.texto = ""

    # Metodo de inicializacion de los componentes graficos
    def init_components(self):
        self.estilos()

        #Etiqueta Titulo
        self.label_title = QLabel(parent=self)
        self.label_title.setText("Find Music on AIMP")
        self.label_title.setGeometry(160,10,190,30)
        self.label_title.setVisible(True)
        self.label_title.setStyleSheet(self.estilo_label_title)

        #Boton de Busqueda
        self.btn = QPushButton("Search",parent=self)
        self.btn.setGeometry(QRect(420,55,70,50))
        self.btn.setStyleSheet(self.estilo_btn)
        self.btn.setVisible(True)
        self.btn.setGraphicsEffect(self.btn_shadow)
        self.btn.clicked.connect(self.ejecutar)

        #Boton Minimizar
        self.btn_minimizar = QPushButton(parent=self)
        self.btn_minimizar.setGeometry(QRect(455,10,30,30))
        self.btn_minimizar.setVisible(True)
        self.btn_minimizar.setObjectName("btn_minimizar")
        self.btn_minimizar.setText("-")
        self.btn_minimizar.setStyleSheet(self.estilo_btn_accion)
        self.btn_minimizar.clicked.connect(self.function_btn_minimize)

        #Boton Cerrar
        self.btn_cerrar = QPushButton(parent=self)
        self.btn_cerrar.setGeometry(QRect(10,10,30,30))
        self.btn_cerrar.setVisible(True)
        self.btn_cerrar.setObjectName("btn_cerrar")
        self.btn_cerrar.setText("x")
        self.btn_cerrar.setStyleSheet(self.estilo_btn_accion)
        self.btn_cerrar.clicked.connect(self.function_btn_close)

        #Edit_Text
        self.txt_to_find = QLineEdit(parent=self)
        self.txt_to_find.setGeometry(10,55,390,50)
        self.txt_to_find.setVisible(True)
        self.txt_to_find.setFocus(True)
        self.txt_to_find.setStyleSheet(self.estilo_line_edit)
        self.txt_to_find.setGraphicsEffect(self.line_edit_shadow)

    # Estilos para los componentes graficos
    def estilos(self):
        self.btn_shadow = QGraphicsDropShadowEffect()
        self.btn_shadow.setBlurRadius(25)
        self.btn_shadow.setOffset(0,0)
        self.btn_shadow.setColor(QColor(0,0,0))

        self.line_edit_shadow = QGraphicsDropShadowEffect()
        self.line_edit_shadow.setBlurRadius(25)
        self.line_edit_shadow.setOffset(0,0)
        self.line_edit_shadow.setColor(QColor(0,0,0))

        self.estilo_btn = """* {
            background-color: #181818;
            color: #0f0;
            border: 2px outset #202020;
            margin: 0;
            padding: 0;
            font-size: 20px;
        }
        *:hover {
            border: 2px inset #202020;
            font-size: 18px;
        }
        """

        self.estilo_line_edit = """QLineEdit {
            background-color: #181818;
            color: #0f0;
            border: 2px outset #202020;
            margin: 0;
            padding: 0;
            font-family: 'Comic Sans';
            font-size: 20px;
        }"""

        self.estilo_btn_accion = """#btn_minimizar {
            color: black;
            background: yellow;
            font-size: 25px;
            padding: 0;
            border: 1px;
            border-style: inset;
            border-radius: 10px;
        }
        #btn_minimizar:hover {
            font-size: 20px;
            border-radius: 12px;
        }

        #btn_cerrar {
            color: black;
            background: red;
            font-size: 20px;
            padding: 0;
            border: 1px;
            border-style: inset;
            border-radius: 10px;
        }
        #btn_cerrar:hover {
            font-size: 20px;
            border-radius: 12px;
        }
        """

        self.estilo_label_title = """* {
            color: #0f0;
            background-color: #181818;
            font: 20px 'Comic Sans MS';
        }"""
        
    # En caso de que esté cerrado el reproductor
    def aimp_closed(self):
        self.bot_audio.say("Por Favor, Verifique que tenga abireto el Reproductor de Audio, AIMP, Luego, Reinicie este Programa")
        self.bot_audio.runAndWait()

    # En Caso de que esté abierto el reproductor
    def aimp_opened(self):
        self.bot_audio.say("OK")
        self.bot_audio.runAndWait()

    #Metodo del sayintro
    def decir_intro(self):
        decir = "Hola de Nuevo"
        comando = os.popen("cmd /c echo %Bot%").readlines()
        salida_comando = comando[0]

        #print(salida_comando)
        if "set" in salida_comando:
            self.bot_audio.say(decir)
            self.bot_audio.runAndWait()
            gui.write("$help",0.2)
        else:
            self.bot_audio.say(self.primer_texto)
            self.bot_audio.runAndWait()
            gui.write("TechOGR",0.3)
            self.bot_audio.say(self.segundo_texto)
            self.bot_audio.runAndWait()
            self.txt_to_find.setText("")
            gui.write("$help",0.2)
            os.popen("setx Bot set")

        h = Thread(target=self.reproducir)
        h.daemon = True
        h.start()
                    
        # while True:
        #     if len(self.texto) <= 0:
        #         continue
        #     else:
        #         self.cosas_para_decir(self.texto)
        
    def reproducir(self):
        while len(self.texto) != 0:
            self.cosas_para_decir(self.texto)

    # Metodo para crear Notificaciones
    def create_notify(self,title,sms):
        notification.notify(
            title = title,
            app_name = "Bot",
            message = sms,
            timeout = 1,
            app_icon = "D:/Fotos/Imagenes/Mi_Logo.ico"
        )
        
    # Metodo que crea el QR-Code
    def crear_qr(self):
        qr = segno.make(self.host_server,micro=False,version=7)
        qr.save(
            f"C:/Users/{self.nombre_usuario}/AppData/Local/ip.png",
            scale=6,
            # dark = "#0f0",
            # light = "#000",
            # alignment_light = "green",
            # alignment_dark = "#0f0",
            # finder_light = "green",
            # finder_dark = "#0f0"
        )
    
    # hilo para el server local
    def servidor(self):
        self.s.bind((self.host_server,self.puerto))
        self.s.listen(2)
        #print(f"Escuhando en.. {self.host_server}:{self.puerto}")

        cli, addr = self.s.accept() # instanciando address del socket

        # Recibiendo Datos y Evaluando Peticiones
        while True:
            data_recv = cli.recv(1024).decode()

            if data_recv.endswith("play_pause"):
                if self.aimp.get_playback_state() == pyaimp.PlayBackState.Playing:
                    self.bot.operaciones(1)
                elif self.aimp.get_playback_state() == pyaimp.PlayBackState.Paused or self.aimp.get_playback_state() == pyaimp.PlayBackState.Stopped:
                    self.bot.operaciones(2)
            elif data_recv.endswith("stop_stop"):
                self.bot.operaciones(3)
            elif data_recv.endswith("next_next"):
                self.bot.operaciones(8)
            elif data_recv.endswith("back_back"):
                self.bot.operaciones(9)
            elif data_recv.endswith("mute_yes"):
                self.bot.operaciones(6)
            elif data_recv.endswith("mute_no"):
                self.bot.operaciones(7)
            elif data_recv.endswith("vol_0"):
                self.aimp.set_volume(0)
            elif data_recv.endswith("vol_1"):
                self.aimp.set_volume(10)
            elif data_recv.endswith("vol_2"):
                self.aimp.set_volume(20)
            elif data_recv.endswith("vol_3"):
                self.aimp.set_volume(30)
            elif data_recv.endswith("vol_4"):
                self.aimp.set_volume(40)
            elif data_recv.endswith("vol_5"):
                self.aimp.set_volume(50)
            elif data_recv.endswith("vol_6"):
                self.aimp.set_volume(60)
            elif data_recv.endswith("vol_7"):
                self.aimp.set_volume(70)
            elif data_recv.endswith("vol_8"):
                self.aimp.set_volume(80)
            elif data_recv.endswith("vol_9"):
                self.aimp.set_volume(90)
            elif data_recv.endswith("vol_10"):
                self.aimp.set_volume(100)
            elif data_recv.endswith("random_yes"):
                self.bot.operaciones(4)
            elif data_recv.endswith("random_no"):
                self.bot.operaciones(5)
            elif data_recv.endswith("OGR_RGO"):
                dev = data_recv.replace("OGR_RGO","")
                devi = dev.replace("#","")
                devic = devi.replace("$", "")
                device = devic.replace("modelo_device"," ")
                #print(device)
                var_tmp = ""
                for i, v in enumerate(device):
                    if i == 0:
                        continue
                    else:
                        var_tmp += v
                element_from_model = var_tmp.split()
                #print(element_from_model)
                if len(var_tmp) > 0 and len(element_from_model) == 2:
                    try:
                        self.bot_audio.say(f"Dispositivo..., {element_from_model[1]} {element_from_model[0]} .Conectado")
                        self.bot_audio.runAndWait()
                    except RuntimeError:
                        self.bot_audio.say(f"Dispositivo..., {element_from_model[1]} {element_from_model[0]} .Conectado")
                        self.bot_audio.runAndWait()
                elif len(var_tmp) > 0 and "Xiaomi" in var_tmp:
                    try:
                        self.bot_audio.say(f"Dispositivo..., {element_from_model[2]} {element_from_model[0]} {element_from_model[1]}. Conectado...")
                        self.bot_audio.runAndWait()
                    except RuntimeError:
                        self.bot_audio.say(f"Dispositivo..., {element_from_model[2]} {element_from_model[0]} {element_from_model[1]}. Conectado...")
                        self.bot_audio.runAndWait()
            else:
                continue

    ############-Permite mover la ventana-#####################
    def mousePressEvent(self,event):
        if event.button() == Qt.LeftButton:
            self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.dragPosition)
            event.accept()
    ############----Junto con Este-----#######################

    # Asignando la tecla Escape para finalizar el Programa
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.cosas_para_decir("Adios, Guapo")
            self.close()
            self.create_server._stop()
            e.accept()

    # Cuando es precionado el Boton Cerrar
    def function_btn_close(self):
        self.cosas_para_decir("Adios, Guapo")
        self.create_server._stop()
        self.say_intro._stop()
        self.close()
        
    # Cuando es precionado el Boton Minimizar
    def function_btn_minimize(self):
        self.cosas_para_decir("Minimizado")
        self.showMinimized()
        
        
    # Encargado de Evaluar y Ejecutar Comandos
    def ejecutar(self):

        self.txt_line = self.txt_to_find.text().lower().replace(" ","")
        
        if len(self.txt_line) <= 0:
            self.sms.sms_error("Escribe algo :)")
        elif self.txt_line == "$qr":
            qr_show = ShowQRCode(self)
            qr_show.show()
        elif self.txt_line == "$pause":
            self.bot.operaciones(1)
        elif self.txt_line == "$play":
            self.bot.operaciones(2)
        elif self.txt_line == "$stop":
            self.bot.operaciones(3)
        elif self.txt_line == "$random_yes":
            self.bot.operaciones(4)
        elif self.txt_line == "$random_no":
            self.bot.operaciones(5)
        elif self.txt_line == "$mute_yes":
            self.bot.operaciones(6)
        elif self.txt_line == "$mute_no":
            self.bot.operaciones(7)
        elif self.txt_line == "$next":
            self.bot.operaciones(8)
        elif self.txt_line == "$prev":
            self.bot.operaciones(9)
        elif self.txt_line.startswith("$") and self.txt_line != "$help" and self.txt_line != "$next" and self.txt_line != "$prev" and self.txt_line != "$mute_no" and self.txt_line != "$mute_yes" and self.txt_line != "$random_yes" and self.txt_line != "$random_no" and self.txt_line != "$play" and self.txt_line != "$pause" and self.txt_line != "$stop" and self.txt_line != "$lento" and self.txt_line != "$rapido" and self.txt_line != "$normal" and self.txt_line != "$qr":
            self.bot_audio.say("Opcion no valida, Revisa la lista de opciones en el panel de ayuda")
            self.bot_audio.runAndWait()
        elif self.velocidad == 0 and self.txt_line != "$help" and self.txt_line != "$lento" and self.txt_line != "$normal" and self.txt_line != "$rapido" and self.txt_line != "$play" and self.txt_line != "$pause" and self.txt_line != "$stop" and self.txt_line != "$mute_yes" and self.txt_line != "$mute_no" and self.txt_line != "$random_yes" and self.txt_line != "$random_no" and self.txt_line != "$play_pause":
            self.cosas_para_decir("Por favor, establezca una velocidad. para mas ayuda escriba en el cuadro de búsqueda, '$help', lo mismo que le dije al inicio")
        elif self.txt_line == "$help":
            self.cosas_para_decir("Abriendo Panel de Ayuda")
            seting = Help(self.direccion)
            seting.__init__(self.direccion)
            seting.show()
        elif self.txt_line == "$lento":
            self.velocidad = 1
            self.texto = "Velocidad establecida en, 'Lento'"
        elif self.txt_line == "$normal":
            self.texto = "Velocidad establecida en, 'Normal'"
            self.velocidad = 2
        elif self.txt_line == "$rapido":
            self.texto = "Velocidad establecida en, 'Rapdio'"
            self.velocidad = 3
        elif len(self.txt_line) > 0 and self.txt_line != "$help" and self.velocidad != 0 and self.txt_line != "$play" and self.txt_line != "$pause":
            nombre = str(self.txt_to_find.text())
            self.bot.abrir_musica(nombre,self.velocidad)
            self.txt_to_find.setText("")
        self.txt_to_find.setText("")

    # Cosas para Decir :D
    def cosas_para_decir(self,texto=None):
        try:
            self.bot_audio.say(texto)
            self.bot_audio.runAndWait()
            self.texto = "";
        except RuntimeError:
            print("error")


# Clase encargada de Mostrar la Ayuda y los comandos
class Help(QDialog):

    def __init__(self,direccion,*args,**kwargs):
        super(Help,self).__init__(*args, **kwargs)
        icono = QIcon("D:/Fotos/Imagenes/Mi_Logo.png")
        self.setFixedSize(300,650)
        self.setWindowTitle("Help")
        self.setWindowIcon(icono)
        self.setVisible(True)
        self.direction = direccion
        self.initComponents()


    #Inicializando componentes graficos
    def initComponents(self):
        
        self.setStyleSheet("""* {
            background-color: #181818;
        }""")

        self.estilo_label_reproduction = """* {
            color: green;
            font-size: 15px;
            font-family: 'Courier';
            font-style: normal;
        }"""

        #Label_Title_Help
        self.label_id = QLabel(parent=self)
        self.label_id.setGeometry(50,10,250,70)
        self.label_id.setText("Velocidades")
        self.label_id.setVisible(True)
        self.label_id.setStyleSheet("""* {
            color: #0f0;
            font-size: 30px;
            font-family: 'Lemon';
            font-style: normal;
        }""")

        #label address
        self.title_address = QLabel(parent=self)
        self.title_address.setGeometry(35,580,250,30)
        self.title_address.setText("Write in your Phone")
        self.title_address.setVisible(True)
        self.title_address.setStyleSheet("""* {
            color: #0f0;
            font-size: 20px;
            font-family: 'Lemon';
            font-style: normal;
        }""")

        self.label_address = QLabel(parent=self)
        self.label_address.setGeometry(60,611,250,30)
        self.label_address.setText(self.direction)
        self.label_address.setVisible(True)
        self.label_address.setStyleSheet("""* {
            color: #0f0;
            font-size: 20px;
            font-family: 'Lemon';
            font-style: normal;
        }""")

        #Labels like options list
        #Option 1
        self.label_1 = QLabel(parent=self)
        self.label_1.setGeometry(10,80,300,50)
        self.label_1.setText("Lento = $lento")
        self.label_1.setVisible(True)
        self.label_1.setStyleSheet("""* {
            color: green;
            font-size: 30px;
            font-family: 'Courier';
            font-style: normal;
        }""")

        #Option 2
        self.label_2 = QLabel(parent=self)
        self.label_2.setGeometry(10,120,300,50)
        self.label_2.setText("Normal = $normal")
        self.label_2.setVisible(True)
        self.label_2.setStyleSheet("""* {
            color: green;
            font-size: 30px;
            font-family: 'Courier';
            font-style: normal;
        }""")

        #Option 3
        self.label_3 = QLabel(parent=self)
        self.label_3.setGeometry(10,160,300,50)
        self.label_3.setText("Rápido = $rapido")
        self.label_3.setVisible(True)
        self.label_3.setStyleSheet("""* {
            color: green;
            font-size: 30px;
            font-family: 'Courier';
            font-style: normal;
        }""")

        #Label Option of Reproduction
        self.label_reproduction = QLabel(parent=self)
        self.label_reproduction.setGeometry(30,200,250,70)
        self.label_reproduction.setText("Reproduccion")
        self.label_reproduction.setVisible(True)
        self.label_reproduction.setStyleSheet("""* {
            color: #0f0;
            font-size: 30px;
            font-family: 'Lemon';
            font-style: normal;
        }""")

        #Option 4
        self.label_4 = QLabel(parent=self)
        self.label_4.setGeometry(10,270,300,30)
        self.label_4.setText("Play = $play")
        self.label_4.setVisible(True)
        self.label_4.setStyleSheet(self.estilo_label_reproduction)
        #Option 5
        self.label_5 = QLabel(parent=self)
        self.label_5.setGeometry(10,300,300,30)
        self.label_5.setText("Puse = $pause")
        self.label_5.setVisible(True)
        self.label_5.setStyleSheet(self.estilo_label_reproduction)
        #Option 6
        self.label_6 = QLabel(parent=self)
        self.label_6.setGeometry(10,330,300,30)
        self.label_6.setText("Stop = $stop")
        self.label_6.setVisible(True)
        self.label_6.setStyleSheet(self.estilo_label_reproduction)
        #Option 7
        self.label_7 = QLabel(parent=self)
        self.label_7.setGeometry(10,360,300,30)
        self.label_7.setText("Random_ON = $random_yes")
        self.label_7.setVisible(True)
        self.label_7.setStyleSheet(self.estilo_label_reproduction)
        #Option 8
        self.label_8 = QLabel(parent=self)
        self.label_8.setGeometry(10,390,300,30)
        self.label_8.setText("Random_OFF = $random_no")
        self.label_8.setVisible(True)
        self.label_8.setStyleSheet(self.estilo_label_reproduction)
        #Option 9
        self.label_9 = QLabel(parent=self)
        self.label_9.setGeometry(10,420,300,30)
        self.label_9.setText("Mute_ON = $mute_yes")
        self.label_9.setVisible(True)
        self.label_9.setStyleSheet(self.estilo_label_reproduction)
        #Option 10
        self.label_10 = QLabel(parent=self)
        self.label_10.setGeometry(10,450,300,30)
        self.label_10.setText("Mute_OFF = $mute_no")
        self.label_10.setVisible(True)
        self.label_10.setStyleSheet(self.estilo_label_reproduction)
        #Option 11
        self.label_11 = QLabel(parent=self)
        self.label_11.setGeometry(10,480,300,30)
        self.label_11.setText("Next = $next")
        self.label_11.setVisible(True)
        self.label_11.setStyleSheet(self.estilo_label_reproduction)
        #Option 12
        self.label_12 = QLabel(parent=self)
        self.label_12.setGeometry(10,510,300,30)
        self.label_12.setText("Previous = $prev")
        self.label_12.setVisible(True)
        self.label_12.setStyleSheet(self.estilo_label_reproduction)
        #Option 13
        self.label_13 = QLabel(parent=self)
        self.label_13.setGeometry(10,540,300,30)
        self.label_13.setText("QR-Code = $qr")
        self.label_13.setVisible(True)
        self.label_13.setStyleSheet(self.estilo_label_reproduction)

# Emergents Messages
class Mensajes_Emergentes(QMessageBox):
    def __init__(self):
        QMessageBox.__init__(self)
        self.setFixedSize(100,100)
    
    def sms_error(self,mensaje):
        self.about(self,"Error", mensaje)

    def sms_velocidad(self,txt):
        self.about(self,"Informacion",txt)

    def info(self,ip,puerto):
        self.about(self,"Informacion",f"IP: {ip}\nPuerto: {puerto}")


# Clase para mostrar el codigo QR
class ShowQRCode(QDialog):
    def __init__(self, *args, **kwargs):
        super(ShowQRCode,self).__init__(*args, **kwargs)
        user = getuser()
        self.img_pix = QPixmap(f"C:/Users/{user}/AppData/Local/ip.png")
        self.setFixedSize(315,315)
        self.setWindowIcon(QIcon(self.img_pix))
        self.setWindowTitle("QR_IP")
        self.setVisible(True)
        self.setWindowFlag(Qt.FramelessWindowHint)
        #self.setVisible(True)
        self.label = QLabel(self)
        self.label.setVisible(True)
        self.label.setPixmap(self.img_pix)
        self.label.setGeometry(0,0,300,300)
        

# Proceso Inicial
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Ventana()
    window.show()
    sys.exit(app.exec_())