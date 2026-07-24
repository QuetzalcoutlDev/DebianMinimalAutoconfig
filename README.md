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
```bash
fastfetch
xorg
lxqt
icewm
lxterminal  # Solo IceWm
openbox
obconf # Solo LXQt
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
lightdm # Solo LXQt
lightdm-gtk-greeter # Solo LXQt
lightdm-settings # Solo LXQt
zram-tools
htop
xdg-user-dirs
xdg-user-dirs-gtk
gvfs
gvfs-backends
ntfs-3g
fuse
nitrogen  # Solo IceWm
zig # Solo IceWm
ly # Solo IceWm y se compila
dunst # Solo IceWm 
network-manager # Solo IceWm
network-manager-gnome # Solo IceWm
nm-tray # Solo IceWm
volumeicon-alsa # Solo IceWm
lxappearance
nomacs # Solo IceWm
udisks2 
pulseaudio
pavucontrol
flameshot # Solo IceWm
qt5ct # Solo IceWm
mpv 
qt6ct # Solo IceWm
qt-style-kvantum # Solo IceWm
qt-style-kvantum-themes # Solo IceWm
kdeconnect
```