### Este script continue todas las variables que comparten todos los demás scripts

import os, subprocess, pathlib, platform

from time import sleep

# Obtener el usuario que llamo a sudo
username = os.getenv("SUDO_USER") 

## Rutas generales
base_config_path = f"/home/{username}/.config"
fast_path = f"/home/{username}/.config/fastfetch"
gtk_path = f"/home/{username}/.config/gtk-3.0"

# Obtener IDs de usuario (el que llamo a sudo)
UID = int(os.getenv("SUDO_UID"))
GID = int(os.getenv("SUDO_GID"))

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

# Lista de paquetes generales a instalar
packages_list = [
    "fastfetch",
    "xorg",      
    "alsa-utils",
    "vlc",
    "falkon",
    "synaptic",
    "gcc",
    "g++",
    "flatpak",
    "x11-xserver-utils",
    "papirus-icon-theme",
    "dmz-cursor-theme",
    "fonts-inter",
    "htop",
    "xdg-user-dirs",
    "gvfs",
    "gvfs-backends",
    "ntfs-3g",
    "fuse",
    "udisks2",
    "pulseaudio",
    "pavucontrol",
    "network-manager",
    "kdeconnect",
    "micro",
    "librsvg2-common",
    "shared-mime-info",
    "abiword",
    "gnumeric",
    "upower",
    "bluez",           
    "bluez-utils",
    "xdg-utils",
    "xdg-desktop-portal",
    "dbus-x11",
    "libfile-mimeinfo-perl",
    "bluez-alsa-utils",
    "bluez-firmware",
    "cpufrequtils"
]

