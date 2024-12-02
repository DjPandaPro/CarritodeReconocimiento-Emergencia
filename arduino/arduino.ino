#include <Wire.h>
#include <SoftwareSerial.h>
#include <DHT.h>  // Incluye la biblioteca para el sensor DHT

const int buzzerPin = 4;           // Pin del buzzer en el Arduino
SoftwareSerial bluetooth(2, 3);    // RX en 2, TX en 3 para el HC-05

// Pines de control del carrito
int Motor1A = 5;
int Motor1B = 6;
int Motor2A = 9;
int Motor2B = 10;

// Pin del sensor de sonido
const int soundSensorPin = A0;

// Configuración del sensor DHT11
#define DHTPIN 7       // Pin donde está conectado el DHT11
#define DHTTYPE DHT11  // Define el tipo de sensor (DHT11 en este caso)
DHT dht(DHTPIN, DHTTYPE);  // Crea un objeto de la clase DHT

void setup() {
    Serial.begin(9600);            // Comunicación serial con la computadora
    bluetooth.begin(9600);         // Comunicación con el HC-05

    pinMode(buzzerPin, OUTPUT);    // Configura el pin del buzzer como salida

    // Configuración de los pines del carrito como salidas
    pinMode(Motor1A, OUTPUT);
    pinMode(Motor1B, OUTPUT);
    pinMode(Motor2A, OUTPUT);
    pinMode(Motor2B, OUTPUT);

    pinMode(soundSensorPin, INPUT); // Configura el pin del sensor de sonido como entrada

    dht.begin();                   // Inicia el sensor DHT11

    detenerCarrito();              // Asegúrate de que los motores estén apagados al inicio
}

void loop() {
    // Verifica si hay un comando disponible desde el HC-05
    if (bluetooth.available()) {
        char command = bluetooth.read();
        manejarComando(command);
    }
}

void manejarComando(char command) {
    switch (command) {
        case 'F':                   // Adelante - Iniciar
            moverAdelante();
            break;
        case 'f':                   // Adelante - Detener
            detenerCarrito();
            break;
        case 'B':                   // Reversa - Iniciar
            moverReversa();
            break;
        case 'b':                   // Reversa - Detener
            detenerCarrito();
            break;
        case 'L':                   // Izquierda - Iniciar
            girarIzquierda();
            break;
        case 'l':                   // Izquierda - Detener
            detenerCarrito();
            break;
        case 'R':                   // Derecha - Iniciar
            girarDerecha();
            break;
        case 'r':                   // Derecha - Detener
            detenerCarrito();
            break;
        case 'A':                   // Activa el buzzer
            activarBuzzer();
            break;
        case 'S':                   // Solicita la lectura del sensor de sonido
            enviarLecturaSonido();
            break;
        case 'T':                   // Solicita la lectura de temperatura y humedad del DHT11
            enviarLecturaDHT();
            break;
        default:
            break;
    }
}

void activarBuzzer() {
    digitalWrite(buzzerPin, HIGH);
    delay(1000);
    digitalWrite(buzzerPin, LOW);
}

void moverAdelante() {
    digitalWrite(Motor1A, HIGH);
    digitalWrite(Motor1B, LOW);
    digitalWrite(Motor2A, HIGH);
    digitalWrite(Motor2B, LOW);
}

void moverReversa() {
    digitalWrite(Motor1A, LOW);
    digitalWrite(Motor1B, HIGH);
    digitalWrite(Motor2A, LOW);
    digitalWrite(Motor2B, HIGH);
}

void girarIzquierda() {
    digitalWrite(Motor1A, LOW);
    digitalWrite(Motor1B, HIGH);
    digitalWrite(Motor2A, HIGH);
    digitalWrite(Motor2B, LOW);
}

void girarDerecha() {
    digitalWrite(Motor1A, HIGH);
    digitalWrite(Motor1B, LOW);
    digitalWrite(Motor2A, LOW);
    digitalWrite(Motor2B, HIGH);
}

void detenerCarrito() {
    digitalWrite(Motor1A, LOW);
    digitalWrite(Motor1B, LOW);
    digitalWrite(Motor2A, LOW);
    digitalWrite(Motor2B, LOW);
}

void enviarLecturaSonido() {
    int soundValue = analogRead(soundSensorPin); // Lee el valor del sensor de sonido
    bluetooth.print("Sonido: ");
    bluetooth.println(soundValue);              // Envía el valor por Bluetooth
    Serial.print("Sonido: ");                   // También muestra el valor en el monitor serial
    Serial.println(soundValue);
}

void enviarLecturaDHT() {
    float h = dht.readHumidity();    // Lee la humedad
    float t = dht.readTemperature(); // Lee la temperatura en grados Celsius

    // Verifica si la lectura fue exitosa
    if (isnan(h) || isnan(t)) {
        bluetooth.println("Error al leer el DHT11");
        Serial.println("Error al leer el DHT11");
    } else {
        // Envía los datos por Bluetooth
        bluetooth.print("Temperatura: ");
        bluetooth.print(t);
        bluetooth.print("°C, Humedad: ");
        bluetooth.print(h);
        bluetooth.println("%");

        // Muestra los datos en el monitor serial
        Serial.print("Temperatura: ");
        Serial.print(t);
        Serial.print("°C, Humedad: ");
        Serial.print(h);
        Serial.println("%");
    }
}
