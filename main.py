from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QFrame
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np


Cv = 0.718
Cp = 1.005 
gamma = Cp / Cv
divisiones= 100

def encontrar_pf_adiabatico(Vo,Vf,Po):
    Pf = Po * ((Vo / Vf) ** gamma)
    return Pf

def encontrar_valores_termo(p1,v1,delta_v,delta_p,gamma,n):
    v3=v1
    v4=v3
    v2=v1+delta_v
    v5=v2
    p2=p1
    p_12= np.linspace(p1,p2,n)
    v_12= np.linspace(v1,v2,n)
    v_23= np.linspace(v2,v3,n)
    p_23= [encontrar_pf_adiabatico(v2, v, p2) for v in v_23]
    p3= encontrar_pf_adiabatico(v2, v3, p2)
    p4=p3+delta_p
    v_34= np.linspace(v3,v4,n)
    p_34= np.linspace(p3,p4,n)
    v_45= np.linspace(v4,v5,n)
    p_45= [encontrar_pf_adiabatico(v4, v, p4) for v in v_45]
    p5= encontrar_pf_adiabatico(v4, v5, p4)
    p_52= np.linspace(p5,p2,n)
    v_52= np.linspace(v5,v2,n)
    return v2,v3,v4,v5,p2,p3,p4,p5,p_12,p_23,p_34,p_45,p_52,v_12,v_23,v_34,v_45,v_52