# Lista de paquetes flatpak a instalar
flatpak_list = [
    "info.febvre.Komikku"
    #"io.github.libvibrant.vibrantLinux",
    #"it.mijorus.gearlever"
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

# Configuración para zram (Por ahora no es necesario)
def zram_settings():

    zram_conf = """PERCENT=50
ALGO=zstd
PRIORITY=100
    """
    print("Configurando ZRAM...")

    subprocess.run(["apt", "install", "zram-tools", "-y"] + packages_list, check=True)

    with open("/etc/default/zramswap", "w", encoding="utf-8") as file:
        file.write(zram_conf)

    # Habilitar e iniciar el servicio zramswap
    subprocess.run(["systemctl", "restart", "zramswap.service"], check=True)

    sleep(1.0)

# Configuración de GTK
def gtk_settings():
    # Crear directorio de configuración de GTK
    if not pathlib.Path(os.path.join(gtk_path)).is_dir():
        print("Configurando GTK...")

        os.makedirs(gtk_path, exist_ok=True)
        os.chown(gtk_path, UID, GID)

    # Crear archivo de configuración para GTK
    gtk_settings_file = os.path.join(gtk_path, "settings.ini")
    if not pathlib.Path(os.path.join(gtk_settings_file)).is_file():
        settings_file = """[Settings]
gtk-icon-theme-name=Papirus-Dark
gtk-theme-name=Arc-Dark
gtk-font-name=Sans 10
gtk-cursor-theme = DMZ-Black
    """
    # Guardar configuraciones en el archivo
    with open(gtk_settings_file, "w", encoding="utf-8") as file:
        file.write(settings_file)

    sleep(1.0)

    os.chown(gtk_settings_file, UID, GID)

def ice_install():
    packages = [
        "icewm",
        "lxterminal",          
        "geany",
        "pcmanfm",
        "fonts-inter",
        "gnome-themes-extra",
        "gnome-backgrounds",
        "nitrogen",
        "dunst",
        "nomacs",
        "network-manager-gnome",
        "nm-tray",
        "volumeicon-alsa",
        "lxappearance",
        "flameshot",
        "qt5ct",
        "qt6ct",
        "qt-style-kvantum",
        "qt-style-kvantum-themes",
        "qt6-svg-plugins",
        "l3adpad",  
        "policykit-1-gnome",
        "blueman",
        "xdg-desktop-portal-gtk",
        "xdg-user-dirs-gtk",
        "arc-theme"
    ]

    print("Instalando dependencias para IceWM...")
    subprocess.run(["apt", "install", "-y"] + packages + ly_packages, check=True)

    gtk_settings()

    print("Configurando Ly...")
    sleep(1.0)

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

    print("Creando Swap temporal...")
    subprocess.run(["fallocate", "-l", "1G", "/swapfile"], check=True)
    subprocess.run(["chmod", "600", "/swapfile"], check=True)
    subprocess.run(["mkswap", "/swapfile"], check=True)
    subprocess.run(["swapon", "/swapfile"], check=True)

    print("Compilando Ly...")

    # Compilar Ly usando Zig y generar el servicio systemd
    subprocess.run(["zig", "build"], cwd=ly_repo_dir, check=True)
    subprocess.run(["zig", "build", "installexe", "-Dinit_system=systemd"], cwd=ly_repo_dir, check=True)

    print("Configurando Ly...")

    subprocess.run(["systemctl", "enable", "ly@tty2.service"], check=True)
    subprocess.run(["systemctl", "disable", "getty@tty2.service"], check=True)
    subprocess.run(["ln", "-sf", "/sbin/agetty", "/usr/bin/agetty"], check=True)

    print("Limpiando Swap temporal...")

    subprocess.run(["swapoff", "/swapfile"], check=False)
    subprocess.run(["rm", "-f", "/swapfile"], check=True)

    sleep(1.0)

    print("Configurando Nitrogen...")
    nitrogen_dir = f"{base_config_path}/nitrogen"
    if not pathlib.Path(nitrogen_dir).is_dir():
        os.makedirs(nitrogen_dir, exist_ok=True)
        os.chown(nitrogen_dir, UID, GID)

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
    os.chown(f"{nitrogen_dir}/nitrogen.cfg", UID, GID)

    sleep(1.0)

    print("Configurando IceWM...")
    icewm_dir = f"/home/{username}/.icewm"
    if not pathlib.Path(icewm_dir).is_dir():
        os.makedirs(icewm_dir, exist_ok=True)
        os.chown(icewm_dir, UID, GID)

    # Script de inicio de IceWM
    startup_file = os.path.join(icewm_dir, "startup")
    startup_content = """#!/bin/bash

export QT_QPA_PLATFORMTHEME="qt5ct"

# Restaurar el fondo de pantalla
nitrogen --restore &

/usr/bin/dunst &
volumeicon &
nm-applet &

"""

    with open(startup_file, "w", encoding="utf-8") as file:
        file.write(startup_content)

    # Hacer ejecutable el script de inicio y cambiar propietario
    os.chmod(startup_file, 0o755)
    os.chown(startup_file, UID, GID)

    ice_keys = os.path.join(icewm_dir, "keys")
    ice_keys_content = """
    key "Super+Shift+s" flameshot gui
    """
    if not pathlib.Path(ice_keys).is_file():
        # Escribir el archivo keys
        with open(ice_keys, "w", encoding="utf-8") as file: 
            file.write(ice_keys_content)

        # cambiar el propietario
        os.chown(ice_keys, UID, GID)

    sleep(1.0)

    print("Configurando PCManFM...")

    # Rutas de configuracion para la entrada personalizada del menu contextual
    local_paths = [
        f"/home/{username}/.local",
        f"/home/{username}/.local/share",
        f"/home/{username}/.local/share/file-manager",
        f"/home/{username}/.local/share/file-manager/actions"
    ]

    # Crear las carpetas
    for p in local_paths:
        if not pathlib.Path(p).is_dir():
            os.makedirs(p, exist_ok=True)
            os.chown(p, UID, GID)


def xfce_install():
    packages = [
        "xfce4",                   
        "xfce4-goodies",          
        "xfce4-power-manager",
        "xfce4-pulseaudio-plugin",
        "thunar",
        "thunar-volman",
        "tumbler",
        "qt5ct",
        "qt6ct",
        "qt-style-kvantum",
        "qt-style-kvantum-themes",
        "librsvg2-common",
        "qt6-svg-plugins",
        "blueman",
        "xdg-desktop-portal-gtk",
        "xdg-user-dirs-gtk",
        "arc-theme",
        "lightdm",
        "lightdm-gtk-greeter",
        "lightdm-settings",
        "network-manager-gnome"
    ]

    print("Instalando dependencias para XFCE...")
    subprocess.run(["apt", "install", "-y"] + packages, check=True)

    gtk_settings()

    sleep(1.0)

def lxqt_install():
    packages = [
        "lxqt",
        "openbox",             
        "obconf",
        "lightdm",
        "lightdm-gtk-greeter",
        "lightdm-settings",
        "xdg-desktop-portal-lxqt",
        "nm-tray"
    ]

    print("Instalando dependencias para LXQt...")
    subprocess.run(["apt", "install", "-y"] + packages, check=True)

    # Ruta del directorio de configuración de LXQt
    lxqt_config_dir = f"/home/{username}/.config/lxqt"

    if not pathlib.Path(os.path.join(lxqt_config_dir)).is_dir():
        print("Configurando LXQt...")

        os.makedirs(lxqt_config_dir, exist_ok=True)
        # Cambiar propietario del directorio
        os.chown(lxqt_config_dir, UID, GID)

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
        os.chown(lxqt_conf_path, UID, GID)

    # Configuración de gestor de ventanas
    session_conf_content = """[General]
window_manager=openbox
"""

    session_conf_path = os.path.join(lxqt_config_dir, "session.conf")
    if not pathlib.Path(os.path.join(session_conf_path)).is_file():
        with open(session_conf_path, "w", encoding="utf-8") as file:
            file.write(session_conf_content)

        # Cambiar propietario del archivo de sesión
        os.chown(session_conf_path, UID, GID)

    # Rutas para la configuración de PCManFM-Qt
    pcman_base_dir = f"/home/{username}/.config/pcmanfm-qt"
    pcman_config_dir = f"{pcman_base_dir}/lxqt"

    # Crear los directorios si no existen
    if not pathlib.Path(pcman_config_dir).is_dir():
        os.makedirs(pcman_config_dir, exist_ok=True)

    # Contenido de configuración: Fondo por defecto y selección estricta de iconos
    pcman_conf_content = """[Desktop]
DesktopShortcuts=Home, Trash
"""

    pcman_conf_path = os.path.join(pcman_config_dir, "settings.conf")
    if not pathlib.Path(pcman_conf_path).is_file():
        with open(pcman_conf_path, "w", encoding="utf-8") as file:
            file.write(pcman_conf_content)

    # Corregir permisos
    os.chown(pcman_conf_path, UID, GID)
    os.chown(pcman_config_dir, UID, GID)
    os.chown(pcman_base_dir, UID, GID)

    # Configurar el icono del menú inicio
    panel_conf_path = os.path.join(lxqt_config_dir, "panel.conf")
    panel_conf_content = """[mainmenu]
icon=/usr/share/lxqt/graphics/helix_white_shadow.png
ownIcon=true
categoriesAtRight=false
"""

    with open(panel_conf_path, "w", encoding="utf-8") as file:
        file.write(panel_conf_content)
    os.chown(panel_conf_path, UID, GID)

    sleep(1.0)