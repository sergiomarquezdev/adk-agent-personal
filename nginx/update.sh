#!/bin/bash

# Script para actualizar el agente personal con Docker Compose

set -e # Salir si cualquier comando falla

# --- Variables de Configuración ---
SCRIPT_DIR="/home/ubuntu/sergio-personal-agent"
LOG_FILE="$SCRIPT_DIR/update.log"
COMPOSE_FILE="$SCRIPT_DIR/docker-compose.yml"
# Nombre completo de la imagen a verificar
IMAGE_NAME="smarquezp/sergio-personal-agent:latest"
# URL del frontend para verificar que Nginx responde
APP_URL="https://chat.sergiomarquez.dev"
# Nombre del servicio en docker-compose.yml
SERVICE_NAME="personal-agent"

# Función para logging
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

# --- Inicio del Script ---
cd "$SCRIPT_DIR"
export PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

log "🔍 Verificando actualizaciones para el agente: $IMAGE_NAME..."

# Verificar que existe docker-compose.yml y Docker
if [ ! -f "$COMPOSE_FILE" ]; then
    log "❌ Error: No se encontró docker-compose.yml en $SCRIPT_DIR"
    exit 1
fi
if ! docker info > /dev/null 2>&1; then
    log "❌ Error: Docker no está corriendo o no hay permisos"
    exit 1
fi

# Obtener ID de la imagen actual
CURRENT_IMAGE_ID=$(docker images --format "{{.ID}}" "$IMAGE_NAME" 2>/dev/null | head -1)
if [ -z "$CURRENT_IMAGE_ID" ]; then
    log "⚠️ No se encontró imagen local, se procederá con la descarga..."
else
    log "📦 Imagen actual ID: $CURRENT_IMAGE_ID"
fi

# Intentar descargar la nueva versión de la imagen
log "🌐 Verificando nueva imagen en el registro..."
if command -v docker-compose > /dev/null 2>&1; then
    docker-compose pull --quiet "$SERVICE_NAME" >> "$LOG_FILE" 2>&1
else
    docker compose pull --quiet "$SERVICE_NAME" >> "$LOG_FILE" 2>&1
fi

# Obtener ID de la imagen después del pull
NEW_IMAGE_ID=$(docker images --format "{{.ID}}" "$IMAGE_NAME" 2>/dev/null | head -1)

# Comparar IDs para ver si hay una actualización
if [ "$CURRENT_IMAGE_ID" = "$NEW_IMAGE_ID" ] && [ -n "$CURRENT_IMAGE_ID" ]; then
    log "✅ No hay actualizaciones disponibles. Saliendo."
    exit 0
fi

log "🆕 Nueva actualización encontrada! Procediendo a actualizar..."
log "📦 Imagen anterior: ${CURRENT_IMAGE_ID:-'(ninguna)'}"
log "📦 Imagen nueva:     $NEW_IMAGE_ID"

# Detener e iniciar los contenedores para aplicar la actualización
log "1️⃣ Deteniendo contenedores..."
if command -v docker-compose > /dev/null 2>&1; then
    docker-compose down >> "$LOG_FILE" 2>&1
else
    docker compose down >> "$LOG_FILE" 2>&1
fi

log "2️⃣ Iniciando contenedores con la nueva imagen..."
if command -v docker-compose > /dev/null 2>&1; then
    docker-compose up -d >> "$LOG_FILE" 2>&1
else
    docker compose up -d >> "$LOG_FILE" 2>&1
fi

log "3️⃣ Esperando 20 segundos a que el servicio se inicie..."
sleep 20

log "4️⃣ Verificando estado de los contenedores..."
if command -v docker-compose > /dev/null 2>&1; then
    docker-compose ps >> "$LOG_FILE" 2>&1
else
    docker compose ps >> "$LOG_FILE" 2>&1
fi

# Verificar que Nginx responde para la URL del chat
if command -v curl > /dev/null 2>&1; then
    log "🔗 Verificando que Nginx responde para $APP_URL..."
    # Para esta app, un 200 (OK) o 404 (Not Found, porque / no es una API) significa que Nginx está funcionando.
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$APP_URL" --max-time 10 || echo "000")

    if [ "$HTTP_CODE" = "200" ] || [ "$HTTP_CODE" = "404" ]; then
        log "✅ El frontend está respondiendo correctamente (HTTP: $HTTP_CODE)"
    else
        log "⚠️ El frontend no responde como se esperaba (HTTP: $HTTP_CODE). Puede haber un problema con Nginx."
    fi
else
    log "⚠️ curl no disponible, no se puede verificar conectividad"
fi

# Limpiar imágenes antiguas sin usar
log "🧹 Limpiando imágenes antiguas..."
docker image prune -f >> "$LOG_FILE" 2>&1 || true

log "✅ Actualización completada exitosamente!"
log "----------------------------------------"

# Mantener solo los últimos 30 días de logs
find "$SCRIPT_DIR" -name "*.log" -type f -mtime +30 -delete 2>/dev/null || true
