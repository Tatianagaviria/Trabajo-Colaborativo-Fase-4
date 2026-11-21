import logging
from datetime import datetime

fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
print("Fecha y hora del sistema:", fecha_actual)

logging.basicConfig(
    filename="errores.log",
    level=logging.ERROR,
    format="%(asctime)s - %(message)s",
)

class Carro:
    
    _valor_hora = 2000
    
    def __init__(self, color, marca, placa, hora_ingreso, hora_salida):
        self._color = color
        self._marca = marca
        self._placa = placa.upper()
        self._hora_ingreso = hora_ingreso
        self._hora_salida = hora_salida
    
    def horas_a_pagar(self):
        horas = self._hora_salida - self._hora_ingreso
        return horas * self._valor_hora
    
    def calcular_horas_estacionado(self):
        return self._hora_salida - self._hora_ingreso
    
    def verificar_datos(self):
        if self._hora_salida < self._hora_ingreso:
            return False, "La hora de salida no puede ser anterior a la hora de ingreso"
        if self._hora_ingreso < 0 or self._hora_ingreso > 23:
            return False, "La hora de ingreso debe estar entre 0 y 23"
        if self._hora_salida < 0 or self._hora_salida > 23:
            return False, "La hora de salida debe estar entre 0 y 23"
        return True, "Datos verificados correctamente"
    
    def mostrar_informacion(self):
        return (
            "Carro: " + self._color + " " + self._marca + 
            " | Placa: " + self._placa +
            " | Ingreso: " + str(self._hora_ingreso) + ":00" +
            " | Salida: " + str(self._hora_salida) + ":00" +
            " | Horas: " + str(self.calcular_horas_estacionado())
        )

def mostrar_encabezado():
    print("=" * 60)
    print("           SISTEMA DE CONTROL DE PARQUEADERO")
    print("=" * 60)
    print("Valor por hora de estacionamiento: $", Carro._valor_hora, "pesos")
    print("=" * 60)

def mostrar_resumen(lista):
    print("\n" + "=" * 60)
    print("                RESUMEN DEL DIA")
    print("=" * 60)
    
    if len(lista) == 0:
        print("No se registraron vehiculos en esta sesion.")
        return
    
    total_carros = len(lista)
    total_horas = 0
    total_dinero = 0
    
    print("Listado de vehiculos registrados:")
    print("-" * 60)
    
    for posicion, carro in enumerate(lista, 1):
        horas = carro.calcular_horas_estacionado()
        valor = carro.horas_a_pagar()
        total_horas += horas
        total_dinero += valor
        print(str(posicion) + ". " + carro.mostrar_informacion() + " | A pagar: $" + f"{valor:,}")
    
    print("-" * 60)
    print("Total de vehiculos registrados:", total_carros)
    print("Total horas de estacionamiento hoy:", total_horas, "horas")
    print("Total dinero recaudado: $" + f"{total_dinero:,} pesos")
    print("=" * 60)

def registrar_un_carro():
    print("\n--- Nuevo Registro de Vehiculo ---")
    color = input("Ingrese el color del vehiculo: ")
    marca = input("Ingrese la marca del vehiculo: ")
    placa = input("Ingrese la placa del vehiculo: ")
    
    while True:
        try:
            hora_ingreso = int(input("Ingrese hora de ingreso (0-23): "))
            hora_salida = int(input("Ingrese hora de salida (0-23): "))
            break
        except ValueError:
            print("Error: Por favor ingrese solo numeros para las horas.")
            logging.error("Entrada no numerica en horas")
    
    carro_nuevo = Carro(color, marca, placa, hora_ingreso, hora_salida)
    
    datos_correctos, mensaje = carro_nuevo.verificar_datos()
    if not datos_correctos:
        print("Mensaje:", mensaje)
        print("Este vehiculo no fue registrado. Intente nuevamente.")
        return None
    
    print("El vehiculo con placa", carro_nuevo._placa, "fue registrado exitosamente.")
    return carro_nuevo

# PROGRAMA PRINCIPAL
lista_carros = []

mostrar_encabezado()

print("Ingrese los datos de los vehiculos. Puede registrar varios en la misma sesion.")

while True:
    carro = registrar_un_carro()
    if carro is not None:
        lista_carros.append(carro)
    
    while True:
        respuesta = input("\nDesea registrar otro vehiculo? (s/n): ").lower().strip()
        if respuesta in ["s", "si", "n", "no"]:
            break
        print("Por favor responda con 's' para si o 'n' para no.")
    
    if respuesta in ["n", "no"]:
        break

mostrar_resumen(lista_carros)

print("\nGracias por utilizar el sistema de parqueadero.")
print("Sesion finalizada.")
