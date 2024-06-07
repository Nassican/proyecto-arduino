#include "arduinoFFT.h"
#include <Keypad.h>

const byte FILAS = 4;
const byte COLUMNAS = 4;
char keys[FILAS][COLUMNAS] = {
  {'1', '2', '3', 'A'},
  {'4', '5', '6', 'B'},
  {'7', '8', '9', 'C'},
  {'*', '0', '#', 'D'}
};

byte pinesFilas[FILAS] = {2, 3, 4, 5};
byte pinesColumnas[COLUMNAS] = {6, 7, 8, 9};
int buzzerPin = 10;  // Pin para el buzzer
int sensorPin = A0;  // Pin para el sensor de sonido (entrada analógica)

// Frecuencias de las notas (2 octavas)
int notas[16] = {
  262,  294,  330,  349,
  392,  440,  494,  523,
  587,  659,  698,  784,
  880,  988, 1047, 1175
};

String nombreNotas[16] = {
  "C4", "D4", "E4", "F4",
  "G4", "A4", "B4", "C5",
  "D5", "E5", "F5", "G5",
  "A5", "B5", "C6", "D6"
};

#define SAMPLES 128             // SAMPLES-pt FFT. Debe ser una potencia de 2. Máximo 128 para Arduino Uno.
#define SAMPLING_FREQUENCY 2048 // Ts = Basado en Nyquist, debe ser 2 veces la frecuencia más alta esperada.

arduinoFFT FFT = arduinoFFT();

unsigned int samplingPeriod;
unsigned long microSeconds;

double vReal[SAMPLES]; // Vector para valores reales
double vImag[SAMPLES]; // Vector para valores imaginarios

Keypad teclado = Keypad(makeKeymap(keys), pinesFilas, pinesColumnas, FILAS, COLUMNAS);

void setup() {
  Serial.begin(115200);
  pinMode(buzzerPin, OUTPUT);
  pinMode(sensorPin, INPUT);

  samplingPeriod = round(1000000 * (1.0 / SAMPLING_FREQUENCY)); // Periodo en microsegundos

  for (byte i = 0; i < FILAS; i++) {
    pinMode(pinesFilas[i], INPUT_PULLUP);
  }
  for (byte i = 0; i < COLUMNAS; i++) {
    pinMode(pinesColumnas[i], OUTPUT);
    digitalWrite(pinesColumnas[i], HIGH);
  }
}

double leerFrecuencia() {
  for (int i = 0; i < SAMPLES; i++) {
    microSeconds = micros();
    vReal[i] = analogRead(sensorPin);
    vImag[i] = 0;
    while (micros() < (microSeconds + samplingPeriod)) {
      // Esperar
    }
  }

  FFT.Windowing(vReal, SAMPLES, FFT_WIN_TYP_HAMMING, FFT_FORWARD);
  FFT.Compute(vReal, vImag, SAMPLES, FFT_FORWARD);
  FFT.ComplexToMagnitude(vReal, vImag, SAMPLES);

  return FFT.MajorPeak(vReal, SAMPLES, SAMPLING_FREQUENCY);
}

String determinarNota(double frecuencia) {
  double minDiferencia = 1e6; // Inicializar la diferencia mínima con un valor grande
  int notaIndex = -1;

  // Determinar la nota correspondiente a la frecuencia dentro de un rango de tolerancia
  for (int i = 0; i < 16; i++) {
    double diferencia = abs(notas[i] - frecuencia);
    if (diferencia < minDiferencia) {
      minDiferencia = diferencia;
      notaIndex = i;
    }
  }

  // Si se encontró una correspondencia dentro del rango de tolerancia
  if (notaIndex != -1 && minDiferencia < 30) {  // Tolerancia de 30 Hz
    return nombreNotas[notaIndex];
  } else {
    return "--";
  }
}

void loop() {
  char teclaPresionada = NO_KEY;

  for (byte j = 0; j < COLUMNAS; j++) {
    digitalWrite(pinesColumnas[j], LOW);
    for (byte i = 0; i < FILAS; i++) {
      if (digitalRead(pinesFilas[i]) == LOW) {
        teclaPresionada = keys[i][j];
        break;
      }
    }
    digitalWrite(pinesColumnas[j], HIGH);
    if (teclaPresionada != NO_KEY) break;
  }

  if (teclaPresionada != NO_KEY) {
    int teclaIndex = obtenerIndiceNota(teclaPresionada);
    if (teclaIndex != -1) {
      tone(buzzerPin, notas[teclaIndex]);

      double frecuencia = leerFrecuencia();
      String nota = determinarNota(frecuencia);
      bool notaCorrecta = (nota == nombreNotas[teclaIndex]);

      // Enviar datos en formato JSON
      Serial.print("{");
      Serial.print("\"tecla\":\""); Serial.print(teclaPresionada); Serial.print("\",");
      Serial.print("\"nota_tecla\":\""); Serial.print(nombreNotas[teclaIndex]); Serial.print("\","); // Agregar la nota correspondiente a la tecla presionada
      Serial.print("\"frecuencia\":"); Serial.print(frecuencia, 2); Serial.print(",");
      Serial.print("\"nota\":\""); Serial.print(nota); Serial.print("\",");
      Serial.print("\"correcta\":"); Serial.print(notaCorrecta ? "true" : "false");
      Serial.println("}");
    }
  } else {
    noTone(buzzerPin);
  }

  delay(10);
}

int obtenerIndiceNota(char tecla) {
  switch(tecla) {
    case '1': return 0;
    case '2': return 1;
    case '3': return 2;
    case 'A': return 3;
    case '4': return 4;
    case '5': return 5;
    case '6': return 6;
    case 'B': return 7;
    case '7': return 8;
    case '8': return 9;
    case '9': return 10;
    case 'C': return 11;
    case '*': return 12;
    case '0': return 13;
    case '#': return 14;
    case 'D': return 15;
    default: return -1;
  }
}