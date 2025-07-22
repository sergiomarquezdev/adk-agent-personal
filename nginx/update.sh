#!/bin/bash

# Script para actualizar el agente personal, incluyendo Nginx y Docker Compose

set -e # Salir si cualquier comando falla

# --- Variables de Configuración ---
SCRIPT_DIR="/home/ubuntu/sergio-personal-agent"
LOG_FILE="$SCRIPT_DIR/update.log"
IMAGE_NAME="smarquezp/sergio-personal-agent:latest"
SERVICE_NAME="personal-agent"
NGINX_SUBDIR="nginx"

# Función para logging
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

# --- Inicio del Script ---
cd "$SCRIPT_DIR"
export PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

log "🚀 Iniciando despliegue completo..."

# 1. Mover archivos desde el subdirectorio de nginx
log "1️⃣  Moviendo archivos de configuración y frontend..."
sudo mv "$NGINX_SUBDIR/index.html" /var/www/chat.sergiomarquez.dev/
sudo mv "$NGINX_SUBDIR/enhanced_rendering.js" /var/www/chat.sergiomarquez.dev/
sudo mv "$NGINX_SUBDIR/docker-compose.yml" ./docker-compose.yml
sudo mv "$NGINX_SUBDIR/nginx.conf" /etc/nginx/sites-available/chat.sergiomarquez.dev
log "✅ Archivos movidos a sus destinos finales."

# 2. Limpiar el subdirectorio de nginx
log "2️⃣  Limpiando directorio temporal..."
sudo rm -r "$NGINX_SUBDIR"
log "✅ Directorio temporal de nginx eliminado."

# 3. Reiniciar Nginx para aplicar los cambios
log "3️⃣  Reiniciando Nginx..."
sudo systemctl restart nginx
log "✅ Nginx reiniciado."

# 4. Actualizar la aplicación Docker
log "4️⃣  Verificando actualizaciones de la imagen Docker: $IMAGE_NAME..."

if [ ! -f "$SCRIPT_DIR/docker-compose.yml" ]; then
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
    docker-compose -f "$SCRIPT_DIR/docker-compose.yml" pull --quiet "$SERVICE_NAME" >> "$LOG_FILE" 2>&1
else
    docker compose -f "$SCRIPT_DIR/docker-compose.yml" pull --quiet "$SERVICE_NAME" >> "$LOG_FILE" 2>&1
fi

NEW_IMAGE_ID=$(docker images --format "{{.ID}}" "$IMAGE_NAME" 2>/dev/null | head -1)

if [ "$CURRENT_IMAGE_ID" = "$NEW_IMAGE_ID" ] && [ -n "$CURRENT_IMAGE_ID" ]; then
    log "✅ La imagen de Docker está actualizada. No se requieren cambios en los contenedores."
else
    log "🆕 Nueva imagen encontrada. Actualizando contenedores..."
    if command -v docker-compose > /dev/null 2>&1; then
        docker-compose -f "$SCRIPT_DIR/docker-compose.yml" up -d --no-deps --build $SERVICE_NAME
    else
        docker compose -f "$SCRIPT_DIR/docker-compose.yml" up -d --no-deps --build $SERVICE_NAME
    fi
    log "✅ Contenedores actualizados."
    docker image prune -f >> "$LOG_FILE" 2>&1 || true
fi

log "🎉 Despliegue completado exitosamente!"
log "----------------------------------------"
