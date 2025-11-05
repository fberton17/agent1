# Vercel Deployment Guide

## Configuración para Vercel

### 1. Instalar Vercel CLI (opcional)

```bash
npm i -g vercel
```

### 2. Configurar Variables de Entorno en Vercel

Ve al dashboard de Vercel → Tu proyecto → Settings → Environment Variables

Agrega todas las variables de entorno necesarias:

```env
# WhatsApp Cloud API
WA_VERIFY_TOKEN=tu_token_de_verificacion
WA_ACCESS_TOKEN=tu_access_token
WA_PHONE_NUMBER_ID=tu_phone_number_id

# Home Assistant
HA_BASE_URL=https://tu-instancia.ui.nabu.casa
HA_TOKEN=tu_token_de_ha
HA_TIMEOUT_MS=5000

# Seguridad
ALLOWED_NUMBERS=+59891234567,+59898765432
DEFAULT_AREA=living

# LLM Provider (OpenAI u otro)
OPENAI_API_KEY=tu_openai_api_key
```

### 3. Desplegar a Vercel

#### Opción A: Desde la CLI

```bash
vercel
```

#### Opción B: Desde GitHub

1. Conecta tu repositorio a Vercel
2. Vercel detectará automáticamente la configuración
3. Asegúrate de que todas las variables de entorno estén configuradas

### 4. Configurar Webhook de WhatsApp

Una vez desplegado, obtendrás una URL como: `https://tu-proyecto.vercel.app`

Configura el webhook de WhatsApp en Meta for Developers:
- **URL del webhook**: `https://tu-proyecto.vercel.app/webhook`
- **Token de verificación**: El mismo que configuraste en `WA_VERIFY_TOKEN`

### 5. Verificar el Deployment

1. Ve a: `https://tu-proyecto.vercel.app/webhook?mode=subscribe&token=TU_VERIFY_TOKEN&challenge=test`
2. Deberías recibir "test" como respuesta si está configurado correctamente

## Estructura de Archivos para Vercel

```
agent1/
├── api/
│   └── index.py          # Handler para Vercel serverless functions
├── src/                  # Código fuente
├── vercel.json           # Configuración de Vercel
├── requirements.txt      # Dependencias Python (incluye mangum)
└── .gitignore
```

## Límites de Vercel

- **Plan Gratuito**: 
  - Timeout máximo: 10 segundos
  - Memoria: 1024 MB
  - Puede ser limitado para llamadas complejas del agente

- **Plan Pro/Premium**:
  - Timeout máximo: 60 segundos (configurable)
  - Memoria: Hasta 3008 MB
  - Más adecuado para producción

Si experimentas timeouts, considera:
- Reducir `max_steps` en `src/agent.py`
- Optimizar las respuestas del agente
- Usar un plan de pago de Vercel

## Notas Importantes

1. **Timeout**: Vercel tiene un timeout máximo de 10 segundos en el plan gratuito, 30 segundos en planes de pago. El agente puede tardar más si llama múltiples herramientas. Considera aumentar `max_steps` o optimizar las respuestas.

2. **Cold Starts**: Las funciones serverless pueden tener "cold starts" (inicio en frío) que agregan latencia. Esto es normal y mejora después del primer uso.

3. **Variables de Entorno**: Todas las variables deben estar configuradas en el dashboard de Vercel. No uses archivos `.env` en producción.

4. **Logs**: Los logs aparecen en el dashboard de Vercel → Functions → Logs

5. **Monitoreo**: Usa el dashboard de Vercel para monitorear:
   - Tiempo de respuesta
   - Errores
   - Límites de uso

## Troubleshooting

### Error: "Module not found"
- Verifica que `requirements.txt` incluya todas las dependencias
- Asegúrate de que `mangum` esté en requirements.txt

### Error: "Timeout"
- Reduce `max_steps` en `src/agent.py`
- Considera usar un plan de Vercel con más tiempo de ejecución

### Webhook no funciona
- Verifica que la URL del webhook sea correcta: `https://tu-proyecto.vercel.app/webhook`
- Verifica que `WA_VERIFY_TOKEN` coincida en Vercel y Meta
- Revisa los logs en Vercel para ver errores específicos

### Variables de entorno no se cargan
- Verifica que estén configuradas en el dashboard de Vercel
- Asegúrate de redeploy después de agregar variables
- Verifica que los nombres de las variables coincidan exactamente

