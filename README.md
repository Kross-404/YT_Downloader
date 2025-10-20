Descargador de musica desde el link de youtube v.1

# Instalación y Uso
Sigue estos pasos para ejecutar el programa.

Este programa requiere FFmpeg para convertir el audio a .mp3. Debes instalarlo y agregarlo al PATH de tu sistema.
1) Ve al sitio de descargas de FFmpeg: https://www.gyan.dev/ffmpeg/builds/

2) Descarga el archivo .zip de la última versión "full build" (ej. ffmpeg-7.0.1-full_build.zip).

3) Descomprime el archivo en una carpeta permanente en tu PC (ej. C:\ffmpeg).
1. Añade FFmpeg al PATH de Windows:
    Abre el menú Inicio y busca "Editar las variables de entorno del sistema".

    Haz clic en "Variables de entorno...".

    En "Variables del sistema", busca y selecciona la variable Path y haz clic en "Editar".

    Haz clic en "Nuevo" y pega la ruta a la carpeta bin de donde descomprimiste FFmpeg (ej. C:\ffmpeg\bin).

    Acepta todas las ventanas.

3) Para verificar, abre una nueva terminal y escribe ffmpeg -version. Si muestra la versión, ¡Está listo!
4) Configurar el Proyecto:
    Clona este repositorio o descarga el ZIP:

    https://github.com/Kross-404/YT_Downloader.git

    Crea un entorno virtual (recomendado):

    python -m venv .venv

    activa el entorno virtual:

    .\.venv\Scripts\activate

    Instala las dependencias de Python:

    pip install -r requirements.txt

5) Ejecutar el Programa

Con tu entorno virtual activado, simplemente corre el script:

python YT_Downloader.py


## KrossDev
### kross404.git@gmail.com