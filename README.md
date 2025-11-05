# WhatsApp → Home Assistant Agent

Agente domótico inteligente que permite controlar las luces de tu hogar mediante WhatsApp usando un agente de IA. El sistema procesa mensajes en español rioplatense y ejecuta comandos en Home Assistant de forma natural.

## 🚀 Características

- **Control de luces**: Enciende, apaga y ajusta el brillo de las luces por área
- **Control de color**: Cambia el color de las luces (azul, rojo, verde, blanco, cálida, fría)
- **Consulta de estado**: Verifica el estado actual de las luces
- **Entendimiento natural**: Procesa comandos en español rioplatense ("prendé", "apagá", "subí al 50%")
- **Whitelist de números**: Restringe el acceso solo a números autorizados
- **Manejo robusto de errores**: Validaciones y mensajes de error informativos

## 📋 Requisitos

- Python 3.8 o superior
- Home Assistant configurado y accesible
- Cuenta de WhatsApp Business API (Meta Cloud API)
- API Key de OpenAI (o el proveedor de LLM que uses)

## 🛠️ Instalación

1. **Clona el repositorio**:
```bash
git clone <url-del-repositorio>
cd agent1
```

2. **Crea un entorno virtual** (recomendado):
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Instala las dependencias**:
```bash
pip install -r requirements.txt
```

## ⚙️ Configuración

1. **Copia el archivo de ejemplo de variables de entorno**:
```bash
cp env.example .env
```

2. **Edita el archivo `.env`** con tus credenciales:

```env
# FastAPI
PORT=8000

# WhatsApp Cloud API (Meta)
WA_VERIFY_TOKEN=coloca_un_token_de_verificacion
WA_ACCESS_TOKEN=EAA...
WA_PHONE_NUMBER_ID=1XXXXXXXXXX

# Home Assistant
HA_BASE_URL=https://<tu-id>.ui.nabu.casa
HA_TOKEN=eyJhbGciOi...
HA_TIMEOUT_MS=5000

# Seguridad
ALLOWED_NUMBERS=+5989XXXXXXXX,+5989YYYYYYYY
DEFAULT_AREA=living
```

### Variables de entorno explicadas

#### FastAPI
- `PORT`: Puerto donde se ejecutará la aplicación (default: 8000)

#### WhatsApp Cloud API
- `WA_VERIFY_TOKEN`: Token de verificación para el webhook de WhatsApp (puede ser cualquier string que elijas)
- `WA_ACCESS_TOKEN`: Token de acceso de tu aplicación de WhatsApp Business API
- `WA_PHONE_NUMBER_ID`: ID del número de teléfono asociado a tu aplicación

#### Home Assistant
- `HA_BASE_URL`: URL base de tu instancia de Home Assistant (con o sin `/` al final)
- `HA_TOKEN`: Token de acceso de Home Assistant (crear en Configuración → Personas → Tokens de acceso)
- `HA_TIMEOUT_MS`: Timeout en milisegundos para las peticiones a HA (default: 5000)

#### Seguridad
- `ALLOWED_NUMBERS`: Lista de números permitidos separados por comas (ej: `+59891234567,+59898765432`)
  - Si está vacío, permite todos los números
  - Los números pueden incluir o no el prefijo `+`
- `DEFAULT_AREA`: Área por defecto cuando el usuario no especifica una (default: `living`)

### Configuración de WhatsApp Cloud API

