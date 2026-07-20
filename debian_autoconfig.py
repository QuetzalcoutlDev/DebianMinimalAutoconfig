#############################################################################
#######  Script de automatización en Python, para Debian 13 Minimal  #######
#############################################################################

### versión 1.0

import os, subprocess, sys, time, json, pathlib, stat

## Rutas generales
username = os.environ.get("SUDO_USER") # Obtener el usuario que llamo a sudo
fast_path = f"/home/{username}/.config/fastfetch"
gtk_path = f"/home/{username}/.config/gtk-3.0"
bg_path = f"/home/{username}/.config/backgrounds"

# Obtener IDs de usuario (el que llamo a sudo)
uid = int(os.getenv("SUDO_UID"))
gid = int(os.getenv("SUDO_GID"))

# Rutas de IceWM
ice_path = f"/home/{username}/.icewm"
startup_file = os.path.join(ice_path, "startup")

# Diccionario de configuración de fastfetch
fastfetch_config = {
  "$schema": "https://github.com/fastfetch-cli/fastfetch/raw/master/doc/json_schema.json",
    "logo": {
        "type": "file",
        "source": f"{fast_path}/logo.txt"
        },      
    "modules": [
        "title",
        "separator",
        "os",
        "host",
        "kernel",
        "uptime",
        "packages",
        "shell",
        "display",
        "de",
        "wm",
        "wmtheme",
        "theme",
        "icons",
        "font",
        "cursor",
        "terminal",
        "terminalfont",
        "cpu",
        "gpu",
        "memory",
        "swap",
        "disk",
        "localip",
        "battery",
        "poweradapter",
        "locale",
        "break",
        "colors"
    ]
}


# Guardar el arte Ascii a usar para crear un archivo .txt en ~/.config/fastfetch/ con el contenido para el fastfetch
# Para configurar el fastfetch hay que usar fastfetch --gen-config y buscar el archivo config.jsonc en ~/.config/fastfetch/
girl_art = """
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⠓⠶⣤⠀⠀⠀⠀⣠⠶⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠇⠀⢠⡏⠀⠀⢀⡔⠉⠀⢈⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠩⠤⣄⣼⠁⠀⣠⠟⠀⠀⣠⠏⠀⠀⢀⣀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⢀⣀⣀⣀⣀⣀⣀⣀⠀⠀⠀⠁⠀⠀⠣⣤⣀⡼⠃⠀⢀⡴⠋⠈⠳⡄⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣴⣶⣿⡿⠿⠿⠟⠛⠛⠛⠛⠿⠿⣿⣿⣶⣤⣄⠀⠀⠀⠉⠀⢀⡴⠋⠀⠀⣠⠞⠁⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣾⣿⠿⠋⠉⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠻⢿⣿⣶⣄⠀⠀⠳⣄⠀⣠⠞⢁⡠⢶⡄⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⣿⠿⠋⠀⠀⢀⣴⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠑⢤⡈⠛⢿⣿⣦⡀⠈⠛⢡⠚⠃⠀⠀⢹⡆⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢀⣼⣿⠟⠁⠀⠀⠀⢀⣾⠃⠀⠀⢀⡀⠀⠀⠀⠀⠀⠀⠀⠀⢻⡆⠀⠀⢻⣦⠀⠙⢿⣿⣦⡀⠈⢶⣀⡴⠞⠋⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣠⣿⡿⠃⠀⠀⠀⠀⢀⣾⡇⢀⡄⠀⢸⡇⠀⠀⠀⠀⠀⠀⣀⠀⢸⣷⡀⠀⠀⠹⣷⡀⠀⠙⢿⣷⡀⠀⠉⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣰⣿⡟⠀⠀⠀⠀⠀⠀⣾⣿⠃⣼⡇⠀⢸⡇⠀⠀⠀⠀⠀⠀⣿⠀⢸⣿⣷⡀⠀⢀⣾⣿⡤⠐⠊⢻⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢠⣿⣿⣼⡇⠀⠀⠀⠀⢠⣿⠉⢠⣿⠧⠀⣸⣇⣠⡄⠀⠀⠀⠀⣿⠠⢸⡟⠹⣿⡍⠉⣿⣿⣧⠀⠀⠀⠻⣿⣶⣄⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢸⣿⣿⡟⠀⠀⠀⠀⠀⣼⡏⢠⡿⣿⣦⣤⣿⡿⣿⡇⠀⠀⠀⢸⡿⠻⣿⣧⣤⣼⣿⡄⢸⡿⣿⡇⠀⠀⢠⣌⠛⢿⣿⣶⣤⣤⣄⡀
⠀⠀⠀⣀⣤⣿⣿⠟⣀⠀⠀⠀⠀⠀⣿⢃⣿⠇⢿⣯⣿⣿⣇⣿⠁⠀⠀⠀⣾⡇⢸⣿⠃⠉⠁⠸⣿⣼⡇⢻⡇⠀⠀⠀⢿⣷⣶⣬⣭⣿⣿⣿⠇
⣾⣿⣿⣿⣿⣻⣥⣾⡇⠀⠀⠀⠀⠀⣿⣿⠇⠀⠘⠿⠋⠻⠿⠿⠶⠶⠾⠿⠿⠍⢛⣧⣰⠶⢀⣀⣼⣿⣴⡸⣿⠀⠀⠀⠸⣿⣿⣿⠉⠛⠉⠀⠀
⠘⠛⠿⠿⢿⣿⠉⣿⠁⠀⠀⠀⠀⢀⣿⡿⣶⣶⣶⣤⣤⣤⣀⣀⠀⠀⠀⠀⠀⠀⢀⣭⣶⣿⡿⠟⠋⠉⠀⠀⣿⠀⡀⡀⠀⣿⣿⣿⡆⠀⠀⠀⠀
⠀⠀⠀⠀⣼⣿⠀⣿⠀⠀⠸⠀⠀⠸⣿⠇⠀⠀⣈⣩⣭⣿⡿⠟⠃⠀⠀⠀⠀⠀⠙⠛⠛⠛⠛⠻⠿⠷⠆⠀⣯⠀⠇⡇⠀⣿⡏⣿⣧⠀⠀⠀⠀
⠀⠀⠀⠀⢿⣿⡀⣿⡆⠀⠀⠀⠀⠀⣿⠰⠿⠿⠛⠋⠉⠀⠀⢀⣴⣶⣶⣶⣶⣶⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣧⠀⠀⠀⣿⡇⣿⣿⠀⠀⠀⠀
⠀⠀⠀⠀⢸⣿⡇⢻⣇⠀⠘⣰⡀⠀⣿⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⠀⠀⠀⠀⢸⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣿⠀⠀⠀⣿⣧⣿⡿⠀⠀⠀⠀
⠀⠀⠀⠀⠈⣿⣧⢸⣿⡀⠀⡿⣧⠀⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⣿⡄⠀⠀⠀⣼⡇⠀⠀⠀⠀⠀⠀⢀⣤⣾⡟⢡⣶⠀⢠⣿⣿⣿⠃⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠹⣿⣿⣿⣷⠀⠇⢹⣷⡸⣿⣶⣦⣄⣀⡀⠀⠀⠀⣿⡇⠀⠀⢠⣿⠁⣀⣀⣠⣤⣶⣾⡿⢿⣿⡇⣼⣿⢀⣿⣿⠿⠏⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠈⠛⠛⣿⣷⣴⠀⢹⣿⣿⣿⡟⠿⠿⣿⣿⣿⣿⣾⣷⣶⣿⣿⣿⣿⡿⠿⠟⠛⠋⠉⠀⢸⣿⣿⣿⣿⣾⣿⠃⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⣿⣦⣘⣿⡿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠛⠛⠻⠿⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠻⣿⣿⣿⠈⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
"""

