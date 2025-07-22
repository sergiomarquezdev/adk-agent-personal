/**
 * Enhanced HTML Rendering System
 * Solución robusta para renderizar contenido de agentes independientemente del formato
 *
 * Características:
 * - Detección automática de tipo de contenido
 * - Rendering seguro con DOMParser
 * - Fallback para Markdown y texto plano
 * - Prevención automática de XSS
 */

class ContentRenderer {
    constructor() {
        this.parser = new DOMParser();
        this.textRenderer = new TextRenderer();
        this.markdownRenderer = new MarkdownRenderer();
        this.htmlRenderer = new HTMLRenderer();
    }

    /**
     * Detecta el tipo de contenido automáticamente
     */
    detectContentType(content) {
        // Limpiar contenido para análisis
        const trimmed = content.trim();

        // Verificar si contiene etiquetas HTML válidas
        const htmlTagPattern = /<\s*([a-zA-Z][a-zA-Z0-9]*)\b[^>]*>.*?<\s*\/\s*\1\s*>/s;
        const hasValidHTMLTags = htmlTagPattern.test(trimmed);

        // Verificar si contiene etiquetas HTML autónomas
        const selfClosingPattern = /<\s*([a-zA-Z][a-zA-Z0-9]*)\b[^>]*\/?\s*>/;
        const hasSelfClosingTags = selfClosingPattern.test(trimmed);

        // Verificar patrones de Markdown
        const markdownPatterns = [
            /\*\*.*?\*\*/,  // **bold**
            /\*.*?\*/,      // *italic*
            /`.*?`/,        // `code`
            /^#{1,6}\s/m,   // # headers
            /^\s*[-*+]\s/m, // - list items
            /^\s*\d+\.\s/m  // 1. numbered lists
        ];
        const hasMarkdown = markdownPatterns.some(pattern => pattern.test(trimmed));

        // Lógica de detección
        if (hasValidHTMLTags || hasSelfClosingTags) {
            return 'html';
        } else if (hasMarkdown && !hasValidHTMLTags) {
            return 'markdown';
        } else {
            return 'text';
        }
    }

    /**
     * Renderiza contenido usando el método más apropiado
     */
    async renderContent(content, targetElement) {
        try {
            console.log('🎯 ContentRenderer: Procesando contenido...');
            console.log('📝 Contenido (primeros 100 chars):', content.substring(0, 100) + '...');

            const contentType = this.detectContentType(content);
            console.log('🔍 Tipo detectado:', contentType);

            // Limpiar elemento objetivo
            this.clearElement(targetElement);

            // Renderizar según tipo detectado
            switch (contentType) {
                case 'html':
                    await this.htmlRenderer.render(content, targetElement);
                    break;
                case 'markdown':
                    await this.markdownRenderer.render(content, targetElement);
                    break;
                case 'text':
                    this.textRenderer.render(content, targetElement);
                    break;
                default:
                    console.warn('⚠️ Tipo de contenido desconocido, usando texto plano');
                    this.textRenderer.render(content, targetElement);
            }

            console.log('✅ Renderizado completado exitosamente');
            return true;

        } catch (error) {
            console.error('❌ Error en renderizado:', error);

            // Fallback de emergencia: texto plano
            console.log('🔄 Aplicando fallback de texto plano...');
            this.textRenderer.render(content, targetElement);
            return false;
        }
    }

    /**
     * Limpia el elemento objetivo de forma segura
     */
    clearElement(element) {
        while (element.firstChild) {
            element.removeChild(element.firstChild);
        }
    }
}

/**
 * Renderer especializado para HTML
 */
class HTMLRenderer {
    constructor() {
        this.parser = new DOMParser();
        this.sanitizer = new HTMLSanitizer();
    }

    async render(htmlContent, targetElement) {
        console.log('🔧 HTMLRenderer: Procesando HTML...');

        // Desescapar HTML si es necesario
        const unescapedHTML = this.unescapeHtml(htmlContent);

        // Parsear HTML con DOMParser
        const doc = this.parser.parseFromString(unescapedHTML, 'text/html');

        // Verificar errores de parsing
        const parserErrors = doc.querySelectorAll('parsererror');
        if (parserErrors.length > 0) {
            throw new Error('HTML malformado detectado por DOMParser');
        }

        // Extraer contenido del body
        const bodyContent = doc.body;

        // Sanitizar contenido
        const sanitizedContent = this.sanitizer.sanitize(bodyContent);

        // Insertar nodos de forma segura
        this.insertNodes(sanitizedContent, targetElement);

        console.log('✅ HTMLRenderer: HTML renderizado exitosamente');
    }

