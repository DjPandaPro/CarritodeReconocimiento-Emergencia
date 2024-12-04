import serial
import matplotlib.pyplot as plt
import numpy as np

# Configuración del puerto serial para Bluetooth
puerto = "COM4"  # Cambia al puerto COM correspondiente al HC-06
baudrate = 9600

try:
    arduino = serial.Serial(puerto, baudrate, timeout=1)
    print(f"Conectado al puerto {puerto}")
except serial.SerialException as e:
    print(f"Error al conectar con el puerto {puerto}: {e}")
    exit()

# Configuración del gráfico
fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
ax.set_ylim(0, 200)  # Máxima distancia en cm
ax.set_theta_direction(1)  # Dirección de los ángulos (en sentido anti-horario)
ax.set_theta_offset(2*np.pi)  # Comienza en la parte superior (90°)
ax.set_thetamin(0)  # Límite mínimo: 0°
ax.set_thetamax(180)  # Límite máximo: 180°

# Función para actualizar el radar
def actualizar_radar(data):
    angles = []
    distances = []

    for angle, distance in data:
        angles.append(np.radians(angle))
        distances.append(distance)

    ax.clear()
    ax.set_ylim(0, 200)
    ax.set_theta_direction(1)  # Sentido anti-horario
    ax.set_theta_offset(2*np.pi)  # Mantener orientación arriba (90°)
    ax.set_thetamin(0)
    ax.set_thetamax(180)
    
    # Configuración de estilo
    ax.grid(color='green', linestyle='--', linewidth=0.5)
    ax.tick_params(axis='x', colors='green')
    ax.tick_params(axis='y', colors='green')
    ax.set_facecolor('black')
    
    # Datos del radar
    ax.scatter(angles, distances, c='red', s=20)  # Puntos del radar
    ax.fill(angles, distances, color='green', alpha=0.3)  # Relleno del radar
    plt.draw()

# Loop principal
try:
    data = []
    plt.ion()
    while True:
        if arduino.in_waiting > 0:
            line = arduino.readline().decode('utf-8').strip()
            print(f"Recibido: {line}")  # Depuración: Ver los datos recibidos
            try:
                angle, distance = map(int, line.split(","))
                if 0 <= angle <= 180:  # Solo procesar datos en el rango 0°-180°
                    data.append((angle, distance))

                if len(data) > 18:  # Limitar a un barrido completo
                    data.pop(0)

                actualizar_radar(data)
                plt.pause(0.01)
            except ValueError:
                print(f"Error procesando línea: {line}")  # Línea con formato incorrecto
except KeyboardInterrupt:
    print("Programa terminado.")
finally:
    arduino.close()
    plt.ioff()
    plt.show()
