#############################################################################
#######  Script de automatización en Python, para Debian 13 Minimal  #######
#############################################################################

### versión 1.2

import os, subprocess, sys, time, json, pathlib, platform

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
    "zram-tools",
    "htop",
    "xdg-user-dirs",
    "xdg-user-dirs-gtk",
    "gvfs",
    "gvfs-backends",
    "ntfs-3g",
    "fuse",
    "nitrogen"
]

# Lista de paquetes flatpak a instalar
flatpak_list = [
    "info.febvre.Komikku",
    "io.github.libvibrant.vibrantLinux",
    "it.mijorus.gearlever"
]

# Dependencias de Ly
ly_packages = [
    "build-essential", 
    "libpam0g-dev",
    "libxcb-xkb-dev", 
    "xauth", 
    "xserver-xorg", 
    "brightnessctl",
    "curl",
    "ca-certificates",
    "xserver-xorg-legacy"
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

print("Configurando ZRAM...")

# Configuración para zram
zram_conf = """PERCENT=50
ALGO=zstd
PRIORITY=100
"""
with open("/etc/default/zramswap", "w", encoding="utf-8") as file:
    file.write(zram_conf)

# Habilitar e iniciar el servicio zramswap
subprocess.run(["systemctl", "enable", "zramswap"], check=True)
subprocess.run(["systemctl", "start", "zramswap"], check=True)

time.sleep(1.0)

print("Configurando Ly...")
time.sleep(1.0)

arch_name = platform.machine()
zig_url = f"https://ziglang.org/download/0.16.0/zig-{arch_name}-linux-0.16.0.tar.xz"

print(f"Instalando dependencias de Ly...")
subprocess.run(["apt", "install", "-y"] + ly_packages, check=True)

# Descargar Zig si no existe
if not pathlib.Path("/tmp/zig.tar.xz").is_file():
    print("Descargando Zig...")
    subprocess.run(["wget", "-qO", "/tmp/zig.tar.xz", zig_url], check=True)
    print("Descomprimiendo Zig...")
    subprocess.run(["tar", "-xf", "/tmp/zig.tar.xz", "-C", "/opt/"], check=True)

# Crear enlace simbólico para usar 'zig'
print("Creando enlace a Zig...")
subprocess.run(["ln", "-sf", f"/opt/zig-{arch_name}-linux-0.16.0/zig", "/bin/zig"], check=True)

ly_repo_dir = "/tmp/ly_build"

if not pathlib.Path(ly_repo_dir).is_dir():
    subprocess.run(["git", "clone", "--recurse-submodules", "https://github.com/fairyglade/ly", ly_repo_dir], check=True)

# Compilar Ly usando Zig y generar el servicio systemd
subprocess.run(["zig", "build"], cwd=ly_repo_dir, check=True)
subprocess.run(["zig", "build", "installexe", "-Dinit_system=systemd"], cwd=ly_repo_dir, check=True)

print("Configurando Ly...")

subprocess.run(["systemctl", "enable", "ly@tty2.service"], check=True)
subprocess.run(["systemctl", "disable", "getty@tty2.service"], check=True)
subprocess.run(["ln", "-sf", "/sbin/agetty", "/usr/bin/agetty"], check=True)

time.sleep(1.0)

print("Configurando Nitrogen...")
nitrogen_dir = f"{base_config_path}/nitrogen"
if not pathlib.Path(nitrogen_dir).is_dir():
    os.makedirs(nitrogen_dir, exist_ok=True)
    os.chown(nitrogen_dir, uid, gid)

# Configuración principal de Nitrogen
nitrogen_cfg = """[geometry]
posx=0
posy=0
sizex=800
sizey=600

[nitrogen]
view=icon
recurse=true
sort=alpha
icon_caps=false
dirs=/usr/share/backgrounds/gnome;
"""
with open(f"{nitrogen_dir}/nitrogen.cfg", "w", encoding="utf-8") as file:
    file.write(nitrogen_cfg)
os.chown(f"{nitrogen_dir}/nitrogen.cfg", uid, gid)

time.sleep(1.0)

print("Configurando IceWM...")
icewm_dir = f"/home/{username}/.icewm"
if not pathlib.Path(icewm_dir).is_dir():
    os.makedirs(icewm_dir, exist_ok=True)
    os.chown(icewm_dir, uid, gid)

# Script de inicio de IceWM
startup_file = os.path.join(icewm_dir, "startup")
startup_content = """#!/bin/bash
# Restaurar el fondo de pantalla
nitrogen --restore &
"""
with open(startup_file, "w", encoding="utf-8") as file:
    file.write(startup_content)

# Hacer ejecutable el script de inicio y cambiar propietario
os.chmod(startup_file, 0o755)
os.chown(startup_file, uid, gid)

time.sleep(1.0)

print("Creando directorios de usuario...")
# Ejecutar xdg-user-dirs con los privilegios del usuario para que cree las carpetas en su home
subprocess.run(["runuser", "-l", username, "-c", "xdg-user-dirs-update"], check=True)

time.sleep(1.0)
print("Configuración terminada, reiniciando...")
time.sleep(0.5)

subprocess.run(["reboot"])