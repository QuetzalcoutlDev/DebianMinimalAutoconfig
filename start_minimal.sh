#!/bin/bash

## Script de automatización para dejar a Debian 13 Minimal al 100% usable usando Bash y Python

# Entornos a seleccionar
desktops=("lxqt" "icewm" "xfce")
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

read -p "Entorno a instalar: 0=lxqt 1=icewm 2=xfce " -n 1 response
echo ""

if [[ $response != "0" && $response != "1" && $response != "2" ]]; then
  echo "Opción no valida..."
  exit 1
fi

sleep 0.5
echo "Ejecutando script de automatización de Python..."

# Ejecutar el script principal
python3 main.py $response