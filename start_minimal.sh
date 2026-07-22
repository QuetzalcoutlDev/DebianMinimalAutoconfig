#!/bin/bash

## Script de automatización para dejar a Debian 13 Minimal al 100% usable usando Bash y Python

# Entornos a seleccionar
desktops=("lxqt" "icewm")
desktop_number=0

# Verificar si el script se está ejecutando como root
if [ "$EUID" -ne 0 ]; then
  echo "Ejecuta este script usando sudo: sudo bash $0"
  exit 1
fi

sleep 0.5
echo "Iniciando configuración..."
sleep 1

echo "Actualizando repositorios y sistema antes de instalar todo lo necesario"
apt update && apt upgrade -y

sleep 0.5 

echo "Instalando Python..."
apt install -y python3 python3-pip
sleep 1

read -p "Entorno a instalar: 0=lxqt 1=icewm " -n 1 response

if [ $response -eq 0 ]; then
  desktop_number=0

  echo ""

elif [ $response -eq 1 ]; then 
  desktop_number=1

  echo ""

else
  echo "Opción no valida..."
  exit 1
fi

# Se elimino el if para descargar el .py, lo normal es clonar el repo antes
echo "Ejecutando script de automatización de Python..."

SCRIPT_NAME="debian_autoconfig_${desktops[$desktop_number]}.py"

python3 "$SCRIPT_NAME"