#!/bin/bash

## Script de automatización para dejar a Debian 13 Minimal al 100% usable usando Bash y Python

SCRIPT_NAME="debian_autoconfig.py"
GITHUB_URL="https://raw.githubusercontent.com/QuetzalcoutlDev/DebianMinimalAutoconfig/refs/heads/master/debian_autoconfig.py"

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

# Descargar el script de automatización
if [ ! -f "$SCRIPT_NAME" ]; then
  echo "Descargando script de automatización de Python..."

  # Descargar el script
  wget -O "$SCRIPT_NAME" "$GITHUB_URL"

  # Si el script se descargo
  if [ $? -eq 0 ]; then
    echo "Script descargado con exito."
    sleep 1
    echo "Ejecutando script de automatización de Python..."
  # Si el script no se descargo
  else
    echo "Error de descarga del script." >&2
    exit 1
  fi
else
  echo "Ejecutando script de automatización de Python..."
fi

python3 "$SCRIPT_NAME"