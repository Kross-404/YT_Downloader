import yt_dlp
import os
from dearpygui import dearpygui as dpg
import threading # Para que la interfaz no se congele durante la descarga

# ==== Funciones ====

def progreso_hook(d):
    """Actualiza la barra de progreso en la interfaz."""
    if d['status'] == 'downloading':
        p_str = d.get("_percent_str", "0%").replace('%', '')
        try:
            progreso = float(p_str) / 100.0
            dpg.set_value("progress_bar", progreso)
            dpg.configure_item("status_text", default_value=f"Descargando: {d.get('_percent_str', '0%')}")
        except ValueError:
            pass
    elif d['status'] == 'finished':
        dpg.set_value("progress_bar", 1.0)
        dpg.configure_item("status_text", default_value="Procesando audio (FFmpeg)...")

def ejecutar_descarga(url, carpeta_destino):
    """Lógica de descarga que corre en un hilo separado."""
    opciones = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(carpeta_destino, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
        'noplaylist': True,
        'progress_hooks': [progreso_hook]
    }

    try:
        with yt_dlp.YoutubeDL(opciones) as ydl:
            ydl.download([url])
        
        dpg.configure_item("status_text", default_value=f"¡Listo! Guardado en: {os.path.basename(carpeta_destino)}")
        dpg.set_value("input_url", "") # Limpiar input
        
    except Exception as e:
        dpg.configure_item("status_text", default_value=f"Error: {str(e)}")

def boton_descargar_callback():
    url = dpg.get_value("input_url").strip()
    if not url:
        dpg.set_value("status_text", "Por favor ingresa un enlace")
        return

    # Ruta al escritorio (compatible con Windows/Linux/Mac)
    escritorio = os.path.join(os.path.expanduser("~"), "Desktop")
    carpeta_destino = os.path.join(escritorio, "Musica")

    if not os.path.exists(carpeta_destino):
        try:
            os.makedirs(carpeta_destino)
        except OSError:
            dpg.set_value("status_text", "Error: No se pudo crear la carpeta en el Escritorio.")
            return

    dpg.set_value("status_text", "Iniciando...")
    dpg.configure_item("progress_bar", show=True)
    dpg.set_value("progress_bar", 0.0)

    # Ejecutamos en un Hilo (Thread) para que la ventana no se congele "No responde"
    hilo = threading.Thread(target=ejecutar_descarga, args=(url, carpeta_destino), daemon=True)
    hilo.start()

# ==== Interfaz Gráfica (GUI) ====

dpg.create_context()

# Ventana de tamaño fijo, más amigable
ANCHO = 600
ALTO = 300

with dpg.window(label="Principal", tag="Primary Window"):
    dpg.add_text("Descargador de YouTube a MP3", color=(0, 255, 0))
    dpg.add_separator()
    dpg.add_spacer(height=10)
    
    dpg.add_text("URL del video:")
    dpg.add_input_text(tag="input_url", width=-1) # -1 ajusta al ancho disponible
    dpg.add_spacer(height=10)
    
    dpg.add_button(label="DESCARGAR MP3", callback=boton_descargar_callback, width=-1, height=40)
    dpg.add_spacer(height=10)
    
    dpg.add_progress_bar(tag="progress_bar", default_value=0.0, width=-1, show=False)
    dpg.add_text("Esperando...", tag="status_text", wrap=ANCHO-20)

dpg.create_viewport(title="Kross Downloader v1.1", width=ANCHO, height=ALTO, resizable=False)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Primary Window", True) # Fija la ventana al viewport
dpg.start_dearpygui()
dpg.destroy_context()