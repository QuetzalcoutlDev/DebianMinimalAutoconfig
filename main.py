#############################################################################
#######  Script de automatización en Python, para Debian 13 Minimal  #######
#############################################################################

### versión 2.0

# Esta nueva versión, tiene un script principal que instala todas las dependencias que comparten todos los entornos de escritorio
# pero con diferencias para cada uno

import autoconfig, sys, os, subprocess, pathlib, json

from time import sleep

## Cerrar el script si no esta en modo superusuario
if os.getuid() != 0:
    sys.exit()

# Guardar el ID del escritorio a instalar
desktop_id = sys.argv[1]
# print("ID = " + desktop_id, " type = ", type(desktop_id))

print("Iniciando script de configuración...")

# Asegurar que .config exista y sea del usuario antes de crear subcarpetas
if not pathlib.Path(autoconfig.base_config_path).is_dir():
    os.makedirs(autoconfig.base_config_path, exist_ok=True)
    os.chown(autoconfig.base_config_path, autoconfig.UID, autoconfig.GID)

sleep(0.5)

print("Instalando dependencias generales...")
subprocess.run(["apt", "install", "--no-install-recommends", "-y"] + autoconfig.packages_list, check=True)
sleep(1.0)

print("Configurando fastfetch...")
# Crear directorio de fastfetch si no existe
if not pathlib.Path(autoconfig.fast_path).is_dir():
    os.makedirs(autoconfig.fast_path, exist_ok=True)
    # Cambiar la propiedad de la carpeta al usuario original
    os.chown(autoconfig.fast_path, autoconfig.UID, autoconfig.GID)

# Crear el archivo de logo para el fastfetch
with open(os.path.join(autoconfig.fast_path, "logo.txt"), "w", encoding="utf-8") as file:
    file.write(autoconfig.girl_art)
os.chown(os.path.join(autoconfig.fast_path, "logo.txt"), autoconfig.UID, autoconfig.GID)

# Crear archivo de configuración de fastfetch
if not pathlib.Path(os.path.join(autoconfig.fast_path, "config.jsonc")).is_file():
    with open(autoconfig.fast_path + "/config.jsonc", "w", encoding="utf-8") as file:
        json.dump(autoconfig.fastfetch_config, file, indent=4)
os.chown(autoconfig.fast_path + "/config.jsonc", autoconfig.UID, autoconfig.GID)

sleep(1.0)

print("Configurando Flatpak...")
# Agregar repositorio de Flatpak
subprocess.run(["flatpak", "remote-add", "--if-not-exists", "flathub", "https://dl.flathub.org/repo/flathub.flatpakrepo"], check=True)

print("Instalando paquetes flatpak...")
subprocess.run(["flatpak", "install", "-y", "--no-related", "flathub"] + autoconfig.flatpak_list, check=True)

sleep(1.0)

# Instalación de los entornos
match desktop_id:
    case "0": autoconfig.lxqt_install()
    case "1": autoconfig.ice_install()
    case "2": autoconfig.xfce_install()

print("Creando directorios de usuario...")
# Ejecutar xdg-user-dirs con los privilegios del usuario para que cree las carpetas en su home
subprocess.run(["runuser", "-l", autoconfig.username, "-c", "xdg-user-dirs-update"], check=True)

sleep(1.0)

print("Configuración terminada, reiniciando...")
sleep(0.5)

subprocess.run(["reboot"])