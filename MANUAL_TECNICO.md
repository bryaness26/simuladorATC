# 🛠️ Manual Técnico: Simulador de Guerra Electrónica

Este documento describe la arquitectura interna, las tecnologías utilizadas y la lógica matemática detrás del Simulador de Guerra Electrónica (EW).

---

## 1. Arquitectura del Sistema

El sistema sigue una arquitectura Modelo-Vista-Controlador (MVC) adaptada para aplicaciones reactivas de datos:

*   **Modelo (Backend Lógico)**: Clase `SimuladorGuerraElectronica`. Encargada de toda la generación matemática de señales, procesamiento DSP (Digital Signal Processing) y cálculos de física de ondas.
*   **Vista (Frontend)**: Interfaz web construida con `Dash` (React.js wrapper) y `Dash Bootstrap Components`. Utiliza `Plotly` para renderizado gráfico avanzado (WebGL) y Mapbox.
*   **Controlador (Callbacks)**: Funciones decoradas con `@callback` que conectan las entradas del usuario (sliders, dropdowns) con la lógica del modelo y actualizan las vistas.

### Estructura de Archivos
```
.
├── app.py                 # Punto de entrada y orquestador principal
├── compilar.bat           # Script de automatización de build (Windows)
├── assets/
│   └── style.css          # Hoja de estilos (Flexbox, Responsive, Dark Theme)
├── requirements.txt       # Dependencias del proyecto
└── MANUAL_USUARIO.md      # Guía para el operador
```

---

## 2. Tecnologías Clave

*   **Python 3.x**: Lenguaje base.
*   **NumPy**: Motor de cálculo vectorial de alto rendimiento.
*   **SciPy**:
    *   `scipy.fft`: Transformada Rápida de Fourier.
    *   `scipy.signal.hilbert`: Transformada de Hilbert (Fase/Cuadratura).
*   **Dash & Plotly**: Framework de visualización.
*   **PyInstaller**: Herramienta de congelación de código para crear binarios independientes.

---

## 3. Lógica Matemática y DSP

### 3.1. Generación de Señales
La señal legítima $S(t)$ se modela como una onda sinusoidal pura:
$$S(t) = A \cdot \sin(2\pi f t)$$

### 3.2. Modelado de Interferencias (Jamming)
*   **Ruido Blanco (AWGN)**: Se genera usando una distribución Normal (Gaussiana) $\mathcal{N}(0, \sigma^2)$.
*   **Interferencia de Pulsos**: Señal nula modulada por una función rectangular periódica.

### 3.3. Análisis Espectral (FFT)
El sistema convierte la señal al dominio de la frecuencia con escala logarítmica (dB) para visualizar el piso de ruido:
$$P_{dB} = 20 \cdot \log_{10}(|FFT(x)|)$$

### 3.4. Diagrama de Constelación (I/Q)
Utiliza la señal analítica $x_a(t)$ derivada de la Transformada de Hilbert para obtener componentes I (Real) y Q (Imaginario). Esto permite visualizar la degradación de fase bajo ataques.

### 3.5. Geolocalización
Simula coordenadas reales sobre Venezuela. El algoritmo calcula la distancia geodésica aproximada (usando proyección plana simple para eficiencia en simulación) entre los nodos de defensa (Caracas, Maracaibo, Puerto Ordaz) y el objetivo.

---

## 4. Frontend y Estilos (CSS)

El diseño (`style.css`) utiliza un enfoque moderno basado en **Flexbox**:
*   **Layout Fluido**: Utilizamos `display: flex` con `flex-direction: column` para el contenedor principal de gráficos.
*   **Filas Flexibles**: La clase `.charts-row` agrupa gráficos en pares horizontales.
*   **Responsividad**: Un breakpoint en `1200px` cambia la dirección de `.charts-row` a columna, permitiendo que la interfaz se adapte perfectamente a tablets o pantallas pequeñas sin romper los gráficos.
*   **Tema Oscuro**: Variables CSS (`--bg-primary`, `--accent-cyan`) definen una paleta de colores de alto contraste estilo "Centro de Comando".

---

## 5. Compilación y Despliegue

Para distribuir la aplicación sin requerir Python en el cliente, utilizamos `PyInstaller`.

### 5.1. Proceso de Build
El script `compilar.bat` automatiza el comando:
```bash
pyinstaller --name "SimuladorEW" --onefile --add-data "assets;assets" app.py
```
*   `--onefile`: Empaqueta todo en un único `.exe`.
*   `--add-data`: Es crítico para incluir la carpeta `assets/` (CSS) dentro del binario, ya que Dash la requiere para renderizar los estilos.

### 5.2. Detección en Runtime
El código en `app.py` incluye una lógica especial:
```python
if getattr(sys, 'frozen', False):
    # Modo EXE: Abre navegador y desactiva debug
```
Esto asegura que el usuario final tenga una experiencia de "doble clic y usar", mientras que el desarrollador mantiene las herramientas de depuración (`debug=True`) al correr el script fuente.

---
**Desarrollado con tecnologías Open Source para visualización científica.**
