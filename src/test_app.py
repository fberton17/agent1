"""
App de prueba para verificar comunicación WhatsApp + LLM.
No usa herramientas de Home Assistant, solo prueba la conexión básica.
"""
from typing import Optional, Tuple
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import PlainTextResponse
from smolagents import CodeAgent
from .config import WA_VERIFY_TOKEN, ALLOWED_NUMBERS, PORT
from .whatsapp import send_whatsapp_text
import uvicorn

app = FastAPI(title="WhatsApp → LLM Test")

# Crear agente simple sin herramientas, solo para chat
SYSTEM_PROMPT = """
Eres un asistente útil y amigable. Responde en español rioplatense.
Responde de forma corta y natural a las preguntas del usuario.
"""

# Agente sin herramientas, solo para probar la comunicación
test_agent = CodeAgent(
    tools=[],  # Sin herramientas, solo chat
    system_prompt=SYSTEM_PROMPT,
    model="openai/gpt-4o-mini",
    temperature=0.7,
    max_steps=1,  # Solo una respuesta, sin pasos adicionales
)

def is_phone_allowed(phone: str) -> bool:
    """Verifica si el número está en la whitelist."""
    if not ALLOWED_NUMBERS:
        return True  # Si no hay whitelist, permitir todos
    return f"+{phone}" in ALLOWED_NUMBERS or phone in ALLOWED_NUMBERS

def extract_message_from_webhook(data: dict) -> Optional[Tuple[str, Optional[str]]]:
    """
    Extrae el número de teléfono y el texto del mensaje desde la estructura de WhatsApp.
    Retorna (phone, text) o None si no hay mensaje válido.
    """
    try:
        entry = data.get("entry", [])
        if not entry:
            return None
        
        changes = entry[0].get("changes", [])
        if not changes:
            return None
        
        value = changes[0].get("value", {})
        messages = value.get("messages", [])
        if not messages:
            return None
        
        msg = messages[0]
        from_phone = msg.get("from")
        if not from_phone:
            return None
        
        msg_type = msg.get("type", "text")
        if msg_type != "text":
            return (from_phone, None)  # Mensaje no es texto
        
        text_body = msg.get("text", {}).get("body", "")
        if not text_body:
            return None
        
        return (from_phone, text_body.strip())
    except (KeyError, IndexError, TypeError):
        return None

# Verificación de webhook (GET)
@app.get("/webhook", response_class=PlainTextResponse)
async def verify(mode: str = "", challenge: str = "", token: str = ""):
    if mode == "subscribe" and token == WA_VERIFY_TOKEN:
        return challenge
    raise HTTPException(status_code=403, detail="Verification failed")

# Recepción de mensajes (POST)
@app.post("/webhook")
async def webhook(req: Request):
    try:
        data = await req.json()
    except Exception as e:
        print(f"Error parseando JSON del webhook: {e}")
        return {"ok": True}
    
    # Extraer mensaje
    result = extract_message_from_webhook(data)
    if not result:
        return {"ok": True}
    
    from_phone, text = result
    
    # Validar whitelist
    if not is_phone_allowed(from_phone):
        print(f"Número no autorizado: {from_phone}")
        return {"ok": True}
    
    # Si el mensaje no es texto, responder y salir
    if text is None:
        try:
            await send_whatsapp_text(from_phone, "Solo acepto texto por ahora 🙂")
        except Exception as e:
            print(f"Error enviando respuesta de tipo no soportado: {e}")
        return {"ok": True}
    
    # Ejecutar agente (solo LLM, sin herramientas)
    try:
        print(f"Mensaje recibido de {from_phone}: {text}")
        result = await test_agent.run(text)
        answer = result.output if hasattr(result, "output") else str(result)
        
        print(f"Respuesta del LLM: {answer}")
        await send_whatsapp_text(from_phone, answer or "Lo siento, no pude generar una respuesta.")
    except ValueError as e:
        # Errores de validación (configuración faltante)
        print(f"Error de validación: {e}")
        try:
            await send_whatsapp_text(from_phone, "Error de configuración. Revisa los logs.")
        except:
            pass
    except Exception as e:
        print(f"Error ejecutando agente: {e}")
        import traceback
        traceback.print_exc()
        try:
            await send_whatsapp_text(from_phone, f"Ocurrió un error: {str(e)}")
        except:
            pass
    
    return {"ok": True}

if __name__ == "__main__":
    print("=" * 50)
    print("🚀 Iniciando app de prueba (WhatsApp + LLM)")
    print("=" * 50)
    print(f"Puerto: {PORT}")
    print(f"URL webhook: http://localhost:{PORT}/webhook")
    print("=" * 50)
    uvicorn.run("src.test_app:app", host="0.0.0.0", port=PORT, reload=True)

