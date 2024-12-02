import serial
import tkinter as tk
import threading
import keyboard

# Configura el puerto serial y la velocidad
bluetooth = serial.Serial(port='COM4', baudrate=9600, timeout=1)  # Cambia 'COM4' por el puerto asignado

# Variable para controlar el hilo de ejecución
running = True
last_command = None  # Para evitar comandos repetidos

# Variables para la interfaz
data_label = None  # Etiqueta para mostrar las lecturas
temp_label = None  # Etiqueta para temperatura y humedad del DHT11

def send_command(command):
    """
    Envía un comando al Arduino a través del módulo HC-05.
    """
    global last_command
    if command != last_command:  # Solo envía si el comando es diferente al último
        bluetooth.write(command.encode())
        print(f"Comando enviado: {command}")
        last_command = command

def check_keys():
    """
    Verifica las teclas presionadas y envía el comando correspondiente.
    """
    global running
    while running:
        if keyboard.is_pressed("up") and keyboard.is_pressed("right"):
            send_command("FR")  # Adelante y derecha
        elif keyboard.is_pressed("up") and keyboard.is_pressed("left"):
            send_command("FL")  # Adelante y izquierda
        elif keyboard.is_pressed("down") and keyboard.is_pressed("right"):
            send_command("BR")  # Reversa y derecha
        elif keyboard.is_pressed("down") and keyboard.is_pressed("left"):
            send_command("BL")  # Reversa y izquierda
        elif keyboard.is_pressed("up"):
            send_command("F")  # Avanzar
        elif keyboard.is_pressed("down"):
            send_command("B")  # Retroceder
        elif keyboard.is_pressed("right"):
            send_command("R")  # Girar derecha
        elif keyboard.is_pressed("left"):
            send_command("L")  # Girar izquierda
        elif keyboard.is_pressed("space"):
            send_command("f")  # Detener movimiento
        elif keyboard.is_pressed("b"):
            send_command("A")  # Activar el buzzer
        elif keyboard.is_pressed("s"):  # Solicitar lectura del sensor de sonido
            send_command("S")
            receive_data()
        elif keyboard.is_pressed("t"):  # Solicitar lectura del DHT11
            send_command("T")
            receive_data()
        else:
            send_command("f")  # Si no hay teclas presionadas, detener

def receive_data():
    """
    Recibe las lecturas enviadas desde el Arduino y las muestra en la GUI.
    """
    global data_label, temp_label
    if bluetooth.in_waiting > 0:  # Verifica si hay datos disponibles
        data = bluetooth.readline().decode('utf-8').strip()
        print(f"Datos recibidos: {data}")
        if "Sonido" in data:  # Si los datos son del sensor de sonido
            if data_label:
                data_label.config(text=f"Sonido: {data.split(': ')[1]}")  # Actualiza la etiqueta
        elif "Temperatura" in data:  # Si los datos son del DHT11
            if temp_label:
                temp_label.config(text=f"DHT11: {data}")  # Actualiza la etiqueta con todo el texto recibido

def stop_program():
    """
    Detiene el programa y cierra la conexión.
    """
    global running
    running = False
    bluetooth.close()
    root.destroy()

# Crear la GUI
root = tk.Tk()
root.title("Control del Carrito y Sensores")
root.geometry("300x300")

# Etiqueta para mostrar las lecturas del sensor de sonido
data_label = tk.Label(root, text="Sonido: --", font=("Arial", 14))
data_label.pack(pady=10)

# Etiqueta para mostrar las lecturas del DHT11
temp_label = tk.Label(root, text="DHT11: --", font=("Arial", 14))
temp_label.pack(pady=10)

# Botón para salir del programa
exit_button = tk.Button(root, text="Salir", command=stop_program, bg="red", fg="white", width=15, height=2)
exit_button.pack(pady=20)

# Iniciar el hilo de teclado
keyboard_thread = threading.Thread(target=check_keys, daemon=True)
keyboard_thread.start()

try:
    root.mainloop()  # Ejecuta la GUI
except Exception as e:
    print(f"Error: {e}")
finally:
    stop_program()