class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)

        self.frames = {}

        for i in range(1, 7):
            frame = self.findChild(QFrame, f'f_{i}')
            
            # Crear una figura de matplotlib y un canvas para cada QFrame
            figure = Figure(figsize=(5, 4), dpi=100)
            canvas = FigureCanvas(figure)
            
            # Crear un layout para el QFrame y agregar el canvas
            frame_layout = QVBoxLayout()
            frame.setLayout(frame_layout)
            frame_layout.addWidget(canvas)
            
            # Ajustar el tamaño del canvas para que llene el frame
            canvas.setSizePolicy(1, 1)  # Expande el canvas para llenar el QFrame
            canvas.updateGeometry()
    
            # Guardar la figura y el canvas en un diccionario
            self.frames[f'f_{i}'] = (figure, canvas)
        
        # Configurar los spin boxes y sliders
        for i in range(1, 5):
            spin_min = getattr(self, f"mi_{i}")
            spin_max = getattr(self, f"ma_{i}")
            slider = getattr(self, f"s_{i}")
            line_input = getattr(self, f"l_{i}")

            spin_min.valueChanged.connect(self.valor_spin_min)
            spin_max.valueChanged.connect(self.valor_spin_max)
            slider.valueChanged.connect(self.valor_slider)
            
            self.actualizar_slider(i)


        # Inicializar los gráficos
        self.grafico_1_2()  # Se dibuja en el frame f_1
        self.grafico_2_3()  # Se dibuja en el frame f_2
        self.grafico_3_4()  # Se dibuja en los frames f_3, f_4, f_5, y f_6
        self.grafico_4_5()  # Se dibuja en los frames f_3, f_4, f_5, y f_6
        self.grafico_5_2()  # Se dibuja en los frames f_3, f_4, f_5, y f_6
        self.grafico_otto()


        # Conectar el cambio en el QLineEdit l_1 con el método grafico_2_3
        self.l_1.textChanged.connect(self.grafico_1_2)
        self.l_1.textChanged.connect(self.grafico_2_3)
        self.l_1.textChanged.connect(self.grafico_3_4)
        self.l_1.textChanged.connect(self.grafico_4_5)
        self.l_1.textChanged.connect(self.grafico_5_2)
        self.l_1.textChanged.connect(self.grafico_otto)


        self.l_2.textChanged.connect(self.grafico_1_2)
        self.l_2.textChanged.connect(self.grafico_2_3)
        self.l_2.textChanged.connect(self.grafico_3_4)
        self.l_2.textChanged.connect(self.grafico_4_5)
        self.l_2.textChanged.connect(self.grafico_5_2)
        self.l_2.textChanged.connect(self.grafico_otto)


        self.l_3.textChanged.connect(self.grafico_1_2)
        self.l_3.textChanged.connect(self.grafico_2_3)
        self.l_3.textChanged.connect(self.grafico_3_4)
        self.l_3.textChanged.connect(self.grafico_4_5)
        self.l_3.textChanged.connect(self.grafico_5_2)
        self.l_3.textChanged.connect(self.grafico_otto)

        self.l_4.textChanged.connect(self.grafico_1_2)
        self.l_4.textChanged.connect(self.grafico_2_3)
        self.l_4.textChanged.connect(self.grafico_3_4)
        self.l_4.textChanged.connect(self.grafico_4_5)
        self.l_4.textChanged.connect(self.grafico_5_2)
        self.l_4.textChanged.connect(self.grafico_otto)




    def valor_slider(self, valor):
        slider = self.sender()
        n_slider = slider.objectName()
        n = int(n_slider.split("_")[1])

        label_n = getattr(self, f"l_{n}")
        label_n.setText(str(valor))
        print(n)

    def valor_spin_min(self, valor):
        spin_min = self.sender()
        n_spin_min = spin_min.objectName()
        n = int(n_spin_min.split("_")[1])

        spin_max = getattr(self, f"ma_{n}")
        slider = getattr(self, f"s_{n}")

        if valor >= spin_max.value():
            spin_max.setValue(valor + 1)

        slider.setMinimum(valor)
        slider.setValue(max(slider.value(), valor))
        
        print(f"Spin Min: {valor}, Spin Max Ajustado: {spin_max.value()}")

    def valor_spin_max(self, valor):
        spin_max = self.sender()
        n_spin_max = spin_max.objectName()
        n = int(n_spin_max.split("_")[1])

        spin_min = getattr(self, f"mi_{n}")
        slider = getattr(self, f"s_{n}")

        if valor <= spin_min.value():
            spin_max.setValue(spin_min.value() + 1)

        slider.setMaximum(valor)
        slider.setValue(min(slider.value(), valor))

        print(f"Spin Max: {valor}, Spin Min: {spin_min.value()}")

    def actualizar_slider(self, i):
        spin_min = getattr(self, f"mi_{i}")
        spin_max = getattr(self, f"ma_{i}")
        slider = getattr(self, f"s_{i}")

        slider.setMinimum(spin_min.value())
        slider.setMaximum(spin_max.value())
        slider.setValue(spin_min.value())

    def grafico_1_2(self):
        try:
            p1 = float(self.l_1.text())
            v1 = float(self.l_2.text())
            delta_v = float(self.l_3.text())  
            delta_p = float(self.l_4.text())   
        except ValueError:
            print("Por favor, ingresa valores válidos.")
            return

        valores= encontrar_valores_termo(p1,v1,delta_v,delta_p,gamma, divisiones)
        # Datos para el gráfico
        x_values = valores[13]
        y_values = valores[8]

        # Obtener la figura y el canvas para el frame f_2
        figure, canvas = self.frames['f_2']
        figure.clear()

        # Crear un subplot y ajustar los márgenes
        ax = figure.add_subplot(111)
        figure.subplots_adjust(left=0.18, right=0.98, top=0.9, bottom=0.175)

        # Graficar los datos
        ax.plot(x_values, y_values, marker='o')
        ax.set_title('Proceso 1-->2')
        ax.set_xlabel('Volumen')
        ax.set_ylabel('Presión')

        # Ajustar etiquetas y títulos para que no se tapen
        ax.tick_params(axis='both', which='major', labelsize=10)

        # Actualizar el canvas para mostrar el gráfico
        canvas.draw()


    def grafico_2_3(self):
        try:
            p1 = float(self.l_1.text())
            v1 = float(self.l_2.text())
            delta_v = float(self.l_3.text())  
            delta_p = float(self.l_4.text())   
        except ValueError:
            print("Por favor, ingresa valores válidos.")
            return

        valores= encontrar_valores_termo(p1,v1,delta_v,delta_p,gamma, divisiones)
        # Datos para el gráfico
        x_values = valores[14]
        y_values = valores[9]
    
        # Obtener la figura y el canvas para el frame f_2
        figure, canvas = self.frames['f_3']
        figure.clear()

        # Crear un subplot y ajustar los márgenes
        ax = figure.add_subplot(111)
        figure.subplots_adjust(left=0.18, right=0.98, top=0.9, bottom=0.175)

        # Graficar los datos
        ax.plot(x_values, y_values, marker='o')
        ax.set_title('Proceso 2-->3')
        ax.set_xlabel('Volumen')
        ax.set_ylabel('Presión')

        # Ajustar etiquetas y títulos para que no se tapen
        ax.tick_params(axis='both', which='major', labelsize=10)

        # Actualizar el canvas para mostrar el gráfico
        canvas.draw()



    def grafico_3_4(self):
        try:
            p1 = float(self.l_1.text())
            v1 = float(self.l_2.text())
            delta_v = float(self.l_3.text())  
            delta_p = float(self.l_4.text())   
        except ValueError:
            print("Por favor, ingresa valores válidos.")
            return

        valores= encontrar_valores_termo(p1,v1,delta_v,delta_p,gamma, divisiones)
        # Datos para el gráfico
        x_values = valores[15]
        y_values = valores[10]

        # Obtener la figura y el canvas para el frame f_2
        figure, canvas = self.frames['f_4']
        figure.clear()

        # Crear un subplot y ajustar los márgenes
        ax = figure.add_subplot(111)
        figure.subplots_adjust(left=0.18, right=0.98, top=0.9, bottom=0.175)


        # Graficar los datos
        ax.plot(x_values, y_values, marker='o')
        ax.set_title('Proceso 3-->4')
        ax.set_xlabel('Volumen')
        ax.set_ylabel('Presión')

        # Ajustar etiquetas y títulos para que no se tapen
        ax.tick_params(axis='both', which='major', labelsize=10)

        # Actualizar el canvas para mostrar el gráfico
        canvas.draw()

    def grafico_4_5(self):
        try:
            p1 = float(self.l_1.text())
            v1 = float(self.l_2.text())
            delta_v = float(self.l_3.text())  
            delta_p = float(self.l_4.text())   
        except ValueError:
            print("Por favor, ingresa valores válidos.")
            return

        valores= encontrar_valores_termo(p1,v1,delta_v,delta_p,gamma, divisiones)
        # Datos para el gráfico
        x_values = valores[16]
        y_values = valores[11]


        # Obtener la figura y el canvas para el frame f_2
        figure, canvas = self.frames['f_5']
        figure.clear()

        # Crear un subplot y ajustar los márgenes
        ax = figure.add_subplot(111)
        figure.subplots_adjust(left=0.18, right=0.98, top=0.9, bottom=0.175)


        # Graficar los datos
        ax.plot(x_values, y_values, marker='o')
        ax.set_title('Proceso 4-->5')
        ax.set_xlabel('Volumen')
        ax.set_ylabel('Presión')

        # Ajustar etiquetas y títulos para que no se tapen
        ax.tick_params(axis='both', which='major', labelsize=10)

        # Actualizar el canvas para mostrar el gráfico
        canvas.draw()


    def grafico_5_2(self):
        try:
            p1 = float(self.l_1.text())
            v1 = float(self.l_2.text())
            delta_v = float(self.l_3.text())  
            delta_p = float(self.l_4.text())   
        except ValueError:
            print("Por favor, ingresa valores válidos.")
            return

        valores= encontrar_valores_termo(p1,v1,delta_v,delta_p,gamma, divisiones)
        # Datos para el gráfico
        x_values = valores[17]
        y_values = valores[12]

        # Obtener la figura y el canvas para el frame f_2
        figure, canvas = self.frames['f_6']
        figure.clear()

        # Crear un subplot y ajustar los márgenes
        ax = figure.add_subplot(111)
        figure.subplots_adjust(left=0.18, right=0.98, top=0.9, bottom=0.175)

        # Graficar los datos
        ax.plot(x_values, y_values, marker='o')
        ax.set_title('Proceso 5-->2')
        ax.set_xlabel('Volumen')
        ax.set_ylabel('Presión')

        # Ajustar etiquetas y títulos para que no se tapen
        ax.tick_params(axis='both', which='major', labelsize=10)

        # Actualizar el canvas para mostrar el gráfico
        canvas.draw()


    def grafico_otto(self):
        try:
            p1 = float(self.l_1.text())
            v1 = float(self.l_2.text())
            delta_v = float(self.l_3.text())  
            delta_p = float(self.l_4.text())   
        except ValueError:
            print("Por favor, ingresa valores válidos.")
            return

        valores= encontrar_valores_termo(p1,v1,delta_v,delta_p,gamma, divisiones)

        x_values = []
        y_values = []
        for i in range(1, 6):
            x_values = np.concatenate((x_values, valores[12 + i]))
            y_values = np.concatenate((y_values, valores[7 + i]))

        figure, canvas = self.frames['f_1']
        figure.clear()

        ax = figure.add_subplot(111)
        ax.clear()
        figure.subplots_adjust(left=0.18, right=0.98, top=0.9, bottom=0.175)

        ax.plot(x_values, y_values, marker='o')
        ax.set_title('Ciclo Otto')
        ax.set_xlabel('Volumen')
        ax.set_ylabel('Presión')

        ax.tick_params(axis='both', which='major', labelsize=10)

        canvas.draw()




if __name__ == "__main__":
    app = QApplication([])
    window = MyWindow()
    window.show()
    app.exec_()