1. Crea una aplicación en [Meta for Developers](https://developers.facebook.com/)
2. Configura WhatsApp Business API
3. Obtén el `WA_ACCESS_TOKEN` y `WA_PHONE_NUMBER_ID`
4. Configura el webhook apuntando a: `https://tu-dominio.com/webhook`
5. Usa el `WA_VERIFY_TOKEN` que configuraste en el `.env`

### Configuración de Home Assistant

1. Ve a **Configuración → Personas → Tokens de acceso**
2. Crea un nuevo token
3. Copia el token al `HA_TOKEN` en tu `.env`
4. Asegúrate de que tu instancia de HA sea accesible desde internet (usa Nabu Casa o configura un túnel)

### Configuración del mapeo de áreas

Edita `src/mapping.py` para mapear tus áreas a las entidades de Home Assistant:

```python
AREA_MAP = {
    "living": ["light.living_ceiling", "light.living_lamp"],
    "dormitorio": ["light.bedroom_ceiling"],
    "cocina": ["light.kitchen"]
}
```

También puedes agregar alias en español rioplatense:

```python
AREA_ALIASES = {
    "living": ["living", "estar", "sala"],
    "dormitorio": ["dormitorio", "cuarto", "pieza", "habitación"],
    "cocina": ["cocina", "kitchen"]
}
```

## 🚀 Ejecución

### Desarrollo

```bash
python -m src.app
```

O directamente con uvicorn:

```bash
uvicorn src.app:app --host 0.0.0.0 --port 8000 --reload
```

### Producción

Para producción, usa un servidor WSGI como Gunicorn con Uvicorn workers:

```bash
pip install gunicorn
gunicorn src.app:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

O con uvicorn sin reload:

```bash
uvicorn src.app:app --host 0.0.0.0 --port 8000
```

## 📱 Uso

Una vez configurado, envía mensajes a tu número de WhatsApp Business:

- **Encender luces**: "prendé las luces del living"
- **Apagar luces**: "apagá la cocina"
- **Ajustar brillo**: "subí las luces al 50%"
- **Cambiar color**: "prendé la luz azul en el dormitorio"
- **Consultar estado**: "¿qué luces están prendidas?"

El agente entiende español rioplatense y variaciones naturales del lenguaje.

## 📁 Estructura del Proyecto

```
agent1/
├── src/                    # Código fuente del proyecto
│   ├── __init__.py         # Inicialización del paquete
│   ├── app.py              # FastAPI, webhook WhatsApp, arranque del agente
│   ├── whatsapp.py         # Envío de mensajes por WhatsApp Cloud API
│   ├── ha_client.py        # Cliente REST a Home Assistant
│   ├── tools.py            # Tools del agente (encender, apagar, brillo, color, estado)
│   ├── agent.py            # Construcción del agente smolagents + system prompt
│   ├── mapping.py          # Mapeo área→entity_ids y utilidades
│   └── config.py           # Carga .env y settings
├── requirements.txt        # Dependencias de Python
├── env.example             # Ejemplo de variables de entorno
├── .gitignore              # Archivos ignorados por Git
└── README.md               # Este archivo
```

## 📚 Librerías Utilizadas

### Core
- **FastAPI** (0.115.0): Framework web moderno y rápido para construir APIs
- **Uvicorn** (0.30.6): Servidor ASGI de alto rendimiento
- **httpx** (0.27.2): Cliente HTTP asíncrono para peticiones a APIs externas

### Agente de IA
- **smolagents** (0.2.0): Framework para crear agentes de IA con herramientas
- **pydantic** (2.9.2): Validación de datos usando tipos de Python

### Utilidades
- **python-dotenv** (1.0.1): Carga variables de entorno desde archivo `.env`

### Modelo de IA
Por defecto usa `openai/gpt-4o-mini`, pero puedes cambiar el modelo en `src/agent.py`:

```python
def build_agent(llm="openai/gpt-4o-mini"):
    # Cambia aquí el modelo
    agent = CodeAgent(
        tools=TOOLS,
        system_prompt=SYSTEM_PROMPT,
        model=llm,  # Cambia aquí
        temperature=0.2,
        max_steps=4,
    )
    return agent
```

**Nota**: Necesitarás configurar la variable de entorno correspondiente al proveedor:
- OpenAI: `OPENAI_API_KEY`
- Otros proveedores según la documentación de smolagents

## 🔧 Arquitectura

1. **Webhook de WhatsApp** (`app.py`): Recibe mensajes de WhatsApp Cloud API
2. **Validación**: Verifica whitelist y estructura del mensaje
3. **Agente de IA** (`agent.py`): Procesa el mensaje usando smolagents
4. **Herramientas** (`tools.py`): Ejecuta acciones en Home Assistant
5. **Cliente HA** (`ha_client.py`): Realiza peticiones REST a Home Assistant
6. **Respuesta**: Envía la respuesta al usuario por WhatsApp

## 🛡️ Seguridad

- **Whitelist de números**: Solo números autorizados pueden usar el bot
- **Validación de configuración**: El sistema valida que todas las credenciales estén presentes
- **Manejo de errores**: Errores no exponen información sensible al usuario
- **Tokens seguros**: Usa tokens de acceso de Home Assistant y WhatsApp

## 🐛 Troubleshooting

### Error: "HA_BASE_URL no está configurado"
- Verifica que el archivo `.env` existe y contiene `HA_BASE_URL`

### Error: "WA_ACCESS_TOKEN no está configurado"
- Verifica que el archivo `.env` existe y contiene `WA_ACCESS_TOKEN`

### Error al enviar mensajes de WhatsApp
- Verifica que el `WA_ACCESS_TOKEN` sea válido y no haya expirado
- Verifica que el `WA_PHONE_NUMBER_ID` sea correcto
- Revisa los logs para ver el error específico de la API

### Error de conexión con Home Assistant
- Verifica que `HA_BASE_URL` sea accesible desde internet
- Verifica que el `HA_TOKEN` sea válido
- Aumenta `HA_TIMEOUT_MS` si tu conexión es lenta

### El agente no entiende los comandos
- Verifica que el área esté mapeada en `src/mapping.py`
- Revisa que el `OPENAI_API_KEY` esté configurado
- Aumenta `max_steps` en `src/agent.py` si el agente necesita más pasos

### Webhook no recibe mensajes
- Verifica que el webhook esté configurado correctamente en Meta for Developers
- Verifica que el `WA_VERIFY_TOKEN` coincida con el configurado en Meta
- Asegúrate de que tu servidor sea accesible desde internet (usa ngrok para desarrollo)

## 📝 Notas

- Los mensajes de texto tienen un límite de 4000 caracteres
- El agente tiene un máximo de 4 pasos por interacción
- El sistema solo acepta mensajes de texto por ahora
- Las áreas deben estar previamente mapeadas en `mapping.py`

## 🔄 Próximas Mejoras

- [ ] Soporte para otros tipos de mensajes (imágenes, audio)
- [ ] Descubrimiento automático de entidades desde Home Assistant
- [ ] Soporte para más dispositivos además de luces
- [ ] Logging estructurado
- [ ] Tests unitarios
- [ ] Dockerización

## 📄 Licencia

[Especifica tu licencia aquí]

## 👤 Autor

[Tu nombre/información]

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

