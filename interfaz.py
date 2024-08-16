from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QFrame
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np


def encontrar_pf_adiabatico(Vo,Vf,Po):
    Cv = 0.718
    Cp = 1.005 
    gamma = Cp / Cv
    Pf = Po * ((Vo / Vf) ** gamma)
    return Pf


class MyWindow(QMainWindow):
    global V1, V2, V3, V4, V5, P1, P2, P3, P4, P5
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


        # Conectar el cambio en el QLineEdit l_1 con el método grafico_2_3
        self.l_1.textChanged.connect(self.grafico_1_2)
        self.l_1.textChanged.connect(self.grafico_2_3)
        self.l_1.textChanged.connect(self.grafico_3_4)
        self.l_1.textChanged.connect(self.grafico_4_5)
        self.l_1.textChanged.connect(self.grafico_5_2)

        self.l_2.textChanged.connect(self.grafico_1_2)
        self.l_2.textChanged.connect(self.grafico_2_3)
        self.l_2.textChanged.connect(self.grafico_3_4)
        self.l_2.textChanged.connect(self.grafico_4_5)
        self.l_2.textChanged.connect(self.grafico_5_2)

        self.l_3.textChanged.connect(self.grafico_1_2)
        self.l_3.textChanged.connect(self.grafico_2_3)
        self.l_3.textChanged.connect(self.grafico_3_4)
        self.l_3.textChanged.connect(self.grafico_4_5)
        self.l_3.textChanged.connect(self.grafico_5_2)

        self.l_4.textChanged.connect(self.grafico_1_2)
        self.l_4.textChanged.connect(self.grafico_2_3)
        self.l_4.textChanged.connect(self.grafico_3_4)
        self.l_4.textChanged.connect(self.grafico_4_5)
        self.l_4.textChanged.connect(self.grafico_5_2)




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
            presion = float(self.l_1.text())
            V1 = float(self.l_2.text())
            delta_v = float(self.l_3.text())   
        except ValueError:
            print("Por favor, ingresa valores válidos.")
            return
        P1=presion
        P2=P1
        V2= V1 + delta_v

        # Obtener la figura y el canvas para el frame f_2
        figure, canvas = self.frames['f_2']
        figure.clear()

        # Crear un subplot y ajustar los márgenes
        ax = figure.add_subplot(111)
        figure.subplots_adjust(left=0.18, right=0.98, top=0.9, bottom=0.175)

        # Datos para el gráfico
        x_values = np.linspace(V1, V2, 100)
        y_values = np.linspace(P1, P2, 100)

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
            P2 = float(self.l_1.text())
            V1 = float(self.l_2.text())
            delta_v_12 = float(self.l_3.text())
        except ValueError:
            print("Por favor, ingresa valores válidos.")
            return
        V2= V1 + delta_v_12
        V3=V1
        V_23= np.linspace(V2, V3, 100)

        P_34= [encontrar_pf_adiabatico(V2, V, P2) for V in V_23]
        P_3= encontrar_pf_adiabatico(V2,V3,P2)     
        # Obtener la figura y el canvas para el frame f_2
        figure, canvas = self.frames['f_3']
        figure.clear()

        # Crear un subplot y ajustar los márgenes
        ax = figure.add_subplot(111)
        figure.subplots_adjust(left=0.18, right=0.98, top=0.9, bottom=0.175)

        # Datos para el gráfico
        x_values = V_23
        y_values = P_34

        # Graficar los datos
        ax.plot(x_values, y_values, marker='o')
        ax.set_title('Proceso 2-->3')
        ax.set_xlabel('Volumen')
        ax.set_ylabel('Presión')

        # Ajustar etiquetas y títulos para que no se tapen
        ax.tick_params(axis='both', which='major', labelsize=10)

        # Actualizar el canvas para mostrar el gráfico
        canvas.draw()

        print(P_34)


    def grafico_3_4(self):
        try:
            P2 = float(self.l_1.text())
            V1 = float(self.l_2.text())
            delta_v_12 = float(self.l_3.text())
            delta_v_34 = float(self.l_4.text())
        except ValueError:
            print("Por favor, ingresa valores válidos.")
            return
        V3= V1
        V4=V3
        V_34= np.linspace(V3, V4, 100)

        P3= encontrar_pf_adiabatico(V1+delta_v_12, V1, P2)
        P4= P3 + delta_v_34
        P_34= np.linspace(P3, P4, 100)

        # Obtener la figura y el canvas para el frame f_2
        figure, canvas = self.frames['f_4']
        figure.clear()

        # Crear un subplot y ajustar los márgenes
        ax = figure.add_subplot(111)
        figure.subplots_adjust(left=0.18, right=0.98, top=0.9, bottom=0.175)

        # Datos para el gráfico
        x_values = V_34
        y_values = P_34

        # Graficar los datos
        ax.plot(x_values, y_values, marker='o')
        ax.set_title('Proceso 3-->4')
        ax.set_xlabel('Volumen')
        ax.set_ylabel('Presión')

        # Ajustar etiquetas y títulos para que no se tapen
        ax.tick_params(axis='both', which='major', labelsize=10)

        # Actualizar el canvas para mostrar el gráfico
        canvas.draw()

        print(P3)


    def grafico_4_5(self):
        try:
            P2 = float(self.l_1.text())
            V1 = float(self.l_2.text())
            delta_v_12 = float(self.l_3.text())
            delta_v_34 = float(self.l_4.text())
        except ValueError:
            print("Por favor, ingresa valores válidos.")
            return
        V3= V1
        V4=V3
        V5= V4 + delta_v_12

        P_3= encontrar_pf_adiabatico(V1+delta_v_12, V1, P2)
        P_4= P_3 + delta_v_34
        V_45= np.linspace(V4, V5, 100)
        P_45= [encontrar_pf_adiabatico(V4, V, P_4) for V in V_45]

        # Obtener la figura y el canvas para el frame f_2
        figure, canvas = self.frames['f_5']
        figure.clear()

        # Crear un subplot y ajustar los márgenes
        ax = figure.add_subplot(111)
        figure.subplots_adjust(left=0.18, right=0.98, top=0.9, bottom=0.175)

        # Datos para el gráfico
        x_values = V_45
        y_values = P_45

        # Graficar los datos
        ax.plot(x_values, y_values, marker='o')
        ax.set_title('Proceso 4-->5')
        ax.set_xlabel('Volumen')
        ax.set_ylabel('Presión')

        # Ajustar etiquetas y títulos para que no se tapen
        ax.tick_params(axis='both', which='major', labelsize=10)

        # Actualizar el canvas para mostrar el gráfico
        canvas.draw()

        print(P_45)

    def grafico_5_2(self):
        try:
            P2 = float(self.l_1.text())
            V1 = float(self.l_2.text())
            delta_v_12 = float(self.l_3.text())
            delta_v_34 = float(self.l_4.text())
        except ValueError:
            print("Por favor, ingresa valores válidos.")
            return
        
        V3= V1
        V4=V3
        V5= V4 + delta_v_12
        V2=V5

        P3= encontrar_pf_adiabatico(V1+delta_v_12, V1, P2)
        P4= P3 + delta_v_34
        P5= encontrar_pf_adiabatico(V4, V5, P4)

        V_52= np.linspace(V5, V2, 100)
        P_52= np.linspace(P5, P2, 100)

        # Obtener la figura y el canvas para el frame f_2
        figure, canvas = self.frames['f_6']
        figure.clear()

        # Crear un subplot y ajustar los márgenes
        ax = figure.add_subplot(111)
        figure.subplots_adjust(left=0.18, right=0.98, top=0.9, bottom=0.175)

        # Datos para el gráfico
        x_values = V_52
        y_values = P_52

        # Graficar los datos
        ax.plot(x_values, y_values, marker='o')
        ax.set_title('Proceso 5-->2')
        ax.set_xlabel('Volumen')
        ax.set_ylabel('Presión')

        # Ajustar etiquetas y títulos para que no se tapen
        ax.tick_params(axis='both', which='major', labelsize=10)

        # Actualizar el canvas para mostrar el gráfico
        canvas.draw()

        print(P_52)


if __name__ == "__main__":
    app = QApplication([])
    window = MyWindow()
    window.show()
    app.exec_()
