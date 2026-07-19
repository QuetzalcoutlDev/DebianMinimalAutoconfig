#!/bin/bash

## Script de automatización para dejar a Debian 13 Minimal al 100% usable usando Bash y Python

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

if [ ! -f ]

echo "Ejecutando script de automatización de Python..."

python3 debian_autoconfig.py