    unescapeHtml(escapedHtml) {
        return escapedHtml
            .replace(/&lt;/g, '<')
            .replace(/&gt;/g, '>')
            .replace(/&amp;/g, '&')
            .replace(/&quot;/g, '"')
            .replace(/&#x27;/g, "'")
            .replace(/&#39;/g, "'");
    }

    insertNodes(sourceElement, targetElement) {
        // Copiar todos los nodos hijos de forma segura
        const nodes = Array.from(sourceElement.childNodes);
        nodes.forEach(node => {
            const clonedNode = node.cloneNode(true);
            targetElement.appendChild(clonedNode);
        });
    }
}

/**
 * Renderer especializado para Markdown
 */
class MarkdownRenderer {
    async render(markdownContent, targetElement) {
        console.log('📝 MarkdownRenderer: Procesando Markdown...');

        // Convertir Markdown básico a HTML
        const htmlContent = this.convertMarkdownToHTML(markdownContent);

        // Usar HTMLRenderer para el resultado
        const htmlRenderer = new HTMLRenderer();
        await htmlRenderer.render(htmlContent, targetElement);

        console.log('✅ MarkdownRenderer: Markdown renderizado exitosamente');
    }

    convertMarkdownToHTML(markdown) {
        // Conversión básica de Markdown a HTML
        // Nota: En producción, esto podría usar marked.js para mayor robustez
        return markdown
            // Headers
            .replace(/^### (.*$)/gim, '<h3>$1</h3>')
            .replace(/^## (.*$)/gim, '<h2>$1</h2>')
            .replace(/^# (.*$)/gim, '<h1>$1</h1>')

            // Bold y italic
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')

            // Code
            .replace(/`(.*?)`/g, '<code>$1</code>')

            // Links (básico)
            .replace(/\[([^\]]*)\]\(([^)]*)\)/g, '<a href="$2">$1</a>')

            // Line breaks
            .replace(/\n/g, '<br>');
    }
}

/**
 * Renderer especializado para texto plano
 */
class TextRenderer {
    render(textContent, targetElement) {
        console.log('📄 TextRenderer: Procesando texto plano...');

        // Crear nodo de texto de forma segura
        const textNode = document.createTextNode(textContent);
        targetElement.appendChild(textNode);

        console.log('✅ TextRenderer: Texto renderizado exitosamente');
    }
}

/**
 * Sanitizador HTML básico
 */
class HTMLSanitizer {
    constructor() {
        // Lista de etiquetas permitidas
        this.allowedTags = [
            'p', 'div', 'span', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
            'strong', 'b', 'em', 'i', 'u', 'br', 'hr',
            'ul', 'ol', 'li', 'blockquote', 'code', 'pre',
            'a'
        ];

        // Atributos permitidos por etiqueta
        this.allowedAttributes = {
            'a': ['href', 'title'],
            'img': ['src', 'alt', 'title', 'width', 'height']
        };
    }

    sanitize(element) {
        // Clonar elemento para no modificar el original
        const clone = element.cloneNode(true);

        // Procesar todos los elementos
        this.sanitizeElement(clone);

        return clone;
    }

    sanitizeElement(element) {
        // Procesar todos los nodos hijos
        const children = Array.from(element.children);
        children.forEach(child => {
            if (this.isTagAllowed(child.tagName.toLowerCase())) {
                this.sanitizeAttributes(child);
                this.sanitizeElement(child); // Recursivo
            } else {
                // Remover etiqueta no permitida pero conservar contenido
                const parent = child.parentNode;
                while (child.firstChild) {
                    parent.insertBefore(child.firstChild, child);
                }
                parent.removeChild(child);
            }
        });
    }

    isTagAllowed(tagName) {
        return this.allowedTags.includes(tagName);
    }

    sanitizeAttributes(element) {
        const tagName = element.tagName.toLowerCase();
        const allowedAttrs = this.allowedAttributes[tagName] || [];

        // Obtener todos los atributos
        const attributes = Array.from(element.attributes);

        // Remover atributos no permitidos
        attributes.forEach(attr => {
            if (!allowedAttrs.includes(attr.name)) {
                element.removeAttribute(attr.name);
            }
        });
    }
}

// Exportar la instancia global
window.ContentRenderer = ContentRenderer;
