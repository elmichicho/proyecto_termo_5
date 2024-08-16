import numpy as np
import matplotlib.pyplot as plt
from pint import UnitRegistry

# Inicializar el registro de unidades
ureg = UnitRegistry()

# Definir las constantes
V1 = 1 * ureg.meter**3
V2 = 27 * ureg.meter**3
P1 = 243 * ureg.pascal
Cv = 0.718 * ureg.kilojoule / (ureg.kilogram * ureg.kelvin)
Cp = 1.005 * ureg.kilojoule / (ureg.kilogram * ureg.kelvin)

# Calcular gamma
gamma = Cp / Cv

# Crear un rango de volúmenes
V_12 = np.linspace(V1, V2, 100)

# Función para encontrar P2
def encontrar_P2(V1, V2, P1):
    P2 = P1 * ((V1 / V2) ** gamma)
    return P2

# Calcular P2 para cada volumen
P_2 = [encontrar_P2(V1, V, P1) for V in V_12]

# Extraer los valores numéricos de P_2
P_2_numeric = np.array([p.magnitude for p in P_2])
V_12_numeric = V_12.magnitude

# Graficar resultados
plt.plot(V_12_numeric, P_2_numeric, label='Curva adiabática')
plt.xlabel('Volumen V (m³)')
plt.ylabel('Presión P (Pa)')
plt.title('Relación entre Volumen y Presión en un Proceso Adiabático')
plt.grid(True)
plt.legend()
plt.show()
