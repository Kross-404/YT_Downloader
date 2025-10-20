import yt_dlp
import os
from dearpygui import dearpygui as dpg
import ctypes
import subprocess


# Obtiene la ruta absoluta del directorio donde está este script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Esta es la ruta que le daremos a yt-dlp
FFMPEG_DIR = script_dir

# Evitamos errores de desactualización
try:
    # Recordatorio: Es mejor ejecutar "pip install -U yt-dlp" en la terminal
    # antes de correr el script, pero lo dejamos por ahora.
    subprocess.run(["pip", "install", "-U", "yt_dlp"])
except:
    print("No se pudo actualizar yt_dlp automáticamente.")

# Hook de progreso
def progreso_hook(d):
    if d['status'] == 'downloading':
        porcentaje = d.get("_percent_str", "0.0%").strip().replace('%', '')
        try:
            progreso = float(porcentaje) / 100.0
            dpg.set_value("progress_bar", progreso)
        except:
            pass
    elif d['status'] == 'finished':
        dpg.set_value("progress_bar", 1.0)

# Función principal de descarga
def descargar_mp3_gui():
    url = dpg.get_value("input_url").strip()
    
    # Obtener la ruta del escritorio del usuario
    try:
        escritorio = os.path.join(os.path.expanduser("~"), "Desktop")
    except Exception:
         # Fallback por si no encuentra el escritorio
        escritorio = os.path.expanduser("~") 
        
    # Crear la carpeta en el escritorio
    carpeta_destino = os.path.join(escritorio, "Musica")

    if not url:
        dpg.set_value("status_text", "Por favor ingresa un enlace")
        return

    try:
        if not os.path.exists(carpeta_destino):
            os.makedirs(carpeta_destino)

        dpg.set_value("status_text", "Descargando...")
        dpg.configure_item("progress_bar", show=True)
        dpg.set_value("progress_bar", 0.0) 

        opciones = {
            'format': 'bestaudio/best',
            'outtmpl': f'{carpeta_destino}/%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'quiet': True,
            'noplaylist': True,
            'ffmpeg_location' : FFMPEG_DIR,
            'progress_hooks': [progreso_hook]
        }

        with yt_dlp.YoutubeDL(opciones) as ydl:
            ydl.download([url])

        dpg.set_value("status_text", f"Descarga completa en: {carpeta_destino}")

    except Exception as e:
        dpg.set_value("status_text", f"Error: {str(e)}")


# Obtener resolución del monitor
user32 = ctypes.windll.user32
pantalla_ancho = user32.GetSystemMetrics(0)
pantalla_alto = user32.GetSystemMetrics(1)

# ==== Interfaz ====
dpg.create_context()
dpg.create_viewport(title="Descargador de Musica", width=pantalla_ancho - 250, height=pantalla_alto - 250)

with dpg.window(label="Descargador de Música", width=pantalla_ancho, height=pantalla_alto):
    dpg.add_text("Descargar audio de video", color=(255, 255, 255))
    dpg.add_input_text(label="URL del video", tag="input_url", width=pantalla_ancho - 550)
    dpg.add_button(label="Descargar", callback=descargar_mp3_gui)
    dpg.add_spacer(height=10)
    dpg.add_progress_bar(tag="progress_bar", default_value=0.0, width=pantalla_ancho - 550, show=False)
    dpg.add_text("", tag="status_text")

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()