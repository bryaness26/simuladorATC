"""
╔══════════════════════════════════════════════════════════════════╗
║         SIMULADOR DE GUERRA ELECTRÓNICA - DASHBOARD              ║
║                    Versión 2.0 - Dashboard Interactivo           ║
║                                                                  ║
║  Características:                                                 ║
║  • Dashboard unificado con 4 paneles de visualización            ║
║  • Controles interactivos en tiempo real                         ║
║  • Análisis de señales en dominio de tiempo y frecuencia         ║
║  • Geolocalización por triangulación                             ║
║  • Métricas de impacto y estado del sistema                      ║
╚══════════════════════════════════════════════════════════════════╝
"""

import numpy as np
from scipy.fft import fft, fftfreq
from scipy.signal import hilbert
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash
from dash import dcc, html, callback, Input, Output, State
import dash_bootstrap_components as dbc

# =============================================================================
# CLASE PRINCIPAL DEL SIMULADOR (Motor de cálculo)
# =============================================================================

class SimuladorGuerraElectronica:
    """Motor de simulación de guerra electrónica y análisis de señales."""
    
    def __init__(self, fs=1000):
        """
        Inicializa el simulador.
        
        Args:
            fs: Frecuencia de muestreo en Hz
        """
        self.fs = fs
        self.t = np.linspace(0, 1, self.fs, endpoint=False)
    
    def generar_onda_legitima(self, freq=5, amplitud=1.0):
        """
        Genera la señal de comunicación normal (ej. Comandos SCADA).
        
        Args:
            freq: Frecuencia de la señal en Hz
            amplitud: Amplitud de la onda
        
        Returns:
            Array numpy con la señal sinusoidal
        """
        return amplitud * np.sin(2 * np.pi * freq * self.t)
    
    def generar_ataque_jamming(self, intensidad=0, tipo="ruido_blanco"):
        """
        Simula el ataque de interferencia electrónica.
        
        Args:
            intensidad: Nivel de potencia del jamming (0-5)
            tipo: Tipo de ataque ("ruido_blanco", "pulso", "barrido")
        
        Returns:
            Array numpy con la interferencia
        """
        if intensidad == 0:
            return np.zeros_like(self.t)
        
        if tipo == "ruido_blanco":
            # Ruido aleatorio gaussiano (típico jamming de banda ancha)
            noise = np.random.normal(0, 1, self.t.shape)
            return noise * intensidad
        
        elif tipo == "pulso":
            # Ataques intermitentes de alta potencia
            noise = np.zeros_like(self.t)
            noise[::50] = intensidad * 3  # Pulsos cada 50 muestras
            return noise
        
        elif tipo == "barrido":
            # Jamming de barrido de frecuencia
            sweep_freq = np.linspace(1, 50, len(self.t))
            sweep = intensidad * np.sin(2 * np.pi * sweep_freq * self.t / 10)
            return sweep + np.random.normal(0, 0.3, self.t.shape) * intensidad
        
        return np.zeros_like(self.t)
    
    def analizar_impacto(self, senal_limpia, senal_sucia):
        """
        Calcula el SNR (Relación Señal-Ruido) para determinar impacto.
        
        Args:
            senal_limpia: Señal original sin interferencia
            senal_sucia: Señal con interferencia añadida
        
        Returns:
            tuple: (snr_db, estado_sistema)
        """
        potencia_senal = np.mean(senal_limpia ** 2)
        potencia_ruido = np.mean((senal_sucia - senal_limpia) ** 2)
        
        if potencia_ruido == 0:
            return 100, "OPERATIVO"
        
        snr = 10 * np.log10(potencia_senal / potencia_ruido)
        
        if snr < -5:
            estado = "COLAPSO TOTAL"
        elif snr < 0:
            estado = "DENEGACIÓN DE SERVICIO"
        elif snr < 5:
            estado = "SEVERAMENTE DEGRADADO"
        elif snr < 10:
            estado = "DEGRADADO"
        elif snr < 20:
            estado = "LATENCIA ALTA"
        else:
            estado = "OPERATIVO"
        
        return snr, estado
    
    def calcular_espectro(self, senal):
        """
        Calcula la Transformada Rápida de Fourier de la señal.
        
        Args:
            senal: Array de la señal a analizar
        
        Returns:
            tuple: (frecuencias, magnitudes)
        """
        N = len(senal)
        yf = fft(senal)
        xf = fftfreq(N, 1 / self.fs)
        
        # Solo tomamos la mitad positiva del espectro
        mag = 2.0/N * np.abs(yf[:N//2])
        
        # Convertir a dB (evitando log(0))
        mag_db = 20 * np.log10(np.maximum(mag, 1e-10))
        
        return xf[:N//2], mag_db

    def obtener_datos_iq(self, senal):
        """
        Obtiene componentes en Fase (I) y Cuadratura (Q) usando Transformada de Hilbert.
        Simula la demodulación de la señal recibida.
        
        Args:
            senal: Señal a analizar
            
        Returns:
            tuple: (I, Q)
        """
        senal_analitica = hilbert(senal)
        return np.real(senal_analitica), np.imag(senal_analitica)
    
    def simular_geolocalizacion(self, pos_ataque_lat, pos_ataque_lon):
        """
        Simula la triangulación sobre coordenadas reales de Venezuela.
        """
        # Coordenadas de "Torres de Defensa" en Venezuela
        torres = {
            'Caracas (HQ)': {'lat': 10.4806, 'lon': -66.9036, 'color': '#00ff88'},
            'Maracaibo': {'lat': 10.6549, 'lon': -71.6364, 'color': '#00d4ff'},
            'Puerto Ordaz': {'lat': 8.2968, 'lon': -62.7116, 'color': '#ff00ff'}
        }
        
        resultados = {}
        for nombre, data in torres.items():
            # Distancia euclidiana aproximada (para simulación simple en grados)
            # En una app real usaríamos Haversine
            dist_lat = data['lat'] - pos_ataque_lat
            dist_lon = data['lon'] - pos_ataque_lon
            dist_real = np.sqrt(dist_lat**2 + dist_lon**2)
            
            # Error de medición
            radio_detectado = dist_real * np.random.uniform(0.95, 1.05)
            
            resultados[nombre] = {
                'lat': data['lat'],
                'lon': data['lon'],
                'radio': radio_detectado, # En grados aprox
                'color': data['color']
            }
        
        return resultados


# =============================================================================
# INSTANCIA GLOBAL DEL SIMULADOR
# =============================================================================

sim = SimuladorGuerraElectronica(fs=1000)


# =============================================================================
# FUNCIONES DE CREACIÓN DE GRÁFICOS
# =============================================================================

def crear_grafico_tiempo(senal_pura, senal_atacada, t, snr, estado):
    """Crea el gráfico de señales en el dominio del tiempo."""
    
    fig = go.Figure()
    
    # Señal legítima
    fig.add_trace(go.Scatter(
        x=t[:200],
        y=senal_pura[:200],
        mode='lines',
        name='Comunicación Legítima',
        line=dict(color='#00ff88', width=3),
        fill='tozeroy',
        fillcolor='rgba(0, 255, 136, 0.1)'
    ))
    
    # Señal bajo ataque
    fig.add_trace(go.Scatter(
        x=t[:200],
        y=senal_atacada[:200],
        mode='lines',
        name='Señal bajo Ataque',
        line=dict(color='#ff4757', width=1.5),
        opacity=0.8
    ))
    
    # Configuración del layout
    fig.update_layout(
        title=dict(
            text=f"<b>Análisis en Dominio del Tiempo</b><br><sub>Estado: {estado} | SNR: {snr:.1f} dB</sub>",
            font=dict(color='white', size=14)
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(26, 31, 46, 0.5)',
        font=dict(color='#a0aec0'),
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1,
            bgcolor='rgba(0,0,0,0)'
        ),
        xaxis=dict(
            title='Tiempo (s)',
            gridcolor='rgba(255,255,255,0.1)',
            zerolinecolor='rgba(255,255,255,0.2)'
        ),
        yaxis=dict(
            title='Amplitud',
            gridcolor='rgba(255,255,255,0.1)',
            zerolinecolor='rgba(255,255,255,0.2)'
        ),
        margin=dict(l=50, r=20, t=80, b=50),
        hovermode='x unified'
    )
    
    return fig


def crear_grafico_espectro(frecuencias, magnitudes):
    """Crea el gráfico del espectro de frecuencia (FFT)."""
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=frecuencias,
        y=magnitudes,
        mode='lines',
        name='Espectro',
        line=dict(color='#7b2cbf', width=2),
        fill='tozeroy',
        fillcolor='rgba(123, 44, 191, 0.3)'
    ))
    
    fig.update_layout(
        title=dict(
            text="<b>Espectro de Frecuencia (FFT)</b><br><sub>Detección de interferencia en banda ancha</sub>",
            font=dict(color='white', size=14)
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(26, 31, 46, 0.5)',
        font=dict(color='#a0aec0'),
        xaxis=dict(
            title='Frecuencia (Hz)',
            gridcolor='rgba(255,255,255,0.1)',
            range=[0, 100]
        ),
        yaxis=dict(
            title='Magnitud (dB)',
            gridcolor='rgba(255,255,255,0.1)',
            range=[-60, 10]
        ),
        margin=dict(l=50, r=20, t=80, b=50)
    )
    
    # Añadir anotación sobre el ruido
    # El piso de ruido en dB suele ser bajo (ej. -40dB). Si sube de -20, es jamming.
    if np.mean(magnitudes[10:]) > -20:
        fig.add_annotation(
            x=60, y=0,
            text="⚠️ Piso de ruido elevado<br>indica ataque de banda ancha",
            showarrow=False,
            font=dict(size=10, color='#ffd93d'),
            bgcolor='rgba(0,0,0,0.5)',
            borderpad=10
        )
    
    return fig



def crear_grafico_histograma(senal):
    """Crea el histograma de distribución de amplitud (PDF)."""
    fig = go.Figure()
    
    fig.add_trace(go.Histogram(
        x=senal,
        histnorm='probability density',
        name='Distribución',
        marker_color='#00ff88',
        opacity=0.7
    ))
    
    fig.update_layout(
        title=dict(
            text="<b>Distribución Estadística (PDF)</b><br><sub>Verificación de Huella del Ataque</sub>",
            font=dict(color='white', size=14)
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(26, 31, 46, 0.5)',
        font=dict(color='#a0aec0'),
        xaxis=dict(
            title='Amplitud de Señal',
            gridcolor='rgba(255,255,255,0.1)'
        ),
        yaxis=dict(
            title='Densidad de Probabilidad',
            gridcolor='rgba(255,255,255,0.1)'
        ),
        margin=dict(l=50, r=20, t=80, b=50),
        bargap=0.1
    )
    return fig


def crear_grafico_constelacion(I, Q, estado):
    """Crea el diagrama de constelación (I vs Q)."""
    
    fig = go.Figure()
    
    # Submuestreo para mejor rendimiento visual
    indices = np.arange(0, len(I), 1)
    
    fig.add_trace(go.Scattergl(
        x=I[indices],
        y=Q[indices],
        mode='markers',
        name='Muestras RX',
        marker=dict(
            color='#00d4ff',
            size=5,
            opacity=0.6,
            line=dict(width=0)
        )
    ))
    
    # Añadir círculos de referencia (magnitud constante)
    theta = np.linspace(0, 2*np.pi, 100)
    for r in [0.5, 1.0, 1.5]:
        fig.add_trace(go.Scatter(
            x=r * np.cos(theta),
            y=r * np.sin(theta),
            mode='lines',
            line=dict(color='rgba(255,255,255,0.1)', dash='dot'),
            showlegend=False,
            hoverinfo='skip'
        ))

    titulo_estado = "Limpio" if estado == "OPERATIVO" else "Distorsionado"
    color_estado = "white" if estado == "OPERATIVO" else "#ff4757"

    fig.update_layout(
        title=dict(
            text=f"<b>Diagrama de Constelación (I/Q)</b><br><sub>Integridad de Modulación: <span style='color:{color_estado}'>{titulo_estado}</span></sub>",
            font=dict(color='white', size=14)
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(26, 31, 46, 0.5)',
        font=dict(color='#a0aec0'),
        xaxis=dict(
            title='En Fase (I)',
            gridcolor='rgba(255,255,255,0.1)',
            zerolinecolor='rgba(255,255,255,0.2)',
            range=[-2.5, 2.5],
            constrain='domain'
        ),
        yaxis=dict(
            title='Cuadratura (Q)',
            gridcolor='rgba(255,255,255,0.1)',
            zerolinecolor='rgba(255,255,255,0.2)',
            scaleanchor='x',
            scaleratio=1,
            range=[-2.5, 2.5]
        ),
        margin=dict(l=50, r=20, t=80, b=50),
        showlegend=False
    )
    
    return fig


def crear_grafico_geolocalizacion(lat_pct, lon_pct):
    """
    Crea mapa de Venezuela con Plotly Mapbox.
    lat_pct, lon_pct: Sliders de 0 a 100
    """
    # Mapear sliders (0-100) a coordenadas de Venezuela
    # Latitud aprox: 4.0 a 12.0
    # Longitud aprox: -73.0 a -60.0
    lat_atacante = 4.0 + (lat_pct / 100.0) * (12.0 - 4.0)
    lon_atacante = -73.0 + (lon_pct / 100.0) * (-60.0 - -73.0)
    
    torres_data = sim.simular_geolocalizacion(lat_atacante, lon_atacante)
    
    fig = go.Figure()
    
    # 1. Dibujar Áreas de Cobertura / Triangulación (Círculos)
    # En mapbox los círculos grandes se dibujan mejor como Scatter con marker size grande o fill
    # Para simplicidad visual, usaremos marcadores grandes translúcidos para el "radio"
    
    # 2. Dibujar Torres
    lats_t = [d['lat'] for d in torres_data.values()]
    lons_t = [d['lon'] for d in torres_data.values()]
    colors_t = [d['color'] for d in torres_data.values()]
    names_t = list(torres_data.keys())
    
    fig.add_trace(go.Scattermap(
        lat=lats_t,
        lon=lons_t,
        mode='markers+text',
        marker=dict(size=15, color=colors_t, symbol='circle'),
        text=names_t,
        textposition="top right",
        name='Defensa'
    ))
    
    # 3. Dibujar Atacante
    fig.add_trace(go.Scattermap(
        lat=[lat_atacante],
        lon=[lon_atacante],
        mode='markers',
        marker=dict(size=20, color='#ff4757', symbol='circle'),
        name='FUENTE JAMMING'
    ))
    
    # Líneas de conexión
    for d in torres_data.values():
        fig.add_trace(go.Scattermap(
            lat=[d['lat'], lat_atacante],
            lon=[d['lon'], lon_atacante],
            mode='lines',
            line=dict(width=2, color='#ff4757'),
            opacity=0.3,
            showlegend=False
        ))

    fig.update_layout(
        title=dict(
            text="<b>Teatro de Operaciones: Venezuela</b><br><sub>Triangulación Satelital/Terrestre</sub>",
            font=dict(color='white', size=14)
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#a0aec0'),
        margin=dict(l=0, r=0, t=50, b=0),
        map=dict(
            style="carto-darkmatter", # Estilo oscuro gratuito integrado
            center=dict(lat=8.0, lon=-66.0),
            zoom=4.5
        ),
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=0,
            xanchor='center',
            x=0.5,
            bgcolor='rgba(0,0,0,0.5)'
        )
    )
    
    return fig


# =============================================================================
# APLICACIÓN DASH
# =============================================================================

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.CYBORG],
    title="Simulador de Guerra Electrónica",
    update_title=None,
    suppress_callback_exceptions=True
)

# Layout de la aplicación
app.layout = html.Div([
    # Header
    html.Div([
        html.H1("⚡ SIMULADOR DE GUERRA ELECTRÓNICA", className="header-title"),
        html.Div([
            html.Div([
                html.Span(className="status-dot"),
                html.Span("ONLINE")
            ], className="status-indicator status-online"),
            html.Div([
                html.Span(className="status-dot"),
                html.Span("SECURE")
            ], className="status-indicator status-online"),
            html.Div(id="alert-indicator", children=[
                html.Span(className="status-dot"),
                html.Span("MONITORING")
            ], className="status-indicator status-online"),
        ], className="header-status")
    ], className="header"),
    
    # Contenedor principal
    html.Div([
        # Sidebar con controles
        html.Div([
            # Sección: Generador de Señal
            html.Div([
                html.H3("📡 GENERADOR DE SEÑAL", className="section-title"),
                
                html.Label("Frecuencia de la Señal (Hz)", className="control-label"),
                dcc.Slider(
                    id='freq-slider',
                    min=1, max=20, step=1, value=5,
                    marks={i: str(i) for i in range(1, 21, 4)},
                    tooltip={"placement": "bottom", "always_visible": True}
                ),
                
                html.Label("Amplitud de la Señal", className="control-label"),
                dcc.Slider(
                    id='amp-slider',
                    min=0.5, max=2.0, step=0.1, value=1.0,
                    marks={0.5: '0.5', 1.0: '1.0', 1.5: '1.5', 2.0: '2.0'},
                    tooltip={"placement": "bottom", "always_visible": True}
                ),
            ], className="control-section"),
            
            # Sección: Controles de Jamming
            html.Div([
                html.H3("🎯 CONTROLES DE JAMMING", className="section-title"),
                
                html.Label("Tipo de Ataque", className="control-label"),
                dcc.Dropdown(
                    id='tipo-ataque',
                    options=[
                        {'label': '🔊 Ruido Blanco (Banda Ancha)', 'value': 'ruido_blanco'},
                        {'label': '⚡ Pulso (Intermitente)', 'value': 'pulso'},
                        {'label': '📻 Barrido de Frecuencia', 'value': 'barrido'}
                    ],
                    value='ruido_blanco',
                    clearable=False,
                    style={'marginBottom': '20px'}
                ),
                
                html.Label("Intensidad del Ataque", className="control-label"),
                dcc.Slider(
                    id='intensidad-slider',
                    min=0, max=5, step=0.1, value=2.5,
                    marks={0: 'OFF', 1: '1', 2: '2', 3: '3', 4: '4', 5: 'MAX'},
                    tooltip={"placement": "bottom", "always_visible": True}
                ),
            ], className="control-section"),
            
            # Sección: Geolocalización
            html.Div([

                
                html.H3("🗺️ POSICIÓN DEL ATACANTE", className="section-title"),
                
                html.Label("Latitud (Norte-Sur)", className="control-label"),
                dcc.Slider(
                    id='pos-x-slider',
                    min=0, max=100, step=1, value=60,
                    marks={0: '0', 25: '25', 50: '50', 75: '75', 100: '100'},
                    tooltip={"placement": "bottom", "always_visible": True}
                ),
                
                html.Label("Longitud (Este-Oeste)", className="control-label"),
                dcc.Slider(
                    id='pos-y-slider',
                    min=0, max=100, step=1, value=55,
                    marks={0: '0', 25: '25', 50: '50', 75: '75', 100: '100'},
                    tooltip={"placement": "bottom", "always_visible": True}
                ),
            ], className="control-section"),
            
            # Botón de regenerar
            html.Button("🔄 REGENERAR SIMULACIÓN", id="btn-regenerar", className="btn-primary"),
            
        ], className="sidebar"),
        
        # Área de gráficos
        html.Div([
            # Fila Superior: Tiempo y Espectro (Antes estaba así, pero ahora reordenamos para grid 2x2)
             html.Div([
                # Gráfico de tiempo
                html.Div([
                    dcc.Graph(id='grafico-tiempo', config={'displayModeBar': False})
                ], className="chart-card half-width"),
                
                # Gráfico de espectro
                html.Div([
                    dcc.Graph(id='grafico-espectro', config={'displayModeBar': False})
                ], className="chart-card half-width"),
            ], className="charts-row"),

            html.Div([
                # Gráfico de geolocalización
                html.Div([
                    dcc.Graph(id='grafico-geo', config={'displayModeBar': False})
                ], className="chart-card half-width"),

                # Gráfico de Constelación (NUEVO)
                html.Div([
                    dcc.Graph(id='grafico-constelacion', config={'displayModeBar': False})
                ], className="chart-card half-width"),
            ], className="charts-row"),
            
            # Panel de métricas
            
            # Fila Inferior: Histograma y Métricas
            html.Div([
                # Gráfico Histograma (NUEVO)
                html.Div([
                    dcc.Graph(id='grafico-histograma', config={'displayModeBar': False})
                ], className="chart-card half-width"),

                # Panel de métricas (Ahora ocupa la mitad derecha)
                html.Div([
                    html.Div("MÉTRICAS DEL SISTEMA", className="chart-title", style={'width': '100%', 'textAlign': 'center', 'marginBottom': '20px'}),
                    
                    html.Div([
                        # SNR grande
                        html.Div([
                            html.Div(id='snr-value', className="metric-value"),
                            html.Div("Signal-to-Noise Ratio (dB)", className="metric-label")
                        ], className="metric-big", style={'width': '100%', 'marginBottom': '20px'}),
                        
                        # Tarjetas de estado
                        html.Div(id='status-cards', className="status-cards", style={'width': '100%', 'justifyContent': 'center', 'marginBottom': '20px'}),
                        
                        # Parámetros del ataque
                        html.Div([
                            html.Div("PARÁMETROS DEL ATAQUE", 
                                    style={'fontSize': '0.85rem', 'color': '#00d4ff', 'marginBottom': '10px', 'fontWeight': '600'}),
                            html.Div(id='attack-params', className="attack-params")
                        ], style={'width': '100%'})
                    ], style={'display': 'flex', 'flexDirection': 'column', 'width': '100%'})
                    
                ], className="chart-card half-width metrics-panel", style={'display': 'flex', 'flexDirection': 'column', 'justifyContent': 'center'}),

            ], className="charts-row"),
            
        ], className="charts-area")
        
    ], className="main-container")
])


# =============================================================================
# CALLBACKS
# =============================================================================

@callback(
    [Output('grafico-tiempo', 'figure'),
     Output('grafico-espectro', 'figure'),
     Output('grafico-geo', 'figure'),
     Output('grafico-constelacion', 'figure'),
     Output('grafico-histograma', 'figure'),
     Output('snr-value', 'children'),
     Output('status-cards', 'children'),
     Output('attack-params', 'children'),
     Output('alert-indicator', 'className')],
    [Input('freq-slider', 'value'),
     Input('amp-slider', 'value'),
     Input('tipo-ataque', 'value'),
     Input('intensidad-slider', 'value'),
     Input('pos-x-slider', 'value'),
     Input('pos-y-slider', 'value'),
     Input('btn-regenerar', 'n_clicks')]
)
def actualizar_dashboard(freq, amp, tipo_ataque, intensidad, pos_x, pos_y, n_clicks):
    """Callback principal que actualiza todos los gráficos y métricas."""
    
    # Generar señales
    senal_pura = sim.generar_onda_legitima(freq=freq, amplitud=amp)
    interferencia = sim.generar_ataque_jamming(intensidad=intensidad, tipo=tipo_ataque)
    senal_atacada = senal_pura + interferencia
    
    # Análisis
    # Análisis
    snr, estado = sim.analizar_impacto(senal_pura, senal_atacada)
    frecuencias, magnitudes_db = sim.calcular_espectro(senal_atacada)
    I, Q = sim.obtener_datos_iq(senal_atacada)
    
    # Crear gráficos
    fig_tiempo = crear_grafico_tiempo(senal_pura, senal_atacada, sim.t, snr, estado)
    fig_espectro = crear_grafico_espectro(frecuencias, magnitudes_db)
    fig_geo = crear_grafico_geolocalizacion(pos_x, pos_y)
    fig_constelacion = crear_grafico_constelacion(I, Q, estado)
    fig_histograma = crear_grafico_histograma(senal_atacada)
    
    # Valor SNR formateado
    snr_text = f"{snr:.1f} dB"
    
    # Determinar clases de estado
    if snr >= 10:
        class_op, class_warn, class_dang = "status-card active", "status-card", "status-card"
        alert_class = "status-indicator status-online"
    elif snr >= 0:
        class_op, class_warn, class_dang = "status-card", "status-card warning", "status-card"
        alert_class = "status-indicator status-online"
    else:
        class_op, class_warn, class_dang = "status-card", "status-card", "status-card danger"
        alert_class = "status-indicator status-alert"
    
    # Tarjetas de estado
    status_cards = [
        html.Div([
            html.Div("✅", className="status-icon"),
            html.Div("OPERATIVO", className="status-text")
        ], className=class_op),
        html.Div([
            html.Div("⚠️", className="status-icon"),
            html.Div("DEGRADADO", className="status-text")
        ], className=class_warn),
        html.Div([
            html.Div("❌", className="status-icon"),
            html.Div("CRÍTICO", className="status-text")
        ], className=class_dang),
    ]
    
    # Parámetros del ataque
    tipo_nombres = {
        'ruido_blanco': 'Ruido Blanco',
        'pulso': 'Pulso',
        'barrido': 'Barrido'
    }
    
    attack_params = [
        html.Div([
            html.Span("Tipo de Jamming:", className="param-name"),
            html.Span(tipo_nombres.get(tipo_ataque, 'N/A'), className="param-value")
        ], className="param-row"),
        html.Div([
            html.Span("Intensidad:", className="param-name"),
            html.Span(f"{intensidad:.1f} / 5.0", className="param-value")
        ], className="param-row"),
        html.Div([
            html.Span("Estado Sistema:", className="param-name"),
            html.Span(estado, className="param-value")
        ], className="param-row"),
        html.Div([
            html.Span("Posición Atacante:", className="param-name"),
            html.Span(f"({pos_x}, {pos_y})", className="param-value")
        ], className="param-row"),
        html.Div([
            html.Span("Frecuencia Señal:", className="param-name"),
            html.Span(f"{freq} Hz", className="param-value")
        ], className="param-row"),
    ]
    
    return fig_tiempo, fig_espectro, fig_geo, fig_constelacion, fig_histograma, snr_text, status_cards, attack_params, alert_class


# =============================================================================
# PUNTO DE ENTRADA
# =============================================================================

if __name__ == '__main__':
    import sys
    import webbrowser
    from threading import Timer

    print("\n" + "="*60)
    print("   🚀 SIMULADOR DE GUERRA ELECTRÓNICA - DASHBOARD")
    print("="*60)
    print("\n   Iniciando servidor...")
    print("   Accede en: http://127.0.0.1:8050\n")
    print("="*60 + "\n")
    
    # Detectar si estamos corriendo en modo ejecutable (PyInstaller)
    if getattr(sys, 'frozen', False):
        # En modo EXE: Desactivar debug y abrir navegador automáticamente
        Timer(1.5, lambda: webbrowser.open("http://127.0.0.1:8050")).start()
        app.run(debug=False, host='127.0.0.1', port=8050)
    else:
        # En modo Desarrollo: Debug activado
        app.run(debug=True, host='127.0.0.1', port=8050)