# Lista de paquetes a instalar
packages_list = [
    "fastfetch",
    "xorg",
    "icewm",
    "lxterminal",
    "alsa-utils",
    "micro",
    "vlc",
    "falkon",
    "pcmanfm",
    "synaptic",
    "netsurf-gtk",
    "git",
    "gcc",
    "g++",
    "flatpak",
    "libreoffice",
    "x11-xserver-utils",
    "papirus-icon-theme",
    "fonts-inter",
    "adwaita-icon-theme",
    "gnome-themes-extra",
    "nitrogen",
    "gnome-backgrounds"
]

# Lista de paquetes flatpak a instalar
flatpak_list = [
    "info.febvre.Komikku",
    "io.github.libvibrant.vibrantLinux",
    "it.mijorus.gearlever"
]

## Cerrar el script si no esta en modo superusuario
if os.getuid() != 0:
    sys.exit()

print("Iniciando script de configuración...")
time.sleep(1.0)

# Instalar todos los paquetes antes de configurar
print(f"Instalando paquetes...")
subprocess.run(["apt", "install", "--no-install-recommends", "-y"] + packages_list, check=True)
time.sleep(1.0)

print("Configurando gestor de sesión Ly...")

subprocess.run(["git", "clone", "--recurse-submodules", "https://github.com/fairyglade/ly.git"], check=True)

# Ir al directorio de Ly descargado desde Git
os.chdir("ly")

# Lista de paquetes necesarios para instalar Ly
ly_build_packages = [
    "build-essential",
    "libpam0g-dev",
    "libxcb-xkb-dev", 
    "xauth", 
    "xserver-xorg", 
    "brightnessctl"
]

# Instalar los paquetes que Ly necesita
subprocess.run(["apt", "install", "-y"] + ly_build_packages, check=True)

# Compilar
subprocess.run(["make"], check=True)
subprocess.run(["make", "install"], check=True)

# Activar Ly
subprocess.run(["systemctl", "enable", "ly"], check=True)

