# Script de automatización para Debian 13 Minimal

Script de automatización pensado para una Orange Pi Zero 2W pero que en general puede ser ejecutado en cualquier instalación minimal.

## Pasos

Deberás descargar el script principal, clonando este repo de Git, por lo que en su instalación minima debes hacer:

```bash
sudo apt install git
```

Después de la instalación deberás hacer esto:

```bash
git clone https://github.com/QuetzalcoutlDev/DebianMinimalAutoconfig.git
cd DebianMinimalAutoconfig
```

Una vez descargado, se debera ejecutar el script `start_minimal.sh` con sudo:

```bash
sudo bash start_minimal.sh
```

Del resto, el script `debian_autoconfig.py` hará el trabajo de configuración

Este script instala los siguientes paquetes (Algunos se instalan segun si se escoje lxqt o icewm):
```
fastfetch
xorg
lxqt
icewm
lxterminal
openbox
obconf
alsa-utils
geany
vlc
falkon
pcmanfm
synaptic
netsurf-gtk
gcc
g++
flatpak
libreoffice
x11-xserver-utils
papirus-icon-theme
fonts-inter
adwaita-icon-theme
gnome-themes-extra
gnome-backgrounds
lightdm
lightdm-gtk-greeter
lightdm-settings
zram-tools
htop
xdg-user-dirs
xdg-user-dirs-gtk
gvfs
gvfs-backends
ntfs-3g
fuse
nitrogen
```