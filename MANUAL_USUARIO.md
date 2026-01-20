# 📘 Manual de Usuario: Simulador de Guerra Electrónica (v2.0)

Este documento proporciona una guía completa para operar e interpretar el **Simulador de Guerra Electrónica**, una herramienta diseñada para visualizar y analizar ataques de interferencia (Jamming) sobre señales de comunicaciones.

---

## 🚀 Inicio Rápido

### Modo Portátil (.exe)
1.  Busca el archivo `SimuladorEW.exe` en la carpeta del proyecto (o en `dist/` si acabas de compilar).
2.  Haz doble clic. Esto abrirá automáticamente una ventana negra (servidor) y tu navegador web por defecto con el simulador listo.

### Modo Código Fuente (Python)
1.  Ejecuta en tu terminal: `python app.py`.
2.  Ingresa manualmente a `http://127.0.0.1:8050`.

---

## 🎮 Panel de Control (Barra Lateral)

La barra izquierda te permite configurar la simulación en tiempo real.

### 1. Generador de Señal 📡
Controla la señal "amiga" o legítima que intentamos proteger.
*   **Frecuencia (Hz)**: Define qué tan rápido oscila la señal. Un valor más alto significa una onda más densa.
*   **Amplitud**: Define la potencia o fuerza de la señal legítima.

### 2. Controles de Jamming 🎯
Configura el ataque enemigo.
*   **Tipo de Ataque**:
    *   **🔊 Ruido Blanco (Banda Ancha)**: Interferencia aleatoria constante en todas las frecuencias. Eleva el "piso de ruido".
    *   **⚡ Pulso (Intermitente)**: Ataques cortos y potentes. Difícil de detectar en promedios, pero visible en el tiempo.
    *   **📻 Barrido de Frecuencia**: Una señal que se mueve rápidamente de frecuencia baja a alta, barriendo todo el espectro.
*   **Intensidad**: Potencia del ataque (0 a 5).
    *   **0**: Sin ataque (Señal limpia).
    *   **5**: Ataque máximo (Señal totalmente destruida).

### 3. Geolocalización 🗺️
Simula la posición física de la fuente del ataque en el teatro de operaciones (Venezuela).
*   **Latitud/Longitud**: Mueve al atacante en el mapa para ver cómo reacciona la triangulación de las torres de defensa simuladas (Caracas, Maracaibo, Puerto Ordaz).

---

## 📊 Interpretación de Gráficos

El dashboard está dividido en paneles visuales clave organizados para una lectura táctica rápida.

### 1. Análisis en Dominio del Tiempo (Arriba Izquierda)
Muestra la forma de la onda tal como llega al receptor.
*   **Línea Verde (🟢)**: La señal original perfecta.
*   **Línea Roja (🔴)**: La señal recibida real (con interferencia).
*   **Qué buscar**: Si la línea roja sigue a la verde, todo está bien. Si es caótica, hay interferencia.

### 2. Espectro de Frecuencia - FFT (Arriba Derecha)
Desglosa la energía por frecuencias en escala logarítmica (dB).
*   **Pico Principal**: La frecuencia de tu señal (ej. 5Hz).
*   **Piso de Ruido**: La línea base. Si sube de nivel (ej. de -60dB a -20dB), indica un ataque de **Ruido Blanco**.

### 3. Mapa de Operaciones: Venezuela (Centro Izquierda)
Visualiza la geolocalización de la amenaza.
*   **Triángulos**: Torres de defensa.
*   **Marcador Rojo**: Posición estimada del atacante.
*   **Líneas**: Triangulación activa.

### 4. Diagrama de Constelación I/Q (Centro Derecha) ⭐
Herramienta avanzada para ver la integridad de la modulación.
*   **Puntos Azules (Muestras RX)**:
    *   **Señal Limpia**: Puntos concentrados, líneas finas.
    *   **Bajo Ataque**: Nube dispersa de puntos. Cuanto más dispersa ("borrosa"), peor es la calidad.

### 5. Distribución Estadística - Histograma (Abajo Izquierda)
Muestra la "huella digital" estadística de la señal.
*   **Forma de Campana (Gaussiana)**: Indica presencia fuerte de ruido aleatorio (Jamming).
*   **Forma de U**: Indica una señal sinusoidal limpia dominante.

---

## 🚦 Métricas del Sistema (Abajo Derecha)

*   **SNR (Signal-to-Noise Ratio)**: Calidad de la señal en dB.
    *   **> 10 dB**: Operativo ✅
    *   **0 - 10 dB**: Degradado ⚠️
    *   **< 0 dB**: Crítico ❌
*   **Estado**: Diagnóstico automático del simulador.

---

### Ejemplo de "Wargame"
1.  Configura una señal limpia (Intensidad 0). Observa la pureza de la Constelación.
2.  Desplaza al atacante cerca de **Maracaibo** usando los sliders de Lat/Lon.
3.  Inicia un ataque de **Barrido** con intensidad media (2.5).
4.  Observa cómo el pico en el FFT se "mueve" y cómo la constelación se distorsiona cíclicamente.