time.sleep(1.0)

print("Configurando fastfetch...")
# Crear directorio de fastfetch si no existe
if not pathlib.Path(fast_path).is_dir():
    os.mkdir(fast_path)
    # Cambiar la propiedad de la carpeta al usuario original
    os.chown(fast_path, uid, gid)

# Crear el archivo de logo para el fastfetch
with open(os.path.join(fast_path, "logo.txt"), "w", encoding="utf-8") as file:
    file.write(girl_art)
os.chown(os.path.join(fast_path, "logo.txt"), uid, gid)

# Crear archivo de configuración de fastfetch
if not pathlib.Path(os.path.join(fast_path, "config.jsonc")).is_file():
    with open(fast_path + "/config.jsonc", "w", encoding="utf-8") as file:
        json.dump(fastfetch_config, file, indent=4)
os.chown(fast_path + "/config.jsonc", uid, gid)

# Comprobar que se haya colocado el arte
subprocess.run(["fastfetch"])

time.sleep(1.0)

print("Configurando Flatpak...")
# Agregar repositorio de Flatpak
subprocess.run(["flatpak", "remote-add", "--if-not-exists", "flathub", "https://dl.flathub.org/repo/flathub.flatpakrepo"], check=True)

print("Instalando paquetes flatpak...")
subprocess.run(["flatpak", "install", "-y", "flathub"] + flatpak_list, check=True)

time.sleep(1.0)

print("Configurando GTK...")

# Crear directorio de configuración de GTK
if not pathlib.Path(os.path.join(gtk_path)).is_dir():
    os.mkdir(gtk_path)
    os.chown(gtk_path, uid, gid)

# Crear archivo de configuración para GTK
gtk_settings_file = os.path.join(gtk_path, "settings.ini")
if not pathlib.Path(os.path.join(gtk_settings_file)).is_file():

    settings_file = """[Settings]
gtk-icon-theme-name=Papirus-Dark
gtk-theme-name=Adwaita-dark
gtk-font-name=Sans 10
gtk-cursor-theme = Adwaita
    """

    # Guardar configuraciones en el archivo
    with open(gtk_settings_file, "w", encoding="utf-8") as file:
        file.write(settings_file)

time.sleep(1.0)

print("Configurando IceWM...")

# Crear directorio de configuración de IceWM
if not pathlib.Path(ice_path).is_dir():
    os.mkdir(ice_path)
    os.chown(ice_path, uid, gid)

# Si el archivo de configuración de inicio si no esta, crearlo
if not pathlib.Path(startup_file).is_file():
    startup_content = """#!/bin/bash

# Detectar automáticamente la pantalla conectada en tiempo de ejecución
monitor=$(xrandr | grep ' connected' | awk '{print $1}' | head -n 1)

# Ejecutar VibrantLinux en segundo plano si hay monitor activo
if [ ! -z "$monitor" ]; then
    flatpak run --command=vibrant-cli io.github.libvibrant.vibrantLinux "$monitor" 1.8 &
fi

# Restaurar el fondo de pantalla
nitrogen --restore &
    """
    # Crear el archivo de inicio 
    with open(startup_file, "w", encoding="utf-8") as file:
        file.write(startup_content)

    # Cambiar propietario
    os.chown(startup_file, uid, gid)
    # Permitir ejecución
    os.chmod(startup_file, 0o755)

time.sleep(1.0)

print("Configurando Nitrogen...")

nitrogen_path = f"/home/{username}/.config/nitrogen"

# Crear directorio de configuración de Nitrogen
if not pathlib.Path(nitrogen_path).is_dir():
    os.makedirs(nitrogen_path, exist_ok=True)
    os.chown(nitrogen_path, uid, gid)

# Archivo que guarda el fondo actual
bg_saved_file = os.path.join(nitrogen_path, "bg-saved.cfg")
bg_saved_content = """[xin_-1]
file=/usr/share/backgrounds/gnome/design-is-rounded-rectangles-d.jpg
mode=4
bgcolor=#000000
"""
with open(bg_saved_file, "w", encoding="utf-8") as file:
    file.write(bg_saved_content)
os.chown(bg_saved_file, uid, gid)

# Configuración de Nitrogen por defecto
nitrogen_cfg_file = os.path.join(nitrogen_path, "nitrogen.cfg")
nitrogen_cfg_content = f"""[geometry]
posx=100
posy=100
sizex=600
sizey=600

[nitrogen]
view=icon
recurse=true
sort=alpha
icon_caps=false
dirs=/home/{username}/.config/backgrounds;/usr/share/backgrounds/gnome;
"""
with open(nitrogen_cfg_file, "w", encoding="utf-8") as file:
    file.write(nitrogen_cfg_content)
os.chown(nitrogen_cfg_file, uid, gid)

print("Configuración terminada, reiniciando...")
time.sleep(0.5)

subprocess.run(["reboot"])