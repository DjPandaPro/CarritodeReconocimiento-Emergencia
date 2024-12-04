#include <Servo.h>
#include <SoftwareSerial.h>

// Pines para el HC-SR04
const int trigPin = 9;
const int echoPin = 8;

// Servo
Servo myServo;
const int servoPin = 10;

// Bluetooth (HC-06)
SoftwareSerial bluetooth(2, 3); // RX, TX

// Variables
int pos = 0;       // Posición del servo
long duration;     // Duración de la señal ultrasónica
int distance;      // Distancia medida
const int threshold = 20; // Umbral de detección en cm

void setup() {
  // Configuración de pines
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  
  // Configuración del servo
  myServo.attach(servoPin);

  // Configuración del Bluetooth
  bluetooth.begin(9600); // Velocidad del HC-06
  
  // Inicio del monitor serie (opcional)
  Serial.begin(9600);
  
  // Mensaje inicial
  bluetooth.println("Radar listo");
}

void loop() {
  for (pos = 0; pos <= 180; pos += 5) { // Mover servo de 0° a 180° en pasos de 5
    myServo.write(pos);
    delay(50); // Espera para estabilizar el sensor
    
    // Medir distancia
    distance = measureDistance();
    
    // Mostrar distancia en el monitor serie
    Serial.print("Angulo: ");
    Serial.print(pos);
    Serial.print("°, Distancia: ");
    Serial.print(distance);
    Serial.println(" cm");
    
    // Enviar datos por Bluetooth si hay un obstáculo
    if (distance > 0 && distance <= threshold) {
      bluetooth.print("Obstaculo detectado! Angulo: ");
      bluetooth.print(pos);
      bluetooth.print("°, Distancia: ");
      bluetooth.print(distance);
      bluetooth.println(" cm");
    }
  }

  for (pos = 180; pos >= 0; pos -= 5) { // Mover servo de 180° a 0° en pasos de 5
    myServo.write(pos);
    delay(50);
    
    // Medir distancia
    distance = measureDistance();
    
    // Mostrar distancia en el monitor serie
    Serial.print("Angulo: ");
    Serial.print(pos);
    Serial.print("°, Distancia: ");
    Serial.print(distance);
    Serial.println(" cm");
    
    // Enviar datos por Bluetooth si hay un obstáculo
    if (distance > 0 && distance <= threshold) {
      bluetooth.print("Obstaculo detectado! Angulo: ");
      bluetooth.print(pos);
      bluetooth.print("°, Distancia: ");
      bluetooth.print(distance);
      bluetooth.println(" cm");
    }
  }
}

// Función para medir distancia usando HC-SR04
int measureDistance() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  duration = pulseIn(echoPin, HIGH);
  int distance = duration * 0.034 / 2; // Convertir a cm
  
  if (distance > 400 || distance <= 0) {
    return -1; // Fuera de rango
  }
  return distance;
}
