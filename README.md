# ⚡ Simulador de Guerra Electrónica (EW Simulator) v2.0

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Dash](https://img.shields.io/badge/Dash-2.14-success)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-lightgrey)
![Status](https://img.shields.io/badge/Status-Operational-green)

Un simulador visual avanzado para el análisis de espectro electromagnético, ataques de interferencia (Jamming) y defensa electrónica. Diseñado para propósitos educativos y de demostración técnica en ciberseguridad y telecomunicaciones.

## 📋 Características Principales

*   **Generación de Señales en Tiempo Real**: Osciladores configurables para simular comunicaciones legítimas.
*   **Ataques de Jamming Configurables**:
    *   Ruido Blanco (Broadband Noise).
    *   Pulsos Intermitentes.
    *   Barrido de Frecuencia (Sweep Jamming).
*   **Dashboard Táctico Unificado**:
    *   🗺️ **Geolocalización**: Mapa interactivo de Venezuela con simulación de triangulación de amenazas (Caracas, Maracaibo, Puerto Ordaz).
    *   📊 **Espectrómetro FFT**: Análisis de frecuencia en escala logarítmica (dB).
    *   📈 **Osciloscopio**: Visualización de señal en el tiempo.
    *   ⭐ **Diagrama I/Q**: Constelación para análisis de integridad de modulación.
    *   📉 **Histograma**: Análisis estadístico (PDF) para firma de ataques.
*   **Diseño Responsivo**: Interfaz moderna "Dark Mode" optimizada para escritorio y tablets.

## 🛠️ Modos de Uso

### Opción A: Ejecutable Portátil (Windows)
Si has descargado la versión compilada, simplemente ejecuta:
*   `SimuladorEW.exe`
*   No requiere instalación de Python ni librerías.

### Opción B: Código Fuente (Desarrolladores)

1.  **Instalar dependencias**:
    ```bash
    pip install -r requirements.txt
    ```
2.  **Ejecutar la aplicación**:
    ```bash
    python app.py
    ```
3.  **Acceder al Dashboard**:
    Abre tu navegador en `http://127.0.0.1:8050`

## 📦 Compilación (Crear .exe)

El proyecto incluye un script automático para generar un ejecutable standalone para Windows.

1.  Ejecuta el script `compilar.bat`.
2.  Espera a que termine el proceso.
3.  El ejecutable `SimuladorEW.exe` aparecerá en la carpeta `dist/`.

## 📚 Documentación

*   [📕 Manual de Usuario](MANUAL_USUARIO.md): Guía paso a paso para operar el simulador e interpretar los gráficos.
*   [⚙️ Manual Técnico](MANUAL_TECNICO.md): Explicación profunda de la arquitectura, física matemática y código fuente.

## 🖥️ Requisitos

*   **SO**: Windows 10/11 (para ejecutable), Linux/macOS (vía Python).
*   **Navegador**: Google Chrome, Firefox o Edge (con soporte WebGL activado).

## 👥 Autor

*   **Bryan Suárez**

## 📄 Licencia

Este proyecto está distribuido bajo la licencia **MIT**. Consulta el archivo [LICENSE](LICENSE) para más detalles.

---
*Desarrollado para demostración de capacidades en Defensa Electrónica y Análisis de Señales.*
