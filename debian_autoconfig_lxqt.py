#############################################################################
#######  Script de automatización en Python, para Debian 13 Minimal  #######
#############################################################################

### versión 1.2

import os, subprocess, sys, time, json, pathlib

# Obtener el usuario que llamo a sudo
username = os.getenv("SUDO_USER") 

## Rutas generales
base_config_path = f"/home/{username}/.config"
fast_path = f"/home/{username}/.config/fastfetch"
gtk_path = f"/home/{username}/.config/gtk-3.0"

# Obtener IDs de usuario (el que llamo a sudo)
uid = int(os.getenv("SUDO_UID"))
gid = int(os.getenv("SUDO_GID"))

# Diccionario de configuración de fastfetch
fastfetch_config = {
  "$schema": "https://github.com/fastfetch-cli/fastfetch/raw/master/doc/json_schema.json",
    "logo": {
        "type": "file",
        "source": f"{fast_path}/logo.txt",
        "position": "top"
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
    "lxqt",
    "openbox",             
    "obconf",
    "alsa-utils",
    "geany",
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
    "gnome-backgrounds",
    "lightdm",
    "lightdm-gtk-greeter",
    "lightdm-settings",
    # "zram-tools",
    "htop",
    "xdg-user-dirs",
    "xdg-user-dirs-gtk",
    "gvfs",
    "gvfs-backends",
    "ntfs-3g",
    "fuse",
    "pulseaudio",
    "pavucontrol",
    "lxappearance",
    "kdeconnect",
    "udisks2"
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

# Asegurar que .config exista y sea del usuario antes de crear subcarpetas
if not pathlib.Path(base_config_path).is_dir():
    os.makedirs(base_config_path, exist_ok=True)
    os.chown(base_config_path, uid, gid)

time.sleep(1.0)

# Instalar todos los paquetes antes de configurar
print(f"Instalando paquetes...")
subprocess.run(["apt", "install", "--no-install-recommends", "-y"] + packages_list, check=True)
time.sleep(1.0)

lightdm_conf_path = "/etc/lightdm/lightdm.conf"
lightdm_conf = f"""[Seat:*]
autologin-guest=false
autologin-user={username}
autologin-user-timeout=0
"""

# Escribir la configuración de autologin
if not pathlib.Path(lightdm_conf_path).is_file():

    print("Configurando LightDM...")
    with open(lightdm_conf_path, "w", encoding="utf-8") as file:
        file.write(lightdm_conf)

    # Activar Lightdm
    subprocess.run(["systemctl", "enable", "lightdm"], check=True)

    time.sleep(1.0)

print("Configurando fastfetch...")
# Crear directorio de fastfetch si no existe
if not pathlib.Path(fast_path).is_dir():
    os.makedirs(fast_path, exist_ok=True)
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

time.sleep(1.0)

print("Configurando Flatpak...")
# Agregar repositorio de Flatpak
subprocess.run(["flatpak", "remote-add", "--if-not-exists", "flathub", "https://dl.flathub.org/repo/flathub.flatpakrepo"], check=True)

print("Instalando paquetes flatpak...")
subprocess.run(["flatpak", "install", "-y", "flathub"] + flatpak_list, check=True)

time.sleep(1.0)

# Crear directorio de configuración de GTK
if not pathlib.Path(os.path.join(gtk_path)).is_dir():
    print("Configurando GTK...")

    os.makedirs(gtk_path, exist_ok=True)
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

# Configuración para zram
zram_conf = """PERCENT=50
ALGO=zstd
PRIORITY=100
"""

"""
print("Configurando ZRAM...")

with open("/etc/default/zramswap", "w", encoding="utf-8") as file:
    file.write(zram_conf)

# Habilitar e iniciar el servicio zramswap
subprocess.run(["systemctl", "restart", "zramswap.service"], check=True)

time.sleep(1.0)
"""

# Ruta del directorio de configuración de LXQt
lxqt_config_dir = f"/home/{username}/.config/lxqt"

if not pathlib.Path(os.path.join(lxqt_config_dir)).is_dir():
    print("Configurando LXQt...")

    os.makedirs(lxqt_config_dir, exist_ok=True)
    # Cambiar propietario del directorio
    os.chown(lxqt_config_dir, uid, gid)

# Configuración de iconos predeterminados para LXQt
lxqt_conf_content = """[General]
__wer=false
theme=dark

[Appearance]
icon_theme=Papirus-Dark
theme=dark
"""

lxqt_conf_path = os.path.join(lxqt_config_dir, "lxqt.conf")
if not pathlib.Path(os.path.join(lxqt_conf_path)).is_file():
    with open(lxqt_conf_path, "w", encoding="utf-8") as file:
        file.write(lxqt_conf_content)

    # Cambiar propietario del archivo de sesión
    os.chown(lxqt_conf_path, uid, gid)

# Configuración de gestor de ventanas
session_conf_content = """[General]
window_manager=openbox
"""

session_conf_path = os.path.join(lxqt_config_dir, "session.conf")
if not pathlib.Path(os.path.join(session_conf_path)).is_file():
    with open(session_conf_path, "w", encoding="utf-8") as file:
        file.write(session_conf_content)

    # Cambiar propietario del archivo de sesión
    os.chown(session_conf_path, uid, gid)

# Rutas para la configuración de PCManFM-Qt
pcman_base_dir = f"/home/{username}/.config/pcmanfm-qt"
pcman_config_dir = f"{pcman_base_dir}/lxqt"

# Crear los directorios si no existen
if not pathlib.Path(pcman_config_dir).is_dir():
    os.makedirs(pcman_config_dir, exist_ok=True)

# Contenido de configuración: Fondo por defecto y selección estricta de iconos
pcman_conf_content = """[Desktop]
Wallpaper=/usr/share/backgrounds/gnome/adwaita-d.jpg
WallpaperMode=zoom
DesktopShortcuts=Home, Trash
"""

pcman_conf_path = os.path.join(pcman_config_dir, "settings.conf")
if not pathlib.Path(pcman_conf_path).is_file():
    with open(pcman_conf_path, "w", encoding="utf-8") as file:
        file.write(pcman_conf_content)

# Corregir permisos
os.chown(pcman_conf_path, uid, gid)
os.chown(pcman_config_dir, uid, gid)
os.chown(pcman_base_dir, uid, gid)

# Configurar el icono del menú inicio
panel_conf_path = os.path.join(lxqt_config_dir, "panel.conf")
panel_conf_content = """[mainmenu]
icon=/usr/share/lxqt/graphics/helix_white_shadow.png
ownIcon=true
categoriesAtRight=false
"""

with open(panel_conf_path, "w", encoding="utf-8") as file:
    file.write(panel_conf_content)
os.chown(panel_conf_path, uid, gid)

time.sleep(1.0)

print("Creando directorios de usuario...")
# Ejecutar xdg-user-dirs con los privilegios del usuario para que cree las carpetas en su home
subprocess.run(["runuser", "-l", username, "-c", "xdg-user-dirs-update"], check=True)

time.sleep(1.0)

print("Configuración terminada, reiniciando...")
time.sleep(0.5)

subprocess.run(["reboot"])