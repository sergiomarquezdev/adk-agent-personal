#!/bin/bash

# Script para actualizar el agente personal, incluyendo Nginx y Docker Compose

set -e # Salir si cualquier comando falla

# --- Variables de Configuración ---
SCRIPT_DIR="/home/ubuntu/sergio-personal-agent"
LOG_FILE="$SCRIPT_DIR/update.log"
COMPOSE_FILE="$SCRIPT_DIR/docker-compose.yml"
IMAGE_NAME="smarquezp/sergio-personal-agent:latest"
SERVICE_NAME="personal-agent"
NGINX_CONFIG_SRC="$SCRIPT_DIR/nginx.conf"
NGINX_CONFIG_DEST="/etc/nginx/sites-available/chat.sergiomarquez.dev"
FRONTEND_SRC_DIR="$SCRIPT_DIR"
FRONTEND_DEST_DIR="/var/www/chat.sergiomarquez.dev"

# Función para logging
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

# --- Inicio del Script ---
cd "$SCRIPT_DIR"
export PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

log "🚀 Iniciando despliegue completo..."

# 1. Actualizar configuración de Nginx
log "1️⃣  Actualizando configuración de Nginx..."
if [ -f "$NGINX_CONFIG_SRC" ]; then
    sudo mv "$NGINX_CONFIG_SRC" "$NGINX_CONFIG_DEST"
    log "✅ Configuración de Nginx movida a $NGINX_CONFIG_DEST"
else
    log "⚠️  No se encontró nginx.conf en $SCRIPT_DIR. Saltando actualización de Nginx."
fi

# 2. Actualizar archivos del frontend
log "2️⃣  Actualizando archivos del frontend..."
sudo mv "$FRONTEND_SRC_DIR/index.html" "$FRONTEND_DEST_DIR/index.html"
sudo mv "$FRONTEND_SRC_DIR/enhanced_rendering.js" "$FRONTEND_DEST_DIR/enhanced_rendering.js"
log "✅ Archivos de frontend actualizados en $FRONTEND_DEST_DIR"

# 3. Reiniciar Nginx para aplicar los cambios
log "3️⃣  Reiniciando Nginx..."
sudo systemctl restart nginx
log "✅ Nginx reiniciado."

# 4. Actualizar la aplicación Docker
log "4️⃣  Verificando actualizaciones de la imagen Docker: $IMAGE_NAME..."

if [ ! -f "$COMPOSE_FILE" ]; then
    log "❌ Error: No se encontró docker-compose.yml en $SCRIPT_DIR"
    exit 1
fi
if ! docker info > /dev/null 2>&1; then
    log "❌ Error: Docker no está corriendo o no hay permisos"
    exit 1
fi

CURRENT_IMAGE_ID=$(docker images --format "{{.ID}}" "$IMAGE_NAME" 2>/dev/null | head -1)

log "🌐 Descargando la última imagen..."
if command -v docker-compose > /dev/null 2>&1; then
    docker-compose pull --quiet "$SERVICE_NAME" >> "$LOG_FILE" 2>&1
else
    docker compose pull --quiet "$SERVICE_NAME" >> "$LOG_FILE" 2>&1
fi

NEW_IMAGE_ID=$(docker images --format "{{.ID}}" "$IMAGE_NAME" 2>/dev/null | head -1)

if [ "$CURRENT_IMAGE_ID" = "$NEW_IMAGE_ID" ] && [ -n "$CURRENT_IMAGE_ID" ]; then
    log "✅ La imagen de Docker está actualizada. No se requieren cambios en los contenedores."
else
    log "🆕 Nueva imagen encontrada. Actualizando contenedores..."
    if command -v docker-compose > /dev/null 2>&1; then
        docker-compose up -d --no-deps --build $SERVICE_NAME
    else
        docker compose up -d --no-deps --build $SERVICE_NAME
    fi
    log "✅ Contenedores actualizados."
    docker image prune -f >> "$LOG_FILE" 2>&1 || true
fi

log "🎉 Despliegue completado exitosamente!"
log "----------------------------------------"