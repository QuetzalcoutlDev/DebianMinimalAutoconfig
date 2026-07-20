# Script de automatización para Debian 13 Minimal

Script de automatización pensado para una Orange Pi Zero 2W pero que en general puede ser ejecutado en cualquier instalación minimal.

Aunque antes que nada se debera ejecutar el script `start_minimal.sh` con sudo
```bash
sudo bash start_minimal.sh
```

Del resto, el script `debian_autoconfig.py` hará el trabajo de configuración

Este script instala los siguientes paquetes:
```
fastfetch
ly
xorg
icewm
lxterminal
alsa-utils
micro
vlc
falkon
pcmanfm
synaptic
netsurf-gtk
git
gcc
g++
flatpak
libreoffice
x11-xserver-utils
papirus-icon-themes
fonts-inter
adwaita-icon-theme
gnome-theme-extras
adwaita-cursor-theme
feh
gnome-backgrounds
